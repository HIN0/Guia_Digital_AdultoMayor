import os
from sqlalchemy.orm import Session

# --- Nuevos imports actualizados a LangChain 0.2+ ---
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import CharacterTextSplitter

from .repository import obtener_o_crear_conversacion, guardar_mensaje

# Instancia global en memoria para evitar recargar el archivo en cada petición
vector_store = None

def inicializar_base_conocimiento():
    global vector_store
    
    # 1. Obtener la ruta absoluta del directorio actual (service.py)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Construir la ruta hacia la carpeta data interna del módulo
    carpeta_data = os.path.join(directorio_actual, "data")
    base_path = os.path.join(carpeta_data, "conocimiento.txt")
    
    # 3. Asegurar que la carpeta exista
    os.makedirs(carpeta_data, exist_ok=True)
    
    if not os.path.exists(base_path):
        with open(base_path, "w", encoding="utf-8") as f:
            f.write("La Guía Digital del HUAP ayuda a los adultos mayores a aprender tecnología. El horario de soporte es de 8:00 a 17:00 hrs.")
            
    with open(base_path, "r", encoding="utf-8") as f:
        texto = f.read()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(texto)
    
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)

def generar_y_guardar_respuesta(db: Session, usuario_id: int, pregunta: str, conversacion_id: int = None) -> dict:
    global vector_store
    if not vector_store:
        inicializar_base_conocimiento()

    # 1. Gestionar historial
    conv = obtener_o_crear_conversacion(db, usuario_id, conversacion_id)
    guardar_mensaje(db, conv.id, tipo="usuario", contenido=pregunta)

    # 2. Configurar IA (Temperatura 0 para evitar alucinaciones)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
    
    template = """Eres el asistente virtual de la Guía Digital del HUAP. Hablas con adultos mayores.
    REGLA: Responde ÚNICAMENTE usando la información del Contexto.
    Si la respuesta no está en el Contexto, DEBES responder exactamente: 'Lo siento, no tengo esa información. Le sugiero consultar directamente en el mesón de atención.'

    Contexto:
    {context}

    Pregunta:
    {question}
    """
    prompt = PromptTemplate.from_template(template)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
    )
    
    # 3. Ejecutar inferencia
    respuesta_obj = rag_chain.invoke(pregunta)
    respuesta_texto = respuesta_obj.content

    # 4. Analizar respuesta para métricas (Bot vs Fallback)
    es_fallback = "Lo siento, no tengo esa información" in respuesta_texto
    tipo_resp = "fallback" if es_fallback else "bot"

    guardar_mensaje(db, conv.id, tipo=tipo_resp, contenido=respuesta_texto)

    return {
        "respuesta": respuesta_texto,
        "conversacion_id": conv.id
    }