"""Detección determinística de banderas rojas (síntomas de emergencia).

Se evalúa ANTES de la whitelist y del LLM, y a propósito NO usa embeddings: el
match semántico falla justo aquí. Medido con el índice real del proyecto,
"me duele mucho el pecho" quedaba a 0.215 de la variante "me duele al orinar" y
recibía la respuesta de infección urinaria; "creo que me está dando un infarto"
quedaba a 0.402 de "tengo ciática". El modelo de embeddings es pequeño y
multilingüe, y pesa más el patrón "me duele mucho el ___" que la parte del
cuerpo. Con una lista de frases el comportamiento es exacto y auditable.

Los síntomas provienen de fuentes oficiales del Ministerio de Salud de Chile:

  - Infarto agudo al miocardio (IAM) — Salud Responde, MINSAL
    https://saludresponde.minsal.cl/iam/
    Síntomas frecuentes: dolor o presión en el pecho; dolor irradiado a brazo,
    hombro, cuello, mandíbula o espalda; sudor frío; náuseas; dificultad para
    respirar; mareos o sensación de desmayo. La página advierte que en adultos
    mayores, mujeres y personas con diabetes el infarto puede ser "silente":
    falta de aire repentina, fatiga extrema, mareos o desmayos SIN dolor de
    pecho — lo que es especialmente relevante para esta plataforma. Conducta
    indicada: llamar de inmediato al 131 (SAMU) o acudir a urgencias, mantener
    reposo, informar la hora de inicio de los síntomas y no manejar.

  - Ataque cerebrovascular (ACV) — MINSAL
    https://www.minsal.cl/ataque_cerebral_sintomas/
    El 90% de quienes sufren un ACV presenta de forma súbita al menos uno de
    estos tres signos: asimetría facial con un lado caído; incapacidad de
    mantener ambos brazos extendidos a la misma altura (un brazo débil o
    entumecido); incapacidad de hablar con claridad. Conducta indicada: acudir
    de inmediato al servicio de urgencia más cercano.

IMPORTANTE: el texto de MENSAJE_EMERGENCIA y la lista de frases deben ser
revisados y validados por la contraparte de salud del HUAP antes de producción.
Este módulo es la mecánica; el contenido clínico es de ellos.
"""

from .normalizacion import normalizar_texto

MENSAJE_EMERGENCIA = (
    "Lo que me cuenta puede ser una emergencia. No espere: llame ahora al 131 "
    "(SAMU, la ambulancia). La llamada es gratuita y atiende las 24 horas. "
    "Si prefiere, vaya al servicio de urgencia más cercano.\n\n"
    "Mientras llega la ayuda: quédese en reposo y no maneje. Si hay alguien "
    "cerca, pídale que lo acompañe. Cuando llame, cuente a qué hora "
    "empezaron los síntomas.\n\n"
    "Yo solo entrego información general y no puedo atender emergencias."
)

# Frases en primera persona o de quien acompaña, no formulaciones informativas.
# "dificultad para respirar", por ejemplo, quedó fuera a propósito: aparece en
# preguntas educativas de la whitelist ("¿Cuándo debo ir a urgencias por la tos
# o dificultad para respirar?") que merecen su respuesta validada, no el aviso
# de emergencia.
_FRASES_EMERGENCIA = (
    # Cardíaco (IAM)
    "me duele el pecho",
    "me duele mucho el pecho",
    "dolor en el pecho",
    "dolor al pecho",
    "duele el pecho",
    "presion en el pecho",
    "opresion en el pecho",
    "aprieta el pecho",
    "apretado en el pecho",
    "peso en el pecho",
    # "me arde el pecho" estaba aquí y se quitó: MINSAL describe el infarto como
    # dolor o PRESIÓN, no como ardor, y el ardor retroesternal después de comer
    # es la forma típica del reflujo. Con la frase incluida, "ando con acidez y
    # me arde el pecho después de comer" recibía el aviso del 131. Sobre-avisar
    # tampoco es gratis: un bot que grita urgencia por una acidez enseña a la
    # persona a no hacerle caso cuando la urgencia sea de verdad.
    "infarto",
    "ataque al corazon",
    "ataque cardiaco",
    "paro cardiaco",
    # Respiratorio
    "no puedo respirar",
    "no puede respirar",
    "me cuesta respirar",
    "le cuesta respirar",
    "me falta el aire",
    "le falta el aire",
    "me estoy ahogando",
    "se esta ahogando",
    "labios morados",
    "labios azules",
    # Ataque cerebrovascular (ACV)
    "no puedo hablar",
    "no puede hablar",
    "se me traba la lengua",
    "se le traba la lengua",
    "no se le entiende",
    "cara caida",
    "boca torcida",
    "un lado de la cara",
    "medio cuerpo",
    "un lado del cuerpo",
    "se me durmio el brazo",
    "se me durmio la cara",
    "no puedo mover el brazo",
    "no puede mover el brazo",
    "no puedo mover la pierna",
    # Conciencia
    "se desmayo",
    "me desmaye",
    "no despierta",
    "no reacciona",
    "perdio el conocimiento",
    "esta inconsciente",
    "quedo inconsciente",
    # Sangrado
    "no para de sangrar",
    "sangrado que no para",
    "vomito con sangre",
    "vomitando sangre",
    # Emergencia declarada
    "es una emergencia",
    "me estoy muriendo",
    "se esta muriendo",
)

# Una pregunta puramente definitoria no es una urgencia en curso: "¿qué es un
# infarto?" merece información, no el aviso del 131. Solo se descarta cuando la
# pregunta EMPIEZA así; "¿qué hago si me duele el pecho?" sí es una urgencia.
_PREFIJOS_INFORMATIVOS = (
    "que es",
    "que son",
    "que significa",
    "como se previene",
    "como prevenir",
    "como evitar",
    "por que se produce",
    "por que da",
    "cuales son los sintomas",
)

# Construcciones que hablan del síntoma como posibilidad o consecuencia, no como
# algo que está ocurriendo. Ajustadas contra la batería completa de la whitelist:
# sin ellas, "la presión alta puede dar infarto" y "dónde consulto si no es una
# emergencia" recibían el aviso del 131. Deliberadamente NO incluyen "puede ser":
# "me duele el pecho, ¿puede ser un infarto?" sí es una urgencia en curso.
_CONTEXTOS_NO_URGENTES = (
    "puede dar",
    "puede causar",
    "puede provocar",
    "puede producir",
    "puede terminar",
    "riesgo de",
    "no es una emergencia",
    "para prevenir",
    "para evitar",
)


def detectar_bandera_roja(pregunta: str) -> bool:
    """True si la pregunta describe una posible emergencia médica en curso."""
    texto = normalizar_texto(pregunta)

    if texto.startswith(_PREFIJOS_INFORMATIVOS):
        return False

    if any(contexto in texto for contexto in _CONTEXTOS_NO_URGENTES):
        return False

    return any(frase in texto for frase in _FRASES_EMERGENCIA)
