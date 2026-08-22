"""Tests de conversación encadenada (multi-turno).

Cubren el problema que test_whitelist.py no puede ver: cuando la pregunta es un
seguimiento ("¿y cuánto dura?"), su texto no menciona ningún tema, y buscarlo
literalmente aterriza en otra patología. Medido antes del arreglo, con el índice
real: tras una conversación sobre neumonía, "¿y cuánto dura?" recuperaba la
sección de hipertensión; "¿y es grave?" la de infección urinaria; y "¿y en los
adultos mayores?" sobre lumbago recibía en duro la respuesta de caídas.

Todo corre offline: usa los embeddings y los índices FAISS reales, sobre SQLite
en memoria y con el LLM reemplazado por un doble. Nunca llama a Groq.

Ejecutar desde backend/:  python -m pytest tests/test_conversacion_multiturno.py -v
"""

from dataclasses import dataclass

import pytest


@dataclass
class _Mensaje:
    """Mínimo que necesita _tema_de_conversacion de un MensajeChat."""

    tipo: str
    contenido: str


def _conversacion(*turnos) -> list:
    """Historial a partir de pares (pregunta_usuario, respuesta_bot)."""
    mensajes = []
    for pregunta, respuesta in turnos:
        mensajes.append(_Mensaje("usuario", pregunta))
        if respuesta is not None:
            mensajes.append(_Mensaje("bot", respuesta))
    return mensajes


def _secciones_recuperadas(service, pregunta: str, tema: str = None) -> list[str]:
    """Encabezados de los chunks que se le entregan al LLM."""
    return [doc.page_content.splitlines()[0] for doc in service._recuperar(pregunta, tema)]


# ── Detección del tema ───────────────────────────────────────────────────────

def test_tema_se_detecta_desde_la_pregunta_del_usuario(service_configurado):
    tema = service_configurado._tema_de_conversacion(
        _conversacion(("¿Qué es la neumonía?", "La neumonía es una infección del pulmón."))
    )
    assert tema and "NEUMONÍA" in tema, f"tema detectado: {tema}"


def test_el_fallback_del_bot_no_contamina_el_tema(service_configurado):
    """El mensaje de fallback nombra todos los temas a la vez ("presión alta,
    caídas, dolor de cabeza..."). Si la detección mirara los mensajes del bot,
    cualquier conversación terminaría con el tema equivocado."""
    historial = _conversacion(
        ("¿Qué es la infección urinaria?", service_configurado.MENSAJE_SIN_INFORMACION)
    )
    tema = service_configurado._tema_de_conversacion(historial)
    assert tema and "URINARIA" in tema, f"tema detectado: {tema}"


def test_tema_none_cuando_no_hay_del_que_hablar(service_configurado):
    assert service_configurado._tema_de_conversacion([]) is None
    assert service_configurado._tema_de_conversacion(_conversacion(("hola", None))) is None


@pytest.mark.parametrize("mensaje, esperado", [
    # El caso reportado: buscando solo por embeddings, el "síntomas" del título
    # de sección pesaba más que el nombre de la enfermedad y esto caía en
    # GASTROENTERITIS — Síntomas (0.740).
    ("sintomas de la neumonia", "NEUMONÍA"),
    ("sintomas de neumonia", "NEUMONÍA"),
    # Un solo vecino era frágil: el chunk más cercano a esto era una sección de
    # CEFALEA ("¿Es por la presión alta?").
    ("tengo la presion alta", "HIPERTENSIÓN"),
    # Sin nombrar el tema, decide la votación entre los 5 más cercanos.
    ("tengo diarrea", "GASTROENTERITIS"),
    ("me duele la espalda baja", "LUMBAGO"),
])
def test_el_tema_se_detecta_aunque_el_embedding_se_confunda(
    service_configurado, mensaje, esperado
):
    tema = service_configurado._tema_de_texto(mensaje)

    assert tema and esperado in tema, f"'{mensaje}' detectó: {tema}"


def test_la_whitelist_no_responde_cuando_las_dos_busquedas_discrepan(service_configurado):
    """Regresión del caso reportado: en una conversación sobre neumonía,
    "flemas y la fiebre ¿cuánto duran?" matcheaba "tos con flema y fiebre" con
    la pregunta cruda (0.420, correcta) y "fiebre con ardor al orinar" con la
    contextualizada (0.401, de infección urinaria), y se entregaba en duro la de
    infección urinaria. Si discrepan, el caso es del LLM."""
    historial = _conversacion(("sintomas de la neumonia", "La neumonía es una infección..."))
    tema = service_configurado._tema_de_conversacion(historial)
    seguimiento = "flemas y la fiebre cuanto duran?"
    consulta = service_configurado._contextualizar(seguimiento, tema)

    _, respuesta = service_configurado._buscar_en_whitelist(seguimiento, consulta)

    assert respuesta is None or "orinar" not in respuesta.lower(), (
        f"respondió con contenido urinario en una conversación de neumonía: {respuesta}"
    )


def test_gana_el_tema_mas_reciente(service_configurado):
    tema = service_configurado._tema_de_conversacion(
        _conversacion(
            ("¿Qué es la neumonía?", "Es una infección del pulmón."),
            ("¿Qué es el lumbago?", "Es un dolor en la espalda baja."),
        )
    )
    assert tema and "LUMBAGO" in tema, f"tema detectado: {tema}"


# ── Recuperación en seguimientos ─────────────────────────────────────────────

@pytest.mark.parametrize(
    "pregunta_previa, seguimiento, seccion_esperada",
    [
        ("¿Qué es la neumonía?", "y cuanto dura?", "NEUMONÍA"),
        ("¿Qué es la neumonía?", "y es grave?", "NEUMONÍA"),
        ("¿Qué es la infección urinaria?", "y eso duele?", "URINARIA"),
        ("¿Qué es el lumbago?", "y en los adultos mayores?", "LUMBAGO"),
        ("¿Cuándo es peligroso el dolor de cabeza?", "cuando tengo que ir a urgencias?", "CEFALEA"),
    ],
)
def test_el_seguimiento_recupera_la_seccion_del_tema(
    service_configurado, pregunta_previa, seguimiento, seccion_esperada
):
    historial = _conversacion((pregunta_previa, "..."))
    tema = service_configurado._tema_de_conversacion(historial)

    secciones = _secciones_recuperadas(service_configurado, seguimiento, tema)
    assert any(seccion_esperada in s for s in secciones), (
        f"'{seguimiento}' tras '{pregunta_previa}' recuperó {secciones}, "
        f"ninguna de {seccion_esperada}"
    )


def test_cambiar_de_tema_no_queda_pegado_al_anterior(service_configurado):
    """El tema acota la búsqueda sin secuestrar la conversación: _recuperar
    también busca sin filtro, así que un cambio de tema encuentra el nuevo."""
    historial = _conversacion(("¿Qué es la neumonía?", "Es una infección del pulmón."))
    tema = service_configurado._tema_de_conversacion(historial)

    secciones = _secciones_recuperadas(
        service_configurado, "ahora cuenteme de la presion alta", tema
    )
    assert any("HIPERTENSIÓN" in s for s in secciones), f"recuperó {secciones}"


def test_un_seguimiento_que_nombra_otro_tema_recupera_ese_tema(service_configurado):
    """Medido: tras hablar de gastroenteritis, "¿y en la neumonía es igual?" con
    el tema antepuesto a la consulta traía tres secciones de gastroenteritis y
    ninguna de neumonía, y el bot contestaba el fallback pese a tener la
    respuesta. Por eso _recuperar busca además sin filtro de tema."""
    historial = _conversacion(("¿Cuánto dura la gastroenteritis?", "Entre 2 y 5 días."))
    tema = service_configurado._tema_de_conversacion(historial)

    secciones = _secciones_recuperadas(service_configurado, "y en la neumonia es igual?", tema)

    assert any("NEUMONÍA" in s for s in secciones), f"recuperó {secciones}"


def test_el_seguimiento_encuentra_la_seccion_que_responde(service_configurado):
    """No basta con acertar la patología: hay que traer la sección concreta.
    Anteponiendo el tema a la consulta, "¿y cuánto dura?" sobre neumonía no
    traía "Recuperación" —donde dice que la tos "puede durar varias semanas"—
    ni entre los 8 primeros resultados. Filtrando por tema sí aparece."""
    historial = _conversacion(("¿Qué es la neumonía?", "Es una infección del pulmón."))
    tema = service_configurado._tema_de_conversacion(historial)

    secciones = _secciones_recuperadas(service_configurado, "y cuanto dura?", tema)

    assert any("Recuperación" in s for s in secciones), f"recuperó {secciones}"


def test_el_primer_turno_recupera_igual_que_antes(service_configurado):
    """Sin tema, _recuperar es la búsqueda de siempre: no se suman chunks extra
    ni crece el prompt en el caso más frecuente."""
    docs = service_configurado._recuperar("¿qué es la neumonía?")

    assert len(docs) == 3, f"se esperaban los 3 chunks del retriever, hubo {len(docs)}"


# ── Whitelist en seguimientos ────────────────────────────────────────────────

def test_la_whitelist_no_responde_de_otro_tema(service_configurado):
    """Regresión: "¿y en los adultos mayores?" queda a 0.351 de una variante de
    caídas, bajo el umbral normal de 0.45. En una conversación sobre lumbago se
    entregaba esa respuesta en duro, sin pasar siquiera por el LLM."""
    historial = _conversacion(("¿Qué es el lumbago?", "Es un dolor en la espalda baja."))
    tema = service_configurado._tema_de_conversacion(historial)
    seguimiento = "y en los adultos mayores?"
    consulta = service_configurado._contextualizar(seguimiento, tema)

    _, respuesta = service_configurado._buscar_en_whitelist(seguimiento, consulta)
    assert respuesta is None or "caída" not in respuesta.lower(), (
        f"respondió con contenido de caídas en una conversación de lumbago: {respuesta}"
    )


@pytest.mark.parametrize("saludo, esperado", [
    ("hola", "Estoy aquí para responder preguntas sobre salud"),
    ("chao", "Hasta pronto"),
    ("gracias", "De nada"),
])
def test_saludos_y_despedidas_funcionan_dentro_de_una_conversacion(
    service_configurado, saludo, esperado
):
    """No dependen del tema: el match exacto normalizado va primero y no se ve
    afectado por el prefijo."""
    tema = "NEUMONÍA ADQUIRIDA EN LA COMUNIDAD"
    consulta = service_configurado._contextualizar(saludo, tema)

    _, respuesta = service_configurado._buscar_en_whitelist(saludo, consulta)
    assert respuesta and esperado in respuesta, f"'{saludo}' respondió: {respuesta}"


def test_la_generica_de_medicamentos_sobrevive_al_seguimiento(service_configurado):
    """Preguntar por remedios es la consulta más sensible del bot y su respuesta
    validada no depende del tema. Como el match es casi literal (0.197), el
    umbral estricto de los seguimientos la deja pasar igual."""
    tema = "HIPERTENSIÓN ARTERIAL (PRESIÓN ALTA)"
    seguimiento = "y que remedio tomo?"
    consulta = service_configurado._contextualizar(seguimiento, tema)

    _, respuesta = service_configurado._buscar_en_whitelist(seguimiento, consulta)
    assert respuesta and "No puedo recomendar medicamentos" in respuesta, (
        f"respondió: {respuesta}"
    )


# ── Guardia de fuera de alcance ──────────────────────────────────────────────

def test_no_se_puede_medir_el_alcance_por_distancia(service_configurado):
    """Por qué se eliminó el corte por "fuera de alcance".

    Existía un umbral de distancia al conocimiento: por encima, se respondía el
    fallback sin gastar una llamada al LLM. Al ampliar el conocimiento a 33
    temas dejó de separar nada, porque ahora se habla de comida, movimiento,
    sueño y seguridad en la casa, y casi cualquier frase cotidiana queda cerca
    de alguna sección.

    Este test mide el solapamiento. Mientras exista, ningún umbral sirve: si
    alguien intenta reponer el corte, esto le muestra por qué no funciona."""
    def distancia(texto):
        return service_configurado._knowledge_store.similarity_search_with_score(texto, k=1)[0][1]

    en_alcance = max(distancia(q) for q in [
        "se me cayo mi mama", "estoy estitico", "que es la epoc",
    ])
    ajena = min(distancia(q) for q in [
        "cual es la mejor receta de tallarines", "que hora es", "como cambio una ampolleta",
    ])

    assert ajena < en_alcance, (
        f"los rangos ya no se solapan (ajena {ajena:.3f} >= en alcance {en_alcance:.3f}); "
        "quizás ahora sí se pueda medir el alcance por distancia, vale la pena revisarlo"
    )


# ── Flujo completo, con el LLM sustituido ────────────────────────────────────

def test_el_seguimiento_llega_al_llm_con_el_tema_de_la_conversacion(bot):
    """La prueba de extremo a extremo del arreglo: en el segundo turno el LLM
    recibe la pregunta tal como la escribió el usuario, y la recuperación se
    acota al tema del que se venía hablando."""
    bot.preguntar("¿Qué es la neumonía?")
    bot.preguntar("y cuanto dura?")

    assert bot.llamadas, "el seguimiento no llegó al LLM"
    ultima = bot.llamadas[-1]
    assert ultima["pregunta"] == "y cuanto dura?", "al LLM se le cambió la pregunta"
    assert ultima["tema"] and "NEUMONÍA" in ultima["tema"], f"tema: {ultima['tema']}"
    assert "Conversación previa" in ultima["historial"]


def test_una_pregunta_ajena_llega_al_llm(bot):
    """Desde que se eliminó el corte por distancia, el filtro de alcance es la
    regla 6 del prompt. Cuesta una llamada a Groq, y a cambio ninguna pregunta
    legítima recibe un fallback sin haber sido evaluada."""
    bot.preguntar("cual es la capital de francia")

    assert len(bot.llamadas) == 1


@pytest.mark.parametrize("consulta", [
    "se me cayo mi mama",   # medía 1.543: el corte por distancia la descartaba
    "estoy estitico",       # medía 1.352
])
def test_una_consulta_de_salud_recibe_respuesta(bot, consulta):
    """El motivo por el que se eliminó el corte por distancia: descartaba
    consultas de temas que el conocimiento sí cubre. No importa si contesta la
    whitelist o el LLM; importa que no reciba un fallback."""
    resultado = bot.preguntar(consulta)

    assert not resultado["respuesta"].startswith("Lo siento, no tengo esa información."), (
        f"'{consulta}' recibió fallback pese a ser un tema cubierto"
    )


def test_una_pregunta_ajena_en_un_seguimiento_la_resuelve_el_llm(bot):
    """Contrapartida deliberada: en un seguimiento no se puede medir el alcance,
    así que el corte queda en manos del LLM (regla 6 del prompt) y sí se gasta
    la llamada."""
    bot.preguntar("¿Qué es la neumonía?")
    bot.preguntar("quien gano el partido de ayer?")

    assert len(bot.llamadas) == 1


# ── El primer turno no cambia ────────────────────────────────────────────────

def test_sin_historial_la_consulta_es_la_pregunta_tal_cual(service_configurado):
    """Sin tema no hay prefijo, así que el camino de un solo turno —el que ya
    cubre test_whitelist.py— queda idéntico."""
    pregunta_simple = "¿que es la neumonia?"
    assert service_configurado._contextualizar(pregunta_simple, None) == pregunta_simple

    pregunta = "cuentame un chiste"
    assert service_configurado._buscar_en_whitelist(pregunta, pregunta) == (None, None)


# ── Cómo se responde "no sé" ─────────────────────────────────────────────────

@pytest.mark.parametrize("texto, es_negativa", [
    ("Lo siento, no tengo esa información. Puedo ayudarle con…", True),
    # El modelo se niega con palabras propias: antes esto se contaba como una
    # respuesta buena, se cacheaba y no aparecía en el panel de revisión.
    ("Lo siento, no puedo ayudar con esa solicitud.", True),
    ("Lo siento, no tengo información sobre eso.", True),
    # Una respuesta larga y útil que menciona "no puedo" NO es una negativa:
    # es la respuesta validada sobre medicamentos.
    ("No puedo recomendar medicamentos ni dosis, porque eso depende de la "
     "situación de cada persona. Tomar remedios por cuenta propia puede ser "
     "riesgoso, sobre todo en personas mayores que ya usan varios fármacos.", False),
    ("La tos y el cansancio pueden durar varias semanas.", False),
])
def test_se_reconoce_una_negativa_aunque_el_modelo_use_sus_palabras(
    service_configurado, texto, es_negativa
):
    assert service_configurado._es_fallback(texto) is es_negativa


def test_el_no_se_nombra_el_tema_de_la_conversacion(service_configurado):
    """Ofrecer la lista completa de temas en medio de una conversación
    desorienta: la persona venía hablando de lumbago y se le respondía "puedo
    ayudarle con presión alta, caídas, dolor de cabeza…"."""
    mensaje = service_configurado._mensaje_sin_informacion("LUMBAGO (DOLOR DE ESPALDA BAJA)")

    assert "lumbago" in mensaje
    assert "presión alta" not in mensaje
    # Conserva la frase centinela, que es como se detecta el fallback.
    assert mensaje.startswith(service_configurado.FRASE_SIN_INFORMACION)


def test_sin_tema_se_ofrece_la_lista_de_grupos(service_configurado):
    """En el primer mensaje no hay tema del que hablar, y ahí sí corresponde
    contarle a la persona de qué puede preguntar."""
    mensaje = service_configurado._mensaje_sin_informacion(None)

    assert mensaje == service_configurado.MENSAJE_SIN_INFORMACION
