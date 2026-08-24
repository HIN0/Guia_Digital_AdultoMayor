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


def test_whitelist_rechaza_preguntas_ajenas(service_configurado):
    """Regresión del falso positivo: estas preguntas quedan a distancia media
    (~0.5-0.7) de alguna variante de salud, y con el umbral antiguo de 0.8
    recibían una respuesta validada que no correspondía."""
    for pregunta in ["quien gano el partido de la u", "cuentame un chiste"]:
        _, respuesta = service_configurado._buscar_en_whitelist(pregunta)
        assert respuesta is None, f"'{pregunta}' recibió respuesta de whitelist: {respuesta}"


def test_pregunta_de_salud_ambigua_va_al_llm_no_al_fallback(service_configurado):
    """Una pregunta de salud sin match claro en la whitelist debe pasar al LLM,
    en vez de matchear con la pregunta equivocada."""
    pregunta = "la ciatica se cura sola"
    _, respuesta = service_configurado._buscar_en_whitelist(pregunta)

    assert respuesta is None, f"matcheó whitelist con: {respuesta}"


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


# ── La whitelist no puede responder de otra condición ────────────────────────

@pytest.mark.parametrize("pregunta", [
    "cuanto dura la bronquitis",   # matcheaba neumonía a 0.299
    "que es la gastritis",         # matcheaba gastroenteritis a 0.370
    "me duele la muela",           # matcheaba "me duele al orinar" a 0.053
    "que es una hernia",           # matcheaba infección urinaria a 0.287
    "me duele la rodilla",         # matcheaba una respuesta de espalda a 0.413
])
def test_no_responde_de_un_tema_que_no_cubre(service_configurado, pregunta):
    """El conocimiento cubre 33 temas y la whitelist solo 10, así que las
    preguntas sobre los temas nuevos caen cerca de respuestas viejas y sin
    relación. Si la persona nombra una condición, la respuesta validada tiene
    que hablar de esa condición; si no, el caso es del LLM."""
    _, respuesta = service_configurado._buscar_en_whitelist(pregunta)

    assert respuesta is None, f"'{pregunta}' recibió una respuesta ajena: {respuesta[:90]}"


@pytest.mark.parametrize("pregunta", [
    "que es la neumonia",
    "cuanto dura la gastroenteritis",
    "que es la infeccion urinaria",
    "que es la presion alta",
    "me duele la cabeza hace dias",
    "se cayo mi mama y no se puede parar",
    "que remedio tomo",
])
def test_las_respuestas_validadas_que_si_corresponden_se_conservan(
    service_configurado, pregunta
):
    """Contrapeso: la regla no debe apagar la whitelist donde sí cubre el tema."""
    _, respuesta = service_configurado._buscar_en_whitelist(pregunta)

    assert respuesta is not None, f"'{pregunta}' perdió su respuesta validada"
