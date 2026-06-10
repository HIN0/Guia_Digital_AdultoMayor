import os
from sqlalchemy.orm import Session

# ── LLM ──────────────────────────────────────────────────────────────────────
# OPCIÓN FUTURA — OpenAI (requiere OPENAI_API_KEY con billing activado)
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# OPCIÓN ACTIVA — Groq (gratuito) + embeddings locales (sin API key)
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from core.config import settings

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import CharacterTextSplitter

from core.database import SessionLocal
from .repository import obtener_o_crear_conversacion, guardar_mensaje, obtener_preguntas_activas, obtener_mensajes_recientes

# Umbral de similitud para considerar un match en la whitelist (0-1)
SIMILARITY_THRESHOLD = 0.82

# Singletons de módulo — se inicializan una sola vez al primer request
_knowledge_store = None   # FAISS sobre conocimiento.txt (RAG)
_pregunta_store = None    # FAISS sobre PREGUNTA_CHATBOT (whitelist)
_embeddings = None        # modelo de embeddings compartido
_llm = None
_rag_chain = None


def _get_embeddings() -> HuggingFaceEmbeddings:
    # OPCIÓN FUTURA — OpenAI embeddings
    # return OpenAIEmbeddings()

    # OPCIÓN ACTIVA — modelo local, primer uso descarga ~90 MB, luego queda en caché
    global _embeddings
    if not _embeddings:
        _embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return _embeddings


def _get_llm() -> ChatGroq:
    # OPCIÓN FUTURA — OpenAI GPT-4o-mini
    # return ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

    # OPCIÓN ACTIVA — Llama 3.1 8B via Groq (gratuito)
    global _llm
    if not _llm:
        _llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.0, groq_api_key=settings.GROQ_API_KEY)
    return _llm


def _formatear_historial(mensajes: list) -> str:
    if not mensajes:
        return ""
    lineas = ["Conversación previa:"]
    for m in mensajes:
        rol = "Usuario" if m.tipo == "usuario" else "Asistente"
        lineas.append(f"{rol}: {m.contenido}")
    return "\n".join(lineas) + "\n\n"


def inicializar_base_conocimiento():
    global _knowledge_store, _rag_chain

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    carpeta_data = os.path.join(directorio_actual, "data")
    base_path = os.path.join(carpeta_data, "conocimiento.txt")
    os.makedirs(carpeta_data, exist_ok=True)

    if not os.path.exists(base_path):
        with open(base_path, "w", encoding="utf-8") as f:
            f.write("La Guía Digital del HUAP ayuda a los adultos mayores a aprender tecnología. El horario de soporte es de 8:00 a 17:00 hrs.")

    with open(base_path, "r", encoding="utf-8") as f:
        texto = f.read()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(texto)

    # OPCIÓN FUTURA — OpenAI embeddings
    # embeddings = OpenAIEmbeddings()

    # OPCIÓN ACTIVA — embeddings locales
    _knowledge_store = FAISS.from_texts(chunks, _get_embeddings())

    template = """Eres el asistente virtual de la Guía Digital del HUAP. Hablas con adultos mayores.
REGLA: Responde ÚNICAMENTE usando la información del Contexto.
Si la respuesta no está en el Contexto, responde exactamente: 'Lo siento, no tengo esa información. Le sugiero consultar directamente en el mesón de atención.'

Contexto:
{context}

{history}Pregunta actual:
{question}
"""
    prompt = PromptTemplate.from_template(template)
    retriever = _knowledge_store.as_retriever(search_kwargs={"k": 3})

    def _format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    _rag_chain = (
        {
            "context": (lambda x: x["question"]) | retriever | _format_docs,
            "question": lambda x: x["question"],
            "history": lambda x: x.get("history", ""),
        }
        | prompt
        | _get_llm()
    )


def cargar_preguntas_validadas():
    """Construye el índice FAISS a partir de PREGUNTA_CHATBOT. Llama tras agregar preguntas a la BD."""
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

        # OPCIÓN FUTURA — OpenAI embeddings
        # embeddings = OpenAIEmbeddings()

        # OPCIÓN ACTIVA — embeddings locales (mismo modelo que el knowledge store)
        _pregunta_store = FAISS.from_texts(texts, _get_embeddings(), metadatas=metadatas)
    finally:
        db.close()


def _buscar_en_whitelist(pregunta: str) -> tuple:
    """Retorna (pregunta_id, respuesta_validada) si hay match, o (None, None)."""
    if not _pregunta_store:
        return None, None

    results = _pregunta_store.similarity_search_with_relevance_scores(pregunta, k=1)
    if not results:
        return None, None

    doc, score = results[0]
    if score >= SIMILARITY_THRESHOLD:
        return doc.metadata["pregunta_id"], doc.metadata["respuesta"]

    return None, None


def generar_y_guardar_respuesta(db: Session, usuario_id: int, pregunta: str, conversacion_id: int = None) -> dict:
    global _knowledge_store, _pregunta_store

    if not _knowledge_store:
        inicializar_base_conocimiento()
    if not _pregunta_store:
        cargar_preguntas_validadas()

    conv = obtener_o_crear_conversacion(db, usuario_id, conversacion_id)

    # Obtener historial antes de guardar el mensaje actual
    mensajes_previos = obtener_mensajes_recientes(db, conv.id, limite=6)
    historial_texto = _formatear_historial(mensajes_previos)

    guardar_mensaje(db, conv.id, tipo="usuario", contenido=pregunta)

    # 1. Buscar primero en la whitelist de respuestas validadas
    pregunta_id, respuesta_validada = _buscar_en_whitelist(pregunta)
    if respuesta_validada:
        guardar_mensaje(db, conv.id, tipo="bot", contenido=respuesta_validada, pregunta_chatbot_id=pregunta_id)
        return {"respuesta": respuesta_validada, "conversacion_id": conv.id}

    # 2. Fallback: RAG sobre conocimiento.txt con LLM (incluye historial)
    respuesta_obj = _rag_chain.invoke({"question": pregunta, "history": historial_texto})
    respuesta_texto = respuesta_obj.content

    es_fallback = "Lo siento, no tengo esa información" in respuesta_texto
    tipo_resp = "fallback" if es_fallback else "bot"

    guardar_mensaje(db, conv.id, tipo=tipo_resp, contenido=respuesta_texto)
    return {"respuesta": respuesta_texto, "conversacion_id": conv.id}
