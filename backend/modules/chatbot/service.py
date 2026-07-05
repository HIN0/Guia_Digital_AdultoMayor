import os
import threading
from sqlalchemy.orm import Session

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from core.config import settings

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

from core.database import SessionLocal
from .normalizacion import normalizar_texto
from .repository import (
    obtener_o_crear_conversacion,
    guardar_mensaje,
    obtener_preguntas_activas,
    obtener_mensajes_recientes,
)

# Umbrales de distancia L2² para FAISS sobre embeddings NORMALIZADOS
# (equivale a 2·(1−coseno)): menor distancia = más similar. Calibrados con
# paraphrase-multilingual-MiniLM-L12-v2 normalizado sobre una batería de
# preguntas reales. Ajustables por .env si aparecen falsos positivos/negativos.
#
# Whitelist: solo matches semánticos claros (paráfrasis reales quedan bajo
# ~0.35). Sobre este valor el vecino más cercano puede ser de otro tema
# ("quién ganó el partido" queda a 0.5 de una variante de salud) o responder
# la pregunta equivocada; esos casos van al LLM, que con el RAG responde la
# sección correcta.
DISTANCE_THRESHOLD = float(os.getenv("CHATBOT_DISTANCE_THRESHOLD", "0.45"))
# Conocimiento: sobre este valor la pregunta está claramente fuera de alcance
# y se responde el fallback SIN gastar una llamada al LLM (la batería de
# preguntas de salud en alcance marcó máximo 1.34).
UMBRAL_FUERA_DE_ALCANCE = float(os.getenv("CHATBOT_FUERA_DE_ALCANCE", "1.4"))

MODELO_PRIMARIO = "llama-3.1-8b-instant"
MODELO_RESPALDO = "llama-3.3-70b-versatile"

MENSAJE_SOBRECARGA = (
    "En este momento estamos recibiendo muchas consultas. "
    "Por favor, espere un momento e intente de nuevo."
)

# Respuestas fijas para conversación casual. Deben coincidir con las de
# seeds/general.py para que el bot responda igual venga de la whitelist
# o del LLM (reglas 2-4 del prompt).
RESPUESTA_SALUDO = "Hola. Estoy aquí para responder preguntas sobre salud. ¿En qué puedo ayudarte?"
RESPUESTA_DESPEDIDA = "Hasta pronto. Cuídese mucho y recuerde asistir a sus controles médicos."
RESPUESTA_AGRADECIMIENTO = "De nada. Si tiene otra pregunta sobre salud, estoy aquí para ayudarle."

# Frase centinela para detectar el fallback: debe ser prefijo del mensaje
# completo, porque generar_y_guardar_respuesta la busca dentro de la respuesta.
FRASE_SIN_INFORMACION = "Lo siento, no tengo esa información."
MENSAJE_SIN_INFORMACION = (
    FRASE_SIN_INFORMACION + " Puedo ayudarle con temas como presión alta, caídas, "
    "dolor de cabeza, dolor de espalda, infección urinaria, neumonía o "
    "gastroenteritis, y con información del hospital y de esta plataforma. "
    "¿Sobre cuál le gustaría saber?"
)

_knowledge_store = None
_pregunta_store = None
_exact_lookup = {}
_embeddings = None
_prompt = None
_retriever = None
_init_lock = threading.Lock()

# Caché de respuestas del LLM por pregunta normalizada. Solo se usa en el
# primer mensaje de una conversación (sin historial), para no servir una
# respuesta cacheada a un seguimiento tipo "¿y eso duele?" que depende del
# contexto. Preguntas repetidas no vuelven a gastar cuota de Groq.
_llm_cache = {}
_LLM_CACHE_MAX = 500


def _get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if not _embeddings:
        # paraphrase-multilingual-MiniLM-L12-v2 maneja bien el español;
        # all-MiniLM-L6-v2 (anterior) era principalmente inglés y daba scores erráticos.
        # normalize_embeddings=True es clave: sin normalizar, FAISS devuelve
        # distancias L2² en una escala ~2-14 y el umbral de 0.8 no matcheaba
        # nunca (toda pregunta caía al LLM aunque estuviera en la whitelist).
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings


def _crear_llm(modelo: str) -> ChatGroq:
    return ChatGroq(
        model=modelo,
        temperature=0.0,
        groq_api_key=settings.GROQ_API_KEY,
        max_retries=2,
        timeout=30,
    )


def _formatear_historial(mensajes: list) -> str:
    if not mensajes:
        return ""
    lineas = ["Conversación previa:"]
    for m in mensajes:
        rol = "Usuario" if m.tipo == "usuario" else "Asistente"
        lineas.append(f"{rol}: {m.contenido}")
    return "\n".join(lineas) + "\n\n"


def _dividir_por_secciones(texto: str) -> list:
    """Divide conocimiento.txt en un chunk por sección (###), anteponiendo el
    título del tema (##) para que cada chunk conserve su contexto al ser
    recuperado (ej: "HIPERTENSIÓN ARTERIAL — Banderas rojas...").

    Reemplaza al CharacterTextSplitter anterior, que cortaba cada 500
    caracteres sin respetar las secciones y dejaba chunks sin su título."""
    chunks = []
    tema = ""
    titulo = ""
    lineas = []

    def _cerrar_chunk():
        contenido = "\n".join(lineas).strip()
        if not contenido:
            return
        encabezado = " — ".join(parte for parte in (tema, titulo) if parte)
        chunks.append(f"{encabezado}\n{contenido}" if encabezado else contenido)

    for linea in texto.splitlines():
        if linea.startswith("### "):
            _cerrar_chunk()
            lineas = []
            titulo = linea[4:].strip()
        elif linea.startswith("## "):
            _cerrar_chunk()
            lineas = []
            tema = linea[3:].strip()
            titulo = ""
        elif linea.strip() == "---":
            continue
        else:
            lineas.append(linea)
    _cerrar_chunk()
    return chunks


def inicializar_base_conocimiento():
    global _knowledge_store, _prompt, _retriever

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    carpeta_data = os.path.join(directorio_actual, "data")
    base_path = os.path.join(carpeta_data, "conocimiento.txt")
    os.makedirs(carpeta_data, exist_ok=True)

    if not os.path.exists(base_path):
        with open(base_path, "w", encoding="utf-8") as f:
            f.write(
                "La Guía Digital del HUAP ayuda a los adultos mayores a aprender "
                "tecnología. El horario de soporte es de 8:00 a 17:00 hrs."
            )

    with open(base_path, "r", encoding="utf-8") as f:
        texto = f.read()

    chunks = _dividir_por_secciones(texto)

    _knowledge_store = FAISS.from_texts(chunks, _get_embeddings())
    _retriever = _knowledge_store.as_retriever(search_kwargs={"k": 3})

    template = f"""Eres el asistente virtual de salud de la Guía Digital del HUAP. Tu único rol es responder preguntas de salud usando exclusivamente la información del Contexto proporcionado.

REGLAS ESTRICTAS (debes seguirlas siempre, sin excepción):
1. Si el Contexto contiene información relacionada con la pregunta, RESPONDE con esa información, aunque la pregunta esté escrita de forma coloquial o con errores de ortografía.
2. Responde ÚNICAMENTE con información que esté en el Contexto: nunca inventes, nunca supongas, nunca indiques dosis ni recomiendes, cambies o suspendas medicamentos, y nunca entregues diagnósticos.
3. Si la pregunta es solo un saludo (ej: "hola", "buenos días", "cómo estás"), responde EXACTAMENTE: '{RESPUESTA_SALUDO}'
4. Si la pregunta es una despedida (ej: "chao", "adiós", "hasta luego", "me voy"), responde EXACTAMENTE: '{RESPUESTA_DESPEDIDA}'
5. Si la pregunta es un agradecimiento (ej: "gracias", "muy amable"), responde EXACTAMENTE: '{RESPUESTA_AGRADECIMIENTO}'
6. SOLO si el Contexto no contiene NADA relacionado con la pregunta, o la pregunta no es de salud, responde EXACTAMENTE: '{MENSAJE_SIN_INFORMACION}'
7. Usa la Conversación previa solo para entender a qué se refiere la pregunta actual (ej: "¿y eso duele?"); nunca la uses como fuente de información médica.
8. Responde en español, con frases cortas y lenguaje claro y simple, adecuado para personas mayores.

Contexto:
{{context}}

{{history}}Pregunta actual:
{{question}}
"""
    _prompt = PromptTemplate.from_template(template)


def cargar_preguntas_validadas():
    """Construye el índice FAISS y el diccionario de match exacto a partir de
    PREGUNTA_CHATBOT. Llamar tras agregar preguntas a la BD."""
    global _pregunta_store, _exact_lookup
    db = SessionLocal()
    try:
        preguntas = obtener_preguntas_activas(db)
        if not preguntas:
            return

        texts, metadatas = [], []
        lookup = {}
        for p in preguntas:
            for texto in [p.texto_pregunta] + (p.variantes or []):
                texts.append(texto)
                metadatas.append({"pregunta_id": p.id, "respuesta": p.respuesta_validada})
                lookup[normalizar_texto(texto)] = (p.id, p.respuesta_validada)

        _pregunta_store = FAISS.from_texts(texts, _get_embeddings(), metadatas=metadatas)
        _exact_lookup = lookup
    finally:
        db.close()


def inicializar_chatbot():
    """Inicializa embeddings e índices FAISS de forma thread-safe.
    Llamar desde el startup de FastAPI antes de aceptar tráfico."""
    with _init_lock:
        if not _knowledge_store:
            inicializar_base_conocimiento()
        if not _pregunta_store:
            cargar_preguntas_validadas()


def _distancia_conocimiento(pregunta: str):
    """Distancia del mejor chunk de conocimiento a la pregunta, o None si el
    índice no está cargado. Sirve para saber si la pregunta es del dominio."""
    if not _knowledge_store:
        return None
    results = _knowledge_store.similarity_search_with_score(pregunta, k=1)
    return results[0][1] if results else None


def _buscar_en_whitelist(pregunta: str) -> tuple:
    """Retorna (pregunta_id, respuesta_validada) si hay match, o (None, None).

    Dos niveles:
    1. Match exacto sobre texto normalizado (determinístico: "¡Chao!" siempre
       cae en la despedida, sin riesgo de que el embedding lo confunda con
       "hola").
    2. Match semántico claro (distancia ≤ DISTANCE_THRESHOLD). Los matches
       más lejanos NO se aceptan aunque sean de salud: el vecino más cercano
       puede ser la pregunta equivocada, y el LLM con RAG lo resuelve mejor."""
    if not _pregunta_store:
        return None, None

    exacto = _exact_lookup.get(normalizar_texto(pregunta))
    if exacto:
        return exacto

    results = _pregunta_store.similarity_search_with_score(pregunta, k=1)
    if not results:
        return None, None

    doc, distance = results[0]
    if distance <= DISTANCE_THRESHOLD:
        return doc.metadata["pregunta_id"], doc.metadata["respuesta"]

    return None, None


def _invocar_llm(pregunta: str, historial: str) -> str:
    """Invoca RAG con el modelo primario; si falla (ej. 429), intenta con el respaldo.
    Los límites de Groq son por modelo, así que el respaldo tiene cuota propia."""
    docs = _retriever.invoke(pregunta)
    contexto = "\n\n".join(d.page_content for d in docs)
    mensaje = _prompt.format(context=contexto, history=historial, question=pregunta)

    try:
        return _crear_llm(MODELO_PRIMARIO).invoke(mensaje).content
    except Exception:
        return _crear_llm(MODELO_RESPALDO).invoke(mensaje).content


def generar_y_guardar_respuesta(db: Session, usuario_id: int, pregunta: str, conversacion_id: int = None) -> dict:
    if not _knowledge_store or not _pregunta_store:
        inicializar_chatbot()

    conv = obtener_o_crear_conversacion(db, usuario_id, conversacion_id)

    mensajes_previos = obtener_mensajes_recientes(db, conv.id, limite=6)
    historial_texto = _formatear_historial(mensajes_previos)

    guardar_mensaje(db, conv.id, tipo="usuario", contenido=pregunta)

    # 1. Whitelist primero — no consume cuota de Groq
    pregunta_id, respuesta_validada = _buscar_en_whitelist(pregunta)
    if respuesta_validada:
        msg = guardar_mensaje(db, conv.id, tipo="bot", contenido=respuesta_validada, pregunta_chatbot_id=pregunta_id)
        return {"respuesta": respuesta_validada, "conversacion_id": conv.id, "mensaje_id": msg.id}

    # 2. Sin historial la pregunta es autocontenida: se puede servir desde el
    #    caché o cortar por fuera de alcance, sin gastar cuota de Groq.
    #    Con historial se salta directo al LLM, porque un seguimiento tipo
    #    "¿y eso duele?" necesita el contexto de la conversación.
    clave_cache = normalizar_texto(pregunta) if not mensajes_previos else None
    if clave_cache:
        respuesta_cacheada = _llm_cache.get(clave_cache)
        if respuesta_cacheada:
            tipo_resp = "fallback" if FRASE_SIN_INFORMACION in respuesta_cacheada else "bot"
            msg = guardar_mensaje(db, conv.id, tipo=tipo_resp, contenido=respuesta_cacheada)
            return {"respuesta": respuesta_cacheada, "conversacion_id": conv.id, "mensaje_id": msg.id}

        dist_conocimiento = _distancia_conocimiento(pregunta)
        if dist_conocimiento is not None and dist_conocimiento > UMBRAL_FUERA_DE_ALCANCE:
            msg = guardar_mensaje(db, conv.id, tipo="fallback", contenido=MENSAJE_SIN_INFORMACION)
            return {"respuesta": MENSAJE_SIN_INFORMACION, "conversacion_id": conv.id, "mensaje_id": msg.id}

    # 3. RAG con LLM (primario → respaldo). Si ambos fallan, mensaje amable.
    try:
        respuesta_texto = _invocar_llm(pregunta, historial_texto)
    except Exception:
        msg = guardar_mensaje(db, conv.id, tipo="fallback", contenido=MENSAJE_SOBRECARGA)
        return {"respuesta": MENSAJE_SOBRECARGA, "conversacion_id": conv.id, "mensaje_id": msg.id}

    es_fallback = FRASE_SIN_INFORMACION in respuesta_texto
    tipo_resp = "fallback" if es_fallback else "bot"

    if clave_cache:
        if len(_llm_cache) >= _LLM_CACHE_MAX:
            _llm_cache.pop(next(iter(_llm_cache)))
        _llm_cache[clave_cache] = respuesta_texto

    msg = guardar_mensaje(db, conv.id, tipo=tipo_resp, contenido=respuesta_texto)
    return {"respuesta": respuesta_texto, "conversacion_id": conv.id, "mensaje_id": msg.id}
