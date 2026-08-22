"""Tests de la detección de banderas rojas (síntomas de emergencia).

El riesgo que cubren es el más grave del chatbot: antes de esta capa, el match
semántico de la whitelist respondía "me duele mucho el pecho" con la respuesta
de infección urinaria (quedaba a 0.215 de la variante "me duele al orinar") y
"creo que me está dando un infarto" con la de ciática (0.402). Ambas por debajo
del umbral de 0.45, es decir, entregadas en duro y sin pasar por el LLM.

La detección es por frases, no por embeddings, precisamente porque los
embeddings fallan aquí. Los síntomas provienen de MINSAL (ver banderas_rojas.py).

Ejecutar desde backend/:  python -m pytest tests/test_banderas_rojas.py -v
"""

import pytest

from modules.chatbot.banderas_rojas import detectar_bandera_roja
from modules.chatbot.seeds import SEED_DATA

# ── Debe disparar ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("pregunta", [
    # Los dos casos que originaron esta capa
    "me duele mucho el pecho",
    "creo que me esta dando un infarto",
    # Infarto agudo al miocardio (síntomas MINSAL)
    "tengo un dolor apretado en el pecho",
    "siento presion en el pecho y sudor frio",
    "me duele el pecho y no puedo respirar",
    # Presentación silente, la advertida por MINSAL para adultos mayores
    "de repente me falta el aire",
    "me cuesta respirar desde anoche",
    # Ataque cerebrovascular (los tres signos de MINSAL)
    "se me durmio la cara y no puedo hablar",
    "mi mama tiene la boca torcida",
    "se me durmio medio cuerpo",
    "no puedo mover el brazo derecho",
    # Compromiso de conciencia
    "mi esposo se desmayo y no despierta",
    "mi papa no reacciona",
    # Otros
    "tengo los labios morados",
    "la herida no para de sangrar",
    "creo que es una emergencia",
])
def test_dispara_ante_sintomas_de_emergencia(pregunta):
    assert detectar_bandera_roja(pregunta), f"no detectó la emergencia: '{pregunta}'"


# ── No debe disparar ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("pregunta", [
    # Preguntas definitorias: merecen información, no el aviso del 131
    "que es un infarto",
    "como se previene un infarto",
    "cuales son los sintomas de la neumonia",
    # Construcciones hipotéticas o de consecuencia
    "la presion alta puede dar infarto",
    "que hago para prevenir un infarto",
    # Negación explícita
    "donde consulto si no es una emergencia",
    # El ardor retroesternal después de comer es reflujo, no infarto: MINSAL
    # describe el infarto como dolor o presión, nunca como ardor. Sobre-avisar
    # enseña a la persona a ignorar el aviso cuando la urgencia sea de verdad.
    "ando con acidez y me arde el pecho despues de comer",
    "me arde el pecho al comer",
    # Molestias que no son banderas rojas
    "me duele la cabeza",
    "me duele la espalda",
    "me duele al orinar",
    "tengo diarrea hace dos dias",
    "a que hora abre el hospital",
])
def test_no_dispara_ante_consultas_normales(pregunta):
    assert not detectar_bandera_roja(pregunta), f"falso positivo: '{pregunta}'"


def test_la_pregunta_por_remedios_no_es_emergencia():
    """La respuesta validada de medicamentos es más útil aquí que el aviso del
    131, y es la consulta más sensible del bot después de las urgencias."""
    assert not detectar_bandera_roja("¿qué remedio tomo para el dolor?")


# ── Barrido sobre toda la whitelist ──────────────────────────────────────────

def _todas_las_preguntas():
    for patologia, preguntas in SEED_DATA.items():
        for item in preguntas:
            for texto in [item["pregunta"]] + item.get("variantes", []):
                yield patologia, texto


def test_los_disparos_sobre_la_whitelist_son_solo_banderas_rojas_reales():
    """Barrido de control sobre las ~1000 preguntas y variantes de los seeds.

    Que una pregunta de la whitelist dispare no es un error por sí solo: varias
    describen urgencias reales ("tengo los labios azules", "se cayó y perdió el
    conocimiento") y para esas el aviso del 131 es la respuesta correcta. Lo que
    este test vigila es que NO dispare en preguntas educativas, que son la
    inmensa mayoría, y que el total se mantenga acotado: si un cambio en las
    frases empieza a capturar consultas normales, el número se dispara y el
    test falla."""
    disparos = [texto for _, texto in _todas_las_preguntas() if detectar_bandera_roja(texto)]
    total = sum(1 for _ in _todas_las_preguntas())

    assert total > 500, "el barrido debería cubrir toda la whitelist"
    assert len(disparos) < total * 0.03, (
        f"{len(disparos)} de {total} preguntas de la whitelist disparan la bandera "
        f"roja; revisar si alguna es educativa: {disparos[:10]}"
    )


@pytest.mark.parametrize("educativa", [
    "¿Cuándo debo ir a urgencias por la tos o dificultad para respirar?",
    "¿Cuándo debo llamar al 131 por una caída?",
    "¿Qué es la infección urinaria?",
])
def test_preguntas_educativas_de_la_whitelist_conservan_su_respuesta(educativa):
    """Estas hablan de urgencias pero son consultas informativas: deben llegar a
    su respuesta validada, no al aviso de emergencia."""
    assert not detectar_bandera_roja(educativa)


# ── En el flujo real ─────────────────────────────────────────────────────────

def test_el_dolor_de_pecho_ya_no_recibe_la_respuesta_de_infeccion_urinaria(bot):
    """La regresión concreta que motivó todo: con el índice real cargado,
    "me duele mucho el pecho" quedaba a 0.215 de la variante "me duele al
    orinar" y la whitelist entregaba la respuesta de ITU."""
    resultado = bot.preguntar("me duele mucho el pecho")

    assert "131" in resultado["respuesta"]
    assert "urinaria" not in resultado["respuesta"].lower()
    assert bot.llamadas == [], "una emergencia no debe depender de que Groq responda"


def test_la_emergencia_corta_antes_que_todo_lo_demas(bot):
    """Va antes de la whitelist, del caché y del LLM: si Groq está caído, el
    resto del flujo contesta "espere un momento", que ante un infarto es
    inaceptable."""
    resultado = bot.preguntar("mi esposo se desmayo y no despierta")

    assert resultado["respuesta"].startswith("Lo que me cuenta puede ser una emergencia")
    assert bot.llamadas == []


def test_una_consulta_normal_sigue_su_curso(bot):
    """Contrapeso: la capa de emergencias no debe interceptar el uso corriente."""
    resultado = bot.preguntar("¿qué es la neumonía?")

    assert "131" not in resultado["respuesta"] or "emergencia" not in resultado["respuesta"]
