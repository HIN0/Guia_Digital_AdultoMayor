"""Tests de la advertencia de "esto no es un diagnóstico".

El bot no diagnostica —la regla 2 del prompt se lo prohíbe y, preguntado de
frente, responde que no reemplaza al médico— pero medido con el flujo real,
"¿esto que tengo es neumonía?" recibía la descripción de la neumonía sin ninguna
aclaración. Esos casos salen por la whitelist, así que las reglas del prompt no
los alcanzan.

Ejecutar desde backend/:  python -m pytest tests/test_advertencias.py -v
"""

import pytest

from modules.chatbot.advertencias import (
    ADVERTENCIA_DIAGNOSTICO,
    con_advertencia,
    pide_diagnostico,
)
from modules.chatbot.seeds import SEED_DATA


@pytest.mark.parametrize("pregunta", [
    # Los casos medidos que motivaron la advertencia
    "tengo fiebre y tos, que tengo?",
    "esto que tengo es neumonia?",
    "me arde al orinar, tengo infeccion urinaria?",
    "tengo dolor de espalda hace 3 dias, que sera?",
    # Otras formas de pedir lo mismo
    "sera que tengo neumonia",
    "que enfermedad puede ser",
    "que me esta pasando",
    "puede ser que tenga una infeccion",
    "sera presion alta lo mio",
])
def test_reconoce_que_le_estan_pidiendo_un_diagnostico(pregunta):
    assert pide_diagnostico(pregunta), f"no lo reconoció: '{pregunta}'"


@pytest.mark.parametrize("pregunta", [
    # Trámites: contienen "qué tengo" sin pedir un diagnóstico
    "que tengo que hacer si me siento mal",
    "que tengo que llevar al hospital",
    "que tengo para el dolor",
    # Definitorias
    "que es la neumonia",
    "que es neumonia",
    "como se previene la gastroenteritis",
    # Causa de algo ya diagnosticado, o diagnóstico ya dado por un médico
    "por que tengo dolor de cabeza",
    "me dijeron que tengo hipertension",
    # Sin relación
    "que sera bueno comer",
    "que enfermedades cubre el ges",
    "a que hora abre el hospital",
    "hola",
])
def test_no_confunde_otras_preguntas_con_un_diagnostico(pregunta):
    assert not pide_diagnostico(pregunta), f"falso positivo: '{pregunta}'"


def test_la_advertencia_se_agrega_sin_reemplazar_la_respuesta():
    """A diferencia de las banderas rojas, no corta el flujo: la persona recibe
    igual la información que pidió."""
    respuesta = "El lumbago es el dolor en la parte baja de la espalda."

    con = con_advertencia(respuesta)

    assert con.startswith(respuesta)
    assert ADVERTENCIA_DIAGNOSTICO.strip() in con


def test_no_se_repite_si_la_respuesta_validada_ya_la_trae():
    """Varias respuestas del equipo de salud ya aclaran que no diagnostican."""
    respuesta = "No puedo darle un diagnóstico; consulte con su médico."

    assert con_advertencia(respuesta) == respuesta


def test_la_advertencia_no_invade_el_uso_corriente():
    """Puesta en cada respuesta se vuelve invisible a los tres usos. Sobre las
    ~1.000 preguntas de la whitelist debe activarse en una fracción pequeña."""
    preguntas = [
        texto
        for pregs in SEED_DATA.values()
        for item in pregs
        for texto in [item["pregunta"]] + item.get("variantes", [])
    ]
    disparos = [p for p in preguntas if pide_diagnostico(p)]

    assert len(preguntas) > 500
    assert len(disparos) < len(preguntas) * 0.05, (
        f"{len(disparos)} de {len(preguntas)} preguntas reciben la advertencia: "
        f"{disparos[:10]}"
    )


# ── En el flujo real ─────────────────────────────────────────────────────────

def test_la_respuesta_de_la_whitelist_llega_con_la_advertencia(bot):
    """El caso medido: la pregunta sale por whitelist, que no pasa por el
    prompt, y aun así debe llevar la aclaración."""
    resultado = bot.preguntar("esto que tengo es neumonia?")

    assert "no es un diagnóstico" in resultado["respuesta"].lower()


def test_una_pregunta_normal_no_lleva_advertencia(bot):
    resultado = bot.preguntar("¿qué es la neumonía?")

    assert ADVERTENCIA_DIAGNOSTICO.strip() not in resultado["respuesta"]


def test_una_emergencia_no_lleva_advertencia(bot):
    """Ante un posible infarto la única respuesta es llamar al 131; agregarle
    una aclaración sobre diagnósticos solo diluye el mensaje."""
    resultado = bot.preguntar("me duele mucho el pecho")

    assert ADVERTENCIA_DIAGNOSTICO.strip() not in resultado["respuesta"]
    assert "131" in resultado["respuesta"]
