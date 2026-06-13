import os
import threading
from sqlalchemy.orm import Session

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from core.config import settings

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import CharacterTextSplitter

from core.database import SessionLocal
from .repository import (
    obtener_o_crear_conversacion,
    guardar_mensaje,
    obtener_preguntas_activas,
    obtener_mensajes_recientes,
)

# Umbral de distancia L2 para FAISS: menor distancia = más similar.
# Con paraphrase-multilingual-MiniLM-L12-v2, distancias < 0.8 son buenos matches.
# Ajustar con CHATBOT_DISTANCE_THRESHOLD en el .env si hay falsos positivos/negativos.
DISTANCE_THRESHOLD = float(os.getenv("CHATBOT_DISTANCE_THRESHOLD", "0.8"))

MODELO_PRIMARIO = "llama-3.1-8b-instant"
MODELO_RESPALDO = "llama-3.3-70b-versatile"

MENSAJE_SOBRECARGA = (
    "En este momento estamos recibiendo muchas consultas. "
    "Por favor, espere un momento e intente de nuevo."
)

_knowledge_store = None
_pregunta_store = None
_embeddings = None
_prompt = None
_retriever = None
_init_lock = threading.Lock()


def _get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if not _embeddings:
        # paraphrase-multilingual-MiniLM-L12-v2 maneja bien el español;
        # all-MiniLM-L6-v2 (anterior) era principalmente inglés y daba scores erráticos.
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
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

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(texto)

    _knowledge_store = FAISS.from_texts(chunks, _get_embeddings())
    _retriever = _knowledge_store.as_retriever(search_kwargs={"k": 3})

    template = """Eres el asistente virtual de salud de la Guía Digital del HUAP. Tu único rol es responder preguntas de salud usando exclusivamente la información del Contexto proporcionado.

REGLAS ESTRICTAS (debes seguirlas siempre, sin excepción):
1. Responde ÚNICAMENTE con información que esté literalmente en el Contexto.
2. Si la pregunta es un saludo, despedida, agradecimiento o conversación casual (ej: "hola", "gracias", "cómo estás"), responde EXACTAMENTE: 'Hola. Estoy aquí para responder preguntas sobre salud. ¿En qué puedo ayudarte?'
3. Si la pregunta no está relacionada con salud o no tiene respuesta en el Contexto, responde EXACTAMENTE: 'Lo siento, no tengo esa información.'
4. Nunca inventes información, nunca respondas fuera del Contexto, nunca hagas suposiciones.
5. Responde en español, con un lenguaje claro y simple, adecuado para adultos mayores.

Contexto:
{context}

{history}Pregunta actual:
{question}
"""
    _prompt = PromptTemplate.from_template(template)


def cargar_preguntas_validadas():
    """Construye el índice FAISS a partir de PREGUNTA_CHATBOT. Llamar tras agregar preguntas a la BD."""
    global _pregunta_store
    db = SessionLocal()
    try:
        preguntas = obtener_preguntas_activas(db)
        if not preguntas:
            return

        texts, metadatas = [], []
        for p in preguntas:
            for texto in [p.texto_pregunta] + (p.variantes or []):
                texts.append(texto)
                metadatas.append({"pregunta_id": p.id, "respuesta": p.respuesta_validada})

        _pregunta_store = FAISS.from_texts(texts, _get_embeddings(), metadatas=metadatas)
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


def _buscar_en_whitelist(pregunta: str) -> tuple:
    """Retorna (pregunta_id, respuesta_validada) si hay match, o (None, None).
    Usa distancia L2 de FAISS: menor valor = más similar (opuesto a un score de similitud)."""
    if not _pregunta_store:
        return None, None

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

    # 2. RAG con LLM (primario → respaldo). Si ambos fallan, mensaje amable.
    try:
        respuesta_texto = _invocar_llm(pregunta, historial_texto)
    except Exception:
        msg = guardar_mensaje(db, conv.id, tipo="fallback", contenido=MENSAJE_SOBRECARGA)
        return {"respuesta": MENSAJE_SOBRECARGA, "conversacion_id": conv.id, "mensaje_id": msg.id}

    es_fallback = "Lo siento, no tengo esa información." in respuesta_texto
    tipo_resp = "fallback" if es_fallback else "bot"

    msg = guardar_mensaje(db, conv.id, tipo=tipo_resp, contenido=respuesta_texto)
    return {"respuesta": respuesta_texto, "conversacion_id": conv.id, "mensaje_id": msg.id}
