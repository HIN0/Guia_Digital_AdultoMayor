"""Tests de cobertura de la base de conocimiento.

El contenido corresponde al listado de enfermedades prevalentes en adultos
mayores atendidos en el Servicio de Urgencia del HUAP. Estos tests no juzgan el
contenido clínico —eso lo valida el equipo de salud— sino que verifiquen que
cada tema exista, esté completo en los aspectos que más se preguntan, y sea
alcanzable por el nombre con que la gente lo llama.

Ejecutar desde backend/:  python -m pytest tests/test_conocimiento.py -v
"""

import os

import pytest

from modules.chatbot.normalizacion import normalizar_texto

try:
    from modules.chatbot import service as _service
except Exception:  # sin .env o sin dependencias del backend
    _service = None

requiere_service = pytest.mark.skipif(
    _service is None, reason="modules.chatbot.service no importable"
)


def _chunks():
    ruta = os.path.join(os.path.dirname(_service.__file__), "data", "conocimiento.txt")
    with open(ruta, encoding="utf-8") as f:
        return _service._dividir_por_secciones(f.read())


def _temas():
    return {c.splitlines()[0].split(" — ")[0] for c in _chunks()}


# Las cinco categorías del documento del HUAP, con el término que debe permitir
# encontrar cada condición.
CONDICIONES = [
    # Sistema digestivo
    "dental", "colecistitis", "pancreatitis", "gastritis", "hernia",
    "constipacion", "hemorragia", "gastroenteritis",
    # Signos y síntomas
    "cefalea", "pecho", "abdominal", "disnea", "delirium",
    # Traumatismos
    "fracturas", "craneal", "esguinces",
    # Sistema respiratorio
    "resfrio", "bronquitis", "epoc", "neumonia",
    # Sistema osteomuscular
    "lumbago", "contractura", "cervicalgia", "rodilla", "hombro",
]


@requiere_service
@pytest.mark.parametrize("termino", CONDICIONES)
def test_cada_condicion_del_huap_tiene_su_tema(termino):
    """Cada condición del listado debe existir como tema del conocimiento."""
    temas_normalizados = " | ".join(normalizar_texto(t) for t in _temas())

    assert termino in temas_normalizados, (
        f"no hay ningún tema que cubra '{termino}'. Temas: {sorted(_temas())}"
    )


@requiere_service
@pytest.mark.parametrize("termino", CONDICIONES)
def test_cada_condicion_se_encuentra_por_su_nombre(service_configurado, termino):
    """El término tiene que identificar el tema por sí solo, sin depender del
    embedding: las siglas y los nombres cortos se pierden al vectorizar ("¿qué
    es la EPOC?" recuperaba la sección de golpes en la cabeza)."""
    assert service_configurado._tema_nombrado(termino) is not None, (
        f"'{termino}' no identifica ningún tema; revisar que aparezca en un encabezado ##"
    )


@requiere_service
def test_las_condiciones_dicen_cuando_ir_a_urgencias():
    """"¿Cuándo tengo que preocuparme?" es de las preguntas más importantes y
    más frecuentes: ningún tema de una condición debería quedarse sin ella."""
    # Los temas que no son una condición: la portada, el glosario, la
    # información del hospital y la nota de fuentes.
    no_son_condiciones = ("guía", "glosario", "información", "fuentes")
    señales = ("alarma", "urgencia", "consultar", "131")

    sin_alarma = []
    for tema in _temas():
        if any(p in tema.lower() for p in no_son_condiciones):
            continue
        texto = " ".join(c for c in _chunks() if c.startswith(tema)).lower()
        if not any(p in texto for p in señales):
            sin_alarma.append(tema)

    assert not sin_alarma, f"temas sin señales de alarma ni cuándo consultar: {sin_alarma}"


@requiere_service
@pytest.mark.parametrize("tema_parcial", [
    "LUMBAGO", "NEUMONÍA", "GASTROENTERITIS", "RESFRÍO", "BRONQUITIS", "ESGUINCES",
    "GASTRITIS", "COLECISTITIS", "PANCREATITIS", "CONSTIPACIÓN", "CERVICALGIA",
    "CONTRACTURA", "RODILLA", "HOMBRO", "DENTAL", "URINARIA", "CEFALEA",
    "DELIRIUM", "CRANEAL", "FRACTURAS", "ABDOMINAL", "EPOC", "HIPERTENSIÓN",
])
def test_cada_condicion_tiene_una_seccion_sobre_cuanto_dura(tema_parcial):
    """"¿Y cuánto dura?" es el seguimiento más frecuente, y no basta con que el
    dato aparezca en alguna parte: tiene que estar en una sección propia.

    Regresión doble. Primero, el bot respondía "¿qué es el lumbago?" diciendo
    que mejora en días o semanas y al preguntarle "¿cuánto dura?" contestaba que
    no tenía esa información, porque el dato estaba en la whitelist pero no en
    el conocimiento. Después pasó lo mismo con gastritis: el dato sí estaba,
    pero enterrado dentro de "¿Qué es?", y la búsqueda de "cuánto dura" no lo
    encontraba. Por eso se exige la sección, no la palabra."""
    titulos = [
        c.splitlines()[0].split(" — ")[-1].lower()
        for c in _chunks()
        if tema_parcial in c.splitlines()[0]
    ]

    assert any("dura" in t or "recupera" in t or "se cura" in t for t in titulos), (
        f"{tema_parcial} no tiene una sección sobre cuánto dura. Secciones: {titulos}"
    )


@requiere_service
def test_el_documento_declara_sus_fuentes():
    """El contenido se redactó desde fuentes oficiales y debe poder auditarse."""
    texto = " ".join(_chunks())

    assert "minsal" in texto.lower()
    assert "medlineplus" in texto.lower()
    assert "validad" in texto.lower(), "debe constar que requiere validación del equipo de salud"
