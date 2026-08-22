"""Tests del caché de respuestas y del registro de secciones usadas.

Dos cosas que no se ven desde fuera pero afectan al equipo que mantiene el bot:
que corregir el conocimiento tenga efecto inmediato, y que una respuesta mala se
pueda auditar.

Ejecutar desde backend/:  python -m pytest tests/test_cache_y_auditoria.py -v
"""


def test_recargar_el_conocimiento_vacia_el_cache(service_configurado, monkeypatch):
    """Bug corregido: el caché guarda respuestas generadas con el conocimiento
    anterior. Sin vaciarlo, corregir conocimiento.txt y apretar "Recargar" en el
    panel admin no cambiaba nada para las preguntas ya cacheadas — se seguía
    sirviendo la respuesta vieja hasta reiniciar el backend."""
    service_configurado._llm_cache["que es la neumonia"] = ("Respuesta vieja.", [])
    assert service_configurado._llm_cache

    service_configurado.inicializar_base_conocimiento()

    assert service_configurado._llm_cache == {}


def test_la_respuesta_guarda_las_secciones_con_que_se_genero(bot, db_session):
    """Sin esto, una respuesta valorada negativamente en el panel de revisión no
    se puede auditar: no queda registro de con qué contexto respondió el bot."""
    from modules.chatbot.entity import MensajeChat

    resultado = bot.preguntar("la ciatica se cura sola")

    mensaje = db_session.query(MensajeChat).filter(
        MensajeChat.id == resultado["mensaje_id"]
    ).first()
    assert mensaje.secciones, "la respuesta del LLM no registró sus secciones"


def test_las_respuestas_que_no_vienen_del_llm_no_registran_secciones(bot, db_session):
    """Una emergencia o una respuesta validada no se generan desde el
    conocimiento, así que no hay secciones que auditar."""
    from modules.chatbot.entity import MensajeChat

    resultado = bot.preguntar("me duele mucho el pecho")

    mensaje = db_session.query(MensajeChat).filter(
        MensajeChat.id == resultado["mensaje_id"]
    ).first()
    assert mensaje.tipo == "emergencia"
    assert not mensaje.secciones
