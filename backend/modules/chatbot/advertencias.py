"""Advertencia para cuando la persona pide que le identifiquen lo que tiene.

El bot no diagnostica: la regla 2 del prompt se lo prohíbe y, preguntado de
frente ("diagnostíqueme"), responde que no reemplaza al médico. Pero medido con
el flujo real, cuando alguien describe sus síntomas y pregunta qué tiene
—"¿esto que tengo es neumonía?"— recibe la descripción de esa patología SIN
ninguna aclaración. Ninguna respuesta afirma "usted tiene neumonía", así que
técnicamente no hay diagnóstico, pero una persona mayor puede leerlo como un sí.

Esos casos salen por la whitelist, no por el LLM, así que las reglas del prompt
no los alcanzan: la advertencia hay que agregarla en el flujo.

Se AGREGA a la respuesta, no la reemplaza (a diferencia de las banderas rojas,
que sí cortan el flujo): la persona recibe igual la información que pidió. Y se
activa solo ante el patrón acotado de "¿qué tengo?", nunca en toda respuesta: una
advertencia repetida en cada mensaje se vuelve invisible a los tres usos, justo
cuando más importa.

IMPORTANTE: el texto de ADVERTENCIA_DIAGNOSTICO es provisional y debe ser
revisado por la contraparte de salud del HUAP antes de producción.
"""

from .normalizacion import normalizar_texto

ADVERTENCIA_DIAGNOSTICO = (
    "\n\nEso sí: esto es información general y no es un diagnóstico. "
    "Para saber qué tiene usted, la debe examinar un profesional. "
    "Consulte en su CESFAM o con su médico."
)

# Nombres con que la gente llama a las condiciones que cubre el conocimiento.
# Sirven para reconocer "¿tengo neumonía?", que es pedir un diagnóstico aunque
# no use ninguna de las frases genéricas de más abajo.
_CONDICIONES = (
    "neumonia", "pulmonia", "gastroenteritis", "infeccion urinaria", "cistitis",
    "lumbago", "ciatica", "cefalea", "migrana", "jaqueca", "hipertension",
    "presion alta", "infarto", "acv", "fractura",
)

# Formas de pedir que le identifiquen lo que tiene. Ajustadas contra la batería
# completa de la whitelist (~1.000 preguntas y variantes).
_FRASES_PIDE_DIAGNOSTICO = (
    "que tengo",
    "que es lo que tengo",
    "que enfermedad ",
    "que sera",
    "sera que tengo",
    "sera que es",
    "puede ser que tenga",
    "estare con",
    "tendre",
    "me estare enfermando",
    "que me esta pasando",
    "que me pasa",
) + tuple(f"tengo {c}" for c in _CONDICIONES) \
  + tuple(f"es {c}" for c in _CONDICIONES) \
  + tuple(f"sera {c}" for c in _CONDICIONES)

# Casos que contienen las mismas frases sin ser una petición de diagnóstico.
# Todos salieron del barrido sobre la whitelist:
#   - "¿qué tengo QUE hacer?" pregunta por un trámite.
#   - "¿por qué tengo cistitis tan seguido?" pregunta por la causa de algo ya
#     diagnosticado.
#   - "me dijeron que tengo hipertensión" ya viene con diagnóstico médico.
#   - "¿qué será bueno comer?" no habla de una enfermedad.
_NO_ES_DIAGNOSTICO = (
    "que tengo que",
    "que tengo para",
    "por que tengo",
    "me dijeron que tengo",
    "ya me dijeron",
    "que sera bueno",
    "que sera mejor",
    "que enfermedades",
)

# Una pregunta definitoria pide información, no que le identifiquen un síntoma.
_PREFIJOS_DEFINITORIOS = ("que es", "que son", "que significa", "como se previene")


def pide_diagnostico(pregunta: str) -> bool:
    """True si la persona está pidiendo que le identifiquen lo que tiene."""
    texto = normalizar_texto(pregunta)

    if texto.startswith(_PREFIJOS_DEFINITORIOS):
        return False

    if any(frase in texto for frase in _NO_ES_DIAGNOSTICO):
        return False

    return any(frase in texto for frase in _FRASES_PIDE_DIAGNOSTICO)


def con_advertencia(respuesta: str) -> str:
    """Agrega la advertencia si no está ya en el texto (las respuestas validadas
    del equipo de salud a veces la traen)."""
    if "no es un diagnóstico" in respuesta.lower() or "diagnóstico" in respuesta.lower():
        return respuesta
    return respuesta + ADVERTENCIA_DIAGNOSTICO
