# -*- coding: utf-8 -*-
"""Batería de consultas reales de personas mayores contra el chatbot.

Las preguntas provienen del catálogo de consultas esperadas del HUAP: lo que
efectivamente pregunta una persona mayor (o quien la cuida), con sus palabras.
No se ejercita el LLM —eso dependería de Groq, de la red y de la temperatura—
sino las capas deterministas que deciden QUÉ se le va a responder:

  · las urgencias, que se responden sin consultar al modelo;
  · las crisis de salud mental, por el mismo motivo;
  · el tema con que se busca en la base de conocimiento;
  · la continuidad de ese tema a lo largo de una conversación.

Buena parte del catálogo queda FUERA de la base de conocimiento (diabetes,
colesterol, sueño, memoria, trámites, cuidadores). Para esas la conducta
correcta no es acertar un tema, sino no inventarlo: un tema equivocado desvía
la búsqueda y produce una respuesta de otra patología.
"""

import pytest

from modules.chatbot.banderas_rojas import (
    detectar_bandera_roja,
    detectar_crisis_salud_mental,
)

# ── 1. Urgencias: deben escalar sin pasar por el modelo ─────────────────────

URGENCIAS = [
    "Me duele el pecho y me falta el aire",
    "Se me durmió medio cuerpo y no puedo hablar bien",
    "Mi papá se cayó y no se puede parar",
    "Mi mamá se cayó y no puede levantarse",
    "Me caí y no me puedo parar",
    "Se desmayó y no reacciona",
    "Estoy vomitando sangre",
    "Se le traba la lengua desde hace un rato",
    "Tiene los labios morados",
]


@pytest.mark.parametrize("pregunta", URGENCIAS)
def test_las_urgencias_escalan(pregunta):
    """Estas respuestas no pueden depender de que Groq esté disponible ni de
    que el match semántico acierte."""
    assert detectar_bandera_roja(pregunta) is True


# Consultas frecuentes que se parecen a una urgencia sin serlo. Sobre-avisar
# no es gratis: un bot que grita 131 por una molestia enseña a la persona a no
# hacerle caso cuando la urgencia sea de verdad.
NO_SON_URGENCIA = [
    "Me caí en el baño, ¿voy al médico?",
    "¿Cómo evito caerme en la casa?",
    "¿Qué es un infarto?",
    "¿Cuáles son los síntomas de un ataque cerebrovascular?",
    "¿Cómo se previene la neumonía?",
    "La presión alta puede dar infarto",
    "Me duelen las rodillas al levantarme",
    "Tengo los pies hinchados hace días",
    "Me da mareo cuando me paro de la cama",
    "No puedo dormir hace semanas",
    "Me canso mucho al subir escaleras",
]


@pytest.mark.parametrize("pregunta", NO_SON_URGENCIA)
def test_no_se_sobre_avisa(pregunta):
    assert detectar_bandera_roja(pregunta) is False


# ── 2. Crisis de salud mental ───────────────────────────────────────────────

CRISIS = [
    "¿Para qué sigo viviendo si ya no sirvo para nada?",
    "Ya no quiero vivir",
    "A veces pienso en quitarme la vida",
    "Siento que soy una carga para mi familia",
    "Mejor estaría muerta",
    "No vale la pena seguir",
]


@pytest.mark.parametrize("pregunta", CRISIS)
def test_las_senales_de_riesgo_suicida_se_detectan(pregunta):
    """Sin esta capa, "¿para qué sigo viviendo?" seguía el flujo normal y
    terminaba en un "no tengo esa información".

    La asimetría del error manda: un falso positivo cuesta una derivación
    amable a una línea de apoyo; un falso negativo puede costar una vida."""
    assert detectar_crisis_salud_mental(pregunta) is True


NO_SON_CRISIS = [
    "Me siento sola desde que murió mi esposo",
    "Ando triste y sin ganas de nada",
    "¿Cómo puedo saber si tengo depresión o solo estoy triste?",
    "Me duele la rodilla",
    "Estoy agotada de cuidar a mi abuela",
    "¿Cuánto me queda de vida?",
]


@pytest.mark.parametrize("pregunta", NO_SON_CRISIS)
def test_la_tristeza_y_el_duelo_no_se_tratan_como_crisis(pregunta):
    """El duelo y el desánimo merecen acompañamiento, no el mensaje de crisis.
    Confundirlos vacía de significado la derivación cuando sí corresponde."""
    assert detectar_crisis_salud_mental(pregunta) is False


# ── 3. Temas que la base de conocimiento sí cubre ───────────────────────────

EN_COBERTURA = [
    ("Tengo la presión en 150/90, ¿está mala?", "HIPERTENSIÓN ARTERIAL (PRESIÓN ALTA)"),
    ("¿Puedo tomar el remedio de la presión con el estómago vacío?",
     "HIPERTENSIÓN ARTERIAL (PRESIÓN ALTA)"),
    ("¿La artrosis se puede curar?", "DOLOR Y ARTROSIS DE RODILLA (GONALGIA Y GONARTROSIS)"),
    ("Me duelen las rodillas al levantarme, ¿qué hago?",
     "DOLOR Y ARTROSIS DE RODILLA (GONALGIA Y GONARTROSIS)"),
    ("Llevo 3 días con diarrea y vómitos, ¿qué debo comer?", "GASTROENTERITIS AGUDA"),
    ("¿Cómo evito caerme en la casa?", "CAÍDAS EN ADULTOS MAYORES"),
    ("¿Qué es la neumonía?", "NEUMONÍA ADQUIRIDA EN LA COMUNIDAD"),
    ("Tengo dolor de espalda baja", "LUMBAGO (DOLOR DE ESPALDA BAJA)"),
]


@pytest.mark.parametrize("pregunta,tema_esperado", EN_COBERTURA)
def test_las_consultas_cubiertas_encuentran_su_tema(
    service_configurado, pregunta, tema_esperado
):
    assert service_configurado._tema_de_texto(pregunta) == tema_esperado


# ── 4. Palabras corrientes que no deben fijar un tema ───────────────────────
# Regresión: los términos distintivos se derivan de los encabezados, y una
# palabra común que aparezca en uno solo quedaba como su identificador
# exclusivo. Importa más desde que el match literal tiene prioridad sobre los
# embeddings: un término distintivo malo ya no lo corrige nadie.

SIN_TEMA_LITERAL = [
    ("¿Qué enfermedad tengo?", "enfermedad estaba en el encabezado de EPOC"),
    ("¿Puedo seguir con mi enfermedad crónica?", "crónica estaba en el de EPOC"),
    ("Tengo dificultad para caminar", "dificultad estaba en el de disnea"),
    ("Tengo ataques de ansiedad por la noche", "ataque estaba en el del ACV"),
    ("¿Dónde consulto un tema de salud?", "salud estaba en el del glosario"),
    ("¿Puedo estar tranquila con este resultado?", "estar estaba en el de constipación"),
]


@pytest.mark.parametrize("pregunta,motivo", SIN_TEMA_LITERAL)
def test_las_palabras_corrientes_no_nombran_un_tema(
    service_configurado, pregunta, motivo
):
    assert service_configurado._tema_nombrado(pregunta) is None, motivo


# ── 5. Continuidad de la conversación ───────────────────────────────────────
# El caso que originó estos tests: los seguimientos vagos no nombran ningún
# tema y la votación de vecinos les asigna uno igual, con plena confianza.
# Medido: "cuanto puede durar?" cae en ESGUINCES y "que remedios se
# recomienda?" en GASTROENTERITIS.

SEGUIMIENTOS_VAGOS = [
    "cuanto puede durar?",
    "que remedios se recomienda?",
    "¿y eso es grave?",
    "¿cuándo tengo que preocuparme?",
    "¿y qué puedo hacer?",
]


@pytest.mark.parametrize("seguimiento", SEGUIMIENTOS_VAGOS)
def test_un_seguimiento_vago_no_secuestra_el_tema(service_configurado, seguimiento):
    """El tema nombrado con todas sus letras sobrevive al seguimiento vago.

    Sin esto, la persona preguntaba por la neumonía, luego "cuanto puede
    durar?", y en el turno siguiente el asistente ya creía estar hablando de
    esguinces: la búsqueda se desviaba y el mensaje de "no sé" ofrecía
    contusiones y golpes a alguien que consultaba por una infección
    pulmonar."""
    from types import SimpleNamespace

    mensajes = [
        SimpleNamespace(tipo="usuario", contenido="¿Qué es la neumonía?"),
        SimpleNamespace(
            tipo="bot", contenido="La neumonía es una infección de los pulmones."
        ),
        SimpleNamespace(tipo="usuario", contenido=seguimiento),
    ]

    assert (
        service_configurado._tema_de_conversacion(mensajes)
        == "NEUMONÍA ADQUIRIDA EN LA COMUNIDAD"
    )


def test_cambiar_de_tema_si_la_persona_nombra_otro(service_configurado):
    """La preferencia por el tema nombrado no puede dejar a la persona
    atrapada: si nombra otro, ese manda por ser el más reciente."""
    from types import SimpleNamespace

    mensajes = [
        SimpleNamespace(tipo="usuario", contenido="¿Qué es la neumonía?"),
        SimpleNamespace(
            tipo="bot", contenido="La neumonía es una infección de los pulmones."
        ),
        SimpleNamespace(tipo="usuario", contenido="ahora quiero saber de la presión alta"),
    ]

    assert (
        service_configurado._tema_de_conversacion(mensajes)
        == "HIPERTENSIÓN ARTERIAL (PRESIÓN ALTA)"
    )


def test_la_conversacion_completa_mantiene_el_tema(bot):
    """El caso real de punta a punta, con el flujo entero: tres turnos, y el
    tercero todavía busca en la sección correcta."""
    bot.preguntar("¿Qué es la neumonía?")
    bot.preguntar("cuanto puede durar?")
    bot.preguntar("que remedios se recomienda?")

    assert bot.llamadas[-1]["tema"] == "NEUMONÍA ADQUIRIDA EN LA COMUNIDAD"


def test_una_urgencia_a_media_conversacion_corta_el_flujo(bot):
    """Aunque se venga hablando de otra cosa, la urgencia manda y no llega al
    modelo."""
    bot.preguntar("¿Qué es la neumonía?")
    llamadas_antes = len(bot.llamadas)

    resultado = bot.preguntar("ahora me duele el pecho y me falta el aire")

    assert resultado["tipo"] == "emergencia"
    assert "131" in resultado["respuesta"]
    assert len(bot.llamadas) == llamadas_antes, "no debió consultarse al modelo"


def test_una_crisis_a_media_conversacion_corta_el_flujo(bot):
    """Igual que la urgencia, pero con el mensaje de contención y sin el marco
    rojo de alarma que el frontend reserva para las emergencias."""
    bot.preguntar("Me duelen las rodillas")
    llamadas_antes = len(bot.llamadas)

    resultado = bot.preguntar("¿para qué sigo viviendo si ya no sirvo para nada?")

    assert resultado["tipo"] == "crisis"
    assert "600 360 7777" in resultado["respuesta"]
    assert len(bot.llamadas) == llamadas_antes, "no debió consultarse al modelo"


# ── 6. El mensaje de "no sé" ────────────────────────────────────────────────


def test_el_no_se_nunca_nombra_una_patologia(service_configurado):
    """Afirmar de qué SÍ se puede hablar exige acertar el tema, y la detección
    falla justo en los seguimientos vagos, que es cuando más aparece este
    mensaje."""
    temas = [
        "NEUMONÍA ADQUIRIDA EN LA COMUNIDAD",
        "ESGUINCES, CONTUSIONES Y GOLPES",
        "HIPERTENSIÓN ARTERIAL (PRESIÓN ALTA)",
    ]
    for tema in temas:
        mensaje = service_configurado._mensaje_sin_informacion(tema)
        nombre = tema.split("(")[0].strip().lower()
        assert nombre not in mensaje.lower()
        assert mensaje.startswith(service_configurado.FRASE_SIN_INFORMACION)
