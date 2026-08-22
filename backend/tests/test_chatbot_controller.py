"""Tests de contrato del controller del chatbot.

/chatbot/preguntar es el endpoint más caro del sistema (llama a Groq) y el que
más protecciones tiene: autenticación, el gate del Módulo 2 y rate limiting.
Ninguna estaba cubierta.

El servicio se reemplaza por un doble, así que estos tests no cargan FAISS ni
llaman a Groq: verifican el contrato HTTP, no la calidad de las respuestas.

Ejecutar desde backend/:  python -m pytest tests/test_chatbot_controller.py -v
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from modules.auth.entity import RolUsuario


@pytest.fixture()
def app_chatbot(db_session, monkeypatch):
    """App con los routers de auth y chatbot, con generar_y_guardar_respuesta
    sustituido para no tocar FAISS ni Groq."""
    from modules.auth.controller import router as auth_router
    from modules.chatbot import controller as chatbot_controller

    llamadas = []

    def _servicio_doble(db, usuario_id, pregunta, conversacion_id=None):
        llamadas.append(pregunta)
        return {"respuesta": "Respuesta de prueba.", "conversacion_id": 1, "mensaje_id": 1}

    monkeypatch.setattr(chatbot_controller, "generar_y_guardar_respuesta", _servicio_doble)
    monkeypatch.setattr(chatbot_controller, "chatbot_esta_desbloqueado", lambda db, uid: True)

    app = FastAPI()
    app.include_router(auth_router, prefix="/api")
    app.include_router(chatbot_controller.router, prefix="/api")

    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    app.state.llamadas = llamadas
    return app


@pytest.fixture()
def client_chatbot(app_chatbot):
    with TestClient(app_chatbot) as test_client:
        yield test_client


@pytest.fixture()
def auth(crear_usuario, token_para):
    """Cabeceras de un alumno y de un admin."""
    def _headers(rol=RolUsuario.alumno, email="alumno@example.com", google_id="g-1"):
        usuario = crear_usuario(google_id=google_id, email=email, rol=rol)
        return usuario, {"Authorization": f"Bearer {token_para(usuario)}"}

    return _headers


# ── Autenticación y gate del Módulo 2 ────────────────────────────────────────

def test_preguntar_requiere_autenticacion(client_chatbot):
    respuesta = client_chatbot.post("/api/chatbot/preguntar", json={"pregunta": "hola"})
    assert respuesta.status_code in (401, 403, 422)


def test_preguntar_exige_haber_completado_el_modulo_2(client_chatbot, app_chatbot, auth):
    from modules.chatbot import controller as chatbot_controller

    chatbot_controller.chatbot_esta_desbloqueado = lambda db, uid: False
    _, headers = auth()

    respuesta = client_chatbot.post(
        "/api/chatbot/preguntar", json={"pregunta": "hola"}, headers=headers
    )

    assert respuesta.status_code == 403
    assert "Módulo 2" in respuesta.json()["detail"]
    assert app_chatbot.state.llamadas == [], "no debería haber llegado al servicio"


def test_preguntar_responde_con_el_modulo_2_completo(client_chatbot, auth):
    _, headers = auth()

    respuesta = client_chatbot.post(
        "/api/chatbot/preguntar", json={"pregunta": "¿qué es la neumonía?"}, headers=headers
    )

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["respuesta"] == "Respuesta de prueba."
    assert cuerpo["conversacion_id"] == 1
    assert cuerpo["mensaje_id"] == 1


# ── Validación de la entrada ─────────────────────────────────────────────────

@pytest.mark.parametrize("pregunta", ["", "x" * 501])
def test_preguntar_rechaza_preguntas_invalidas(client_chatbot, auth, pregunta):
    """min_length=1 y max_length=500 en ChatRequest: sin el tope, una pregunta
    enorme se convierte en un prompt enorme y en cuota de Groq quemada."""
    _, headers = auth()

    respuesta = client_chatbot.post(
        "/api/chatbot/preguntar", json={"pregunta": pregunta}, headers=headers
    )

    assert respuesta.status_code == 422


# ── Rate limiting ────────────────────────────────────────────────────────────

def test_preguntar_bloquea_despues_del_limite(client_chatbot, auth):
    """@limiter.limit("15/minute"): la petición 16 debe dar 429."""
    _, headers = auth()

    codigos = [
        client_chatbot.post(
            "/api/chatbot/preguntar", json={"pregunta": "hola"}, headers=headers
        ).status_code
        for _ in range(16)
    ]

    assert codigos[:15] == [200] * 15
    assert codigos[15] == 429


def test_el_limite_es_por_sesion(client_chatbot, auth):
    """Dos usuarios distintos no comparten el contador: en un club de adultos
    mayores todos salen por la misma IP."""
    _, headers_a = auth(email="a@example.com", google_id="g-a")
    _, headers_b = auth(email="b@example.com", google_id="g-b")

    for _ in range(15):
        client_chatbot.post("/api/chatbot/preguntar", json={"pregunta": "hola"}, headers=headers_a)

    agotado = client_chatbot.post(
        "/api/chatbot/preguntar", json={"pregunta": "hola"}, headers=headers_a
    )
    otro = client_chatbot.post(
        "/api/chatbot/preguntar", json={"pregunta": "hola"}, headers=headers_b
    )

    assert agotado.status_code == 429
    assert otro.status_code == 200


# ── Errores del servicio ─────────────────────────────────────────────────────

def test_un_error_del_servicio_devuelve_503(client_chatbot, auth):
    """El usuario nunca debe ver un 500 ni una traza."""
    from modules.chatbot import controller as chatbot_controller

    def _explota(**kwargs):
        raise RuntimeError("Groq caído")

    chatbot_controller.generar_y_guardar_respuesta = _explota
    _, headers = auth()

    respuesta = client_chatbot.post(
        "/api/chatbot/preguntar", json={"pregunta": "hola"}, headers=headers
    )

    assert respuesta.status_code == 503
    assert "no está disponible" in respuesta.json()["detail"]


# ── Valoración ───────────────────────────────────────────────────────────────

def test_no_se_pueden_valorar_mensajes_de_otro_usuario(client_chatbot, auth, db_session):
    from modules.chatbot import repository as repo

    dueño, _ = auth(email="dueno@example.com", google_id="g-d")
    _, headers_intruso = auth(email="intruso@example.com", google_id="g-i")

    conversacion = repo.obtener_o_crear_conversacion(db_session, dueño.id)
    mensaje = repo.guardar_mensaje(db_session, conversacion.id, tipo="bot", contenido="hola")

    respuesta = client_chatbot.post(
        "/api/chatbot/valorar",
        json={"mensaje_id": mensaje.id, "valoracion": "negativa"},
        headers=headers_intruso,
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == {"ok": False}


def test_valoracion_invalida_es_rechazada(client_chatbot, auth):
    _, headers = auth()

    respuesta = client_chatbot.post(
        "/api/chatbot/valorar",
        json={"mensaje_id": 1, "valoracion": "excelente"},
        headers=headers,
    )

    assert respuesta.status_code == 422


# ── Endpoints admin ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("ruta", [
    "/api/chatbot/admin/resumen",
    "/api/chatbot/admin/revision",
    "/api/chatbot/admin/preguntas",
])
def test_los_endpoints_admin_rechazan_a_un_alumno(client_chatbot, auth, ruta):
    _, headers = auth()

    respuesta = client_chatbot.get(ruta, headers=headers)

    assert respuesta.status_code == 403


def test_resumen_cuenta_lo_que_paso(client_chatbot, auth, db_session):
    from modules.chatbot import repository as repo

    usuario, _ = auth(email="u@example.com", google_id="g-u")
    _, headers_admin = auth(rol=RolUsuario.admin, email="admin@example.com", google_id="g-adm")

    conversacion = repo.obtener_o_crear_conversacion(db_session, usuario.id)
    repo.guardar_mensaje(db_session, conversacion.id, tipo="usuario", contenido="¿qué es la gripe?")
    repo.guardar_mensaje(db_session, conversacion.id, tipo="fallback", contenido="No tengo esa información.")
    repo.guardar_mensaje(db_session, conversacion.id, tipo="usuario", contenido="me duele el pecho")
    repo.guardar_mensaje(db_session, conversacion.id, tipo="emergencia", contenido="Llame al 131.")

    resumen = client_chatbot.get("/api/chatbot/admin/resumen", headers=headers_admin).json()

    assert resumen["preguntas"] == 2
    assert resumen["fallbacks"] == 1
    assert resumen["emergencias"] == 1


def test_la_revision_trae_la_pregunta_que_provoco_el_fallback(client_chatbot, auth, db_session):
    """Es el dato que hace útil la vista: sin la pregunta, saber que hubo un
    fallback no sirve para ampliar la whitelist."""
    from modules.chatbot import repository as repo

    usuario, _ = auth(email="u2@example.com", google_id="g-u2")
    _, headers_admin = auth(rol=RolUsuario.admin, email="admin2@example.com", google_id="g-adm2")

    conversacion = repo.obtener_o_crear_conversacion(db_session, usuario.id)
    repo.guardar_mensaje(db_session, conversacion.id, tipo="usuario", contenido="¿me sirve el jengibre?")
    repo.guardar_mensaje(db_session, conversacion.id, tipo="fallback", contenido="No tengo esa información.")

    items = client_chatbot.get("/api/chatbot/admin/revision", headers=headers_admin).json()

    assert len(items) == 1
    assert items[0]["motivo"] == "fallback"
    assert items[0]["pregunta"] == "¿me sirve el jengibre?"


def test_la_revision_incluye_las_valoraciones_negativas(client_chatbot, auth, db_session):
    from modules.chatbot import repository as repo

    usuario, headers = auth(email="u3@example.com", google_id="g-u3")
    _, headers_admin = auth(rol=RolUsuario.admin, email="admin3@example.com", google_id="g-adm3")

    conversacion = repo.obtener_o_crear_conversacion(db_session, usuario.id)
    repo.guardar_mensaje(db_session, conversacion.id, tipo="usuario", contenido="¿cuánto dura la tos?")
    mensaje = repo.guardar_mensaje(db_session, conversacion.id, tipo="bot", contenido="Depende.")

    client_chatbot.post(
        "/api/chatbot/valorar",
        json={"mensaje_id": mensaje.id, "valoracion": "negativa"},
        headers=headers,
    )
    items = client_chatbot.get("/api/chatbot/admin/revision", headers=headers_admin).json()

    assert [i["motivo"] for i in items] == ["valoracion_negativa"]
    assert items[0]["pregunta"] == "¿cuánto dura la tos?"
