"""Tests del matching de la whitelist y del chunking del conocimiento.

Dos niveles:
  1. Match exacto normalizado (rápido, offline): reproduce el lookup que
     construye service.cargar_preguntas_validadas y verifica el bug de
     coherencia "chao" → respuesta de despedida (no el saludo).
  2. Match semántico FAISS (lento la primera vez: descarga el modelo de
     embeddings ~470 MB). Se salta automáticamente si sentence-transformers
     no está instalado.

El chunking (_dividir_por_secciones) se testea importando service, que
requiere el .env del backend; si no está disponible, esos tests se saltan.

Ejecutar desde backend/:  python -m pytest tests/test_whitelist.py -v
"""

import os

import pytest

from modules.chatbot.normalizacion import normalizar_texto
from modules.chatbot.seeds import SEED_DATA

# El mismo umbral que usa service._buscar_en_whitelist por defecto
DISTANCE_THRESHOLD = float(os.getenv("CHATBOT_DISTANCE_THRESHOLD", "0.45"))


def _construir_lookup():
    """Réplica del lookup exacto de service.cargar_preguntas_validadas,
    construido desde los seeds (sin base de datos)."""
    lookup = {}
    for preguntas in SEED_DATA.values():
        for item in preguntas:
            for texto in [item["pregunta"]] + item.get("variantes", []):
                lookup[normalizar_texto(texto)] = item["respuesta"]
    return lookup


LOOKUP = _construir_lookup()


# ── 1. Match exacto (coherencia de conversación casual) ──────────────────────

def test_chao_responde_despedida_no_saludo():
    respuesta = LOOKUP.get(normalizar_texto("chao"))
    assert respuesta is not None, "'chao' debe estar en la whitelist"
    assert "Hasta pronto" in respuesta, f"'chao' respondió: {respuesta}"
    assert "¿En qué puedo ayudarte?" not in respuesta, (
        "'chao' está respondiendo con el saludo (bug de coherencia)"
    )


def test_chao_con_signos_y_mayusculas():
    assert LOOKUP.get(normalizar_texto("¡Chao!")) == LOOKUP.get("chao")


def test_hola_responde_saludo():
    respuesta = LOOKUP.get(normalizar_texto("hola"))
    assert respuesta and "¿En qué puedo ayudarte?" in respuesta


def test_gracias_responde_agradecimiento():
    respuesta = LOOKUP.get(normalizar_texto("gracias"))
    assert respuesta and "De nada" in respuesta


def test_temas_nuevos_en_whitelist():
    assert LOOKUP.get(normalizar_texto("¿Qué es la presión alta?")) is not None
    assert LOOKUP.get(normalizar_texto("se cayo mi abuela que hago")) is not None


# ── 2. Match semántico FAISS (requiere modelo de embeddings) ─────────────────

@pytest.fixture(scope="module")
def embeddings():
    pytest.importorskip("langchain_huggingface")
    pytest.importorskip("langchain_community")
    from langchain_huggingface import HuggingFaceEmbeddings

    # Misma configuración que service._get_embeddings (normalización incluida)
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        encode_kwargs={"normalize_embeddings": True},
    )


@pytest.fixture(scope="module")
def pregunta_store(embeddings):
    from langchain_community.vectorstores import FAISS

    texts, metadatas = [], []
    for i, (patologia, preguntas) in enumerate(SEED_DATA.items()):
        for item in preguntas:
            for texto in [item["pregunta"]] + item.get("variantes", []):
                texts.append(texto)
                metadatas.append({
                    "patologia": patologia,
                    "respuesta": item["respuesta"],
                    "pregunta_id": i,  # placeholder: en producción es el id de BD
                })
    return FAISS.from_texts(texts, embeddings, metadatas=metadatas)


def _mejor_match(store, pregunta):
    doc, distancia = store.similarity_search_with_score(pregunta, k=1)[0]
    return doc.metadata, distancia


@pytest.mark.parametrize(
    "pregunta, patologia_esperada",
    [
        ("me duele mucho la cabeza desde ayer", "Urgencias y Síntomas Frecuentes"),
        ("se me cayo la abuelita al suelo y no se para", "Caídas en Adultos Mayores"),
        ("ando con la presion arterial alta", "Hipertensión Arterial"),
        ("a que hora abre el hospital", "Información General HUAP"),
        ("que significa ser de fonasa", "Glosario de Salud"),
        ("mi marido es hombre y tiene infeccion de orina", "Urgencias y Síntomas Frecuentes"),
    ],
)
def test_matching_semantico(pregunta_store, pregunta, patologia_esperada):
    metadata, distancia = _mejor_match(pregunta_store, pregunta)
    assert distancia <= DISTANCE_THRESHOLD, (
        f"'{pregunta}' quedó fuera del umbral ({distancia:.3f} > {DISTANCE_THRESHOLD}); "
        "caería al LLM en vez de la whitelist"
    )
    assert metadata["patologia"] == patologia_esperada, (
        f"'{pregunta}' matcheó con {metadata['patologia']} (distancia {distancia:.3f})"
    )


def test_pregunta_fuera_de_alcance_no_matchea(pregunta_store):
    _, distancia = _mejor_match(pregunta_store, "cual es la capital de francia")
    assert distancia > DISTANCE_THRESHOLD, (
        "Una pregunta fuera de alcance no debería matchear la whitelist "
        f"(distancia {distancia:.3f})"
    )


# ── 3. Chunking por secciones (requiere .env del backend) ────────────────────

try:
    from modules.chatbot import service as _service
except Exception:  # sin .env o sin dependencias del backend
    _service = None

requiere_service = pytest.mark.skipif(
    _service is None, reason="modules.chatbot.service no importable (falta .env o dependencias)"
)


@pytest.fixture(scope="module")
def service_configurado(embeddings, pregunta_store):
    """Configura los índices de service desde los seeds (sin base de datos)
    para poder testear la lógica real de _buscar_en_whitelist y los umbrales."""
    if _service is None:
        pytest.skip("modules.chatbot.service no importable (falta .env o dependencias)")
    from langchain_community.vectorstores import FAISS

    ruta = os.path.join(os.path.dirname(_service.__file__), "data", "conocimiento.txt")
    with open(ruta, encoding="utf-8") as f:
        chunks = _service._dividir_por_secciones(f.read())
    knowledge = FAISS.from_texts(chunks, embeddings)

    lookup = {}
    for i, preguntas in enumerate(SEED_DATA.values()):
        for item in preguntas:
            for texto in [item["pregunta"]] + item.get("variantes", []):
                lookup[normalizar_texto(texto)] = (i, item["respuesta"])

    anterior = (_service._pregunta_store, _service._knowledge_store, _service._exact_lookup)
    _service._pregunta_store = pregunta_store
    _service._knowledge_store = knowledge
    _service._exact_lookup = lookup
    yield _service
    _service._pregunta_store, _service._knowledge_store, _service._exact_lookup = anterior


def test_whitelist_rechaza_preguntas_ajenas(service_configurado):
    """Regresión del falso positivo: estas preguntas quedan a distancia media
    (~0.5-0.7) de alguna variante de salud, y con el umbral antiguo de 0.8
    recibían una respuesta validada que no correspondía."""
    for pregunta in ["quien gano el partido de la u", "cuentame un chiste"]:
        _, respuesta = service_configurado._buscar_en_whitelist(pregunta)
        assert respuesta is None, f"'{pregunta}' recibió respuesta de whitelist: {respuesta}"


def test_pregunta_de_salud_ambigua_va_al_llm_no_al_fallback(service_configurado):
    """Una pregunta de salud sin match claro en la whitelist debe pasar al LLM
    (no matchear whitelist con la pregunta equivocada, ni cortarse por fuera
    de alcance)."""
    pregunta = "la ciatica se cura sola"
    _, respuesta = service_configurado._buscar_en_whitelist(pregunta)
    assert respuesta is None, f"matcheó whitelist con: {respuesta}"

    distancia = service_configurado._distancia_conocimiento(pregunta)
    assert distancia <= service_configurado.UMBRAL_FUERA_DE_ALCANCE


def test_umbral_fuera_de_alcance(service_configurado):
    """El corte sin LLM debe activarse para lo claramente ajeno y nunca para
    preguntas de salud que el RAG puede responder."""
    lejos = service_configurado._distancia_conocimiento("cuanto cuesta el dolar hoy")
    assert lejos > service_configurado.UMBRAL_FUERA_DE_ALCANCE

    cerca = service_configurado._distancia_conocimiento(
        "mi marido esta con diarrea que le doy de comer"
    )
    assert cerca <= service_configurado.UMBRAL_FUERA_DE_ALCANCE


@requiere_service
def test_chunks_conservan_titulo_de_seccion():
    ruta = os.path.join(
        os.path.dirname(_service.__file__), "data", "conocimiento.txt"
    )
    with open(ruta, encoding="utf-8") as f:
        chunks = _service._dividir_por_secciones(f.read())

    assert len(chunks) > 30, f"Se esperaban >30 secciones, hay {len(chunks)}"

    horario = [c for c in chunks if "24 horas del día" in c]
    assert horario, "No se encontró el chunk del horario del HUAP"
    assert "Horarios de atención" in horario[0].splitlines()[0], (
        "El chunk del horario no conserva su título de sección"
    )

    for chunk in chunks:
        assert len(chunk) < 1600, f"Chunk demasiado largo ({len(chunk)} caracteres)"
