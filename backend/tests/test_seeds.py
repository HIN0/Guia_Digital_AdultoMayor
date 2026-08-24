"""Tests de integridad de la whitelist del chatbot (seeds/).

Rápidos y 100% offline: solo importan los diccionarios de seeds y la
normalización de texto, sin langchain, sin base de datos y sin .env.

Ejecutar desde backend/:  python -m pytest tests/test_seeds.py -v
"""

import re

from modules.chatbot.normalizacion import normalizar_texto
from modules.chatbot.seeds import SEED_DATA


def _todas_las_preguntas():
    """Itera (patologia, item) por cada pregunta de la whitelist."""
    for patologia, preguntas in SEED_DATA.items():
        for item in preguntas:
            yield patologia, item


def test_patologias_esperadas():
    esperadas = {
        "General",
        "Información General HUAP",
        "Hipertensión Arterial",
        "Caídas en Adultos Mayores",
        "Glosario de Salud",
    }
    faltantes = esperadas - set(SEED_DATA.keys())
    assert not faltantes, f"Faltan patologías en SEED_DATA: {faltantes}"


def test_toda_pregunta_tiene_respuesta():
    for patologia, item in _todas_las_preguntas():
        assert item.get("pregunta", "").strip(), f"Pregunta vacía en {patologia}"
        assert item.get("respuesta", "").strip(), (
            f"Respuesta vacía para '{item.get('pregunta')}' en {patologia}"
        )
        assert isinstance(item.get("variantes", []), list), (
            f"'variantes' debe ser lista en '{item['pregunta']}' ({patologia})"
        )


def test_sin_textos_ambiguos_en_whitelist():
    """Un mismo texto (normalizado) no puede apuntar a dos preguntas DISTINTAS:
    haría ambiguo el match exacto y el índice FAISS. Que una variante repita
    su propia pregunta es inofensivo (misma respuesta) y no se marca aquí."""
    vistos = {}
    ambiguos = []
    for patologia, item in _todas_las_preguntas():
        for texto in [item["pregunta"]] + item.get("variantes", []):
            clave = normalizar_texto(texto)
            duenio = f"'{item['pregunta']}' ({patologia})"
            if clave in vistos and vistos[clave] != duenio:
                ambiguos.append(f"'{texto}' ({patologia}) ya existe en {vistos[clave]}")
            else:
                vistos[clave] = duenio
    assert not ambiguos, "Textos ambiguos en la whitelist:\n" + "\n".join(ambiguos)


def test_respuestas_sin_dosis_de_medicamentos():
    """Pilar de seguridad del proyecto: el bot nunca indica dosis."""
    patron_dosis = re.compile(
        r"\b\d+\s*(mg|ml|mcg|gramos|miligramos|comprimidos?|pastillas?|gotas|c/8|cada\s+\d+\s+horas)\b",
        re.IGNORECASE,
    )
    for patologia, item in _todas_las_preguntas():
        match = patron_dosis.search(item["respuesta"])
        assert not match, (
            f"Posible dosis '{match.group()}' en la respuesta de "
            f"'{item['pregunta']}' ({patologia})"
        )


def test_respuestas_de_largo_razonable():
    """Respuestas cortas y legibles para personas mayores (y para el TTS)."""
    for patologia, item in _todas_las_preguntas():
        largo = len(item["respuesta"])
        assert largo <= 900, (
            f"Respuesta de {largo} caracteres (máx 900) en "
            f"'{item['pregunta']}' ({patologia})"
        )


def test_normalizar_texto():
    assert normalizar_texto("¡Chao!") == "chao"
    assert normalizar_texto("  ¿A qué HORA   atienden?  ") == "a que hora atienden"
    assert normalizar_texto("adiós") == normalizar_texto("adios")
