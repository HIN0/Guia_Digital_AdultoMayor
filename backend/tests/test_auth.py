"""Tests del módulo auth: repository, service (login con Google) y los
endpoints de /api/auth.

Ejecutar desde backend/:  python -m pytest tests/test_auth.py -v
"""

from unittest.mock import patch

import pytest

from modules.auth import repository, service
from modules.auth.entity import RolUsuario

# ── repository ───────────────────────────────────────────────────────────

def test_crear_usuario_lo_persiste(db_session):
    usuario = repository.crear_usuario(db_session, google_id="g1", email="a@a.com", nombre="A")
    assert usuario.id is not None
    assert usuario.rol == RolUsuario.alumno  # valor por defecto de la entidad


def test_get_usuario_by_google_id_encontrado_y_no_encontrado(db_session):
    repository.crear_usuario(db_session, google_id="g1", email="a@a.com", nombre="A")

    assert repository.get_usuario_by_google_id(db_session, "g1") is not None
    assert repository.get_usuario_by_google_id(db_session, "no-existe") is None


def test_get_usuario_by_id_encontrado_y_no_encontrado(db_session):
    creado = repository.crear_usuario(db_session, google_id="g1", email="a@a.com", nombre="A")

    assert repository.get_usuario_by_id(db_session, creado.id).email == "a@a.com"
    assert repository.get_usuario_by_id(db_session, 99999) is None


# ── service.login_con_google ────────────────────────────────────────────────

_DATOS_GOOGLE = {"google_id": "google-42", "email": "nueva@example.com", "nombre": "Nueva Persona"}


@pytest.mark.anyio
async def test_login_con_google_crea_usuario_nuevo(db_session):
    with patch("modules.auth.service.verify_google_token") as mock_verify:
        mock_verify.return_value = _DATOS_GOOGLE
        access_token, usuario = await service.login_con_google(db_session, "id-token-google")

    assert usuario.email == "nueva@example.com"
    assert usuario.google_id == "google-42"
    assert access_token  # no vacío

    # Debe haber quedado persistido en la BD.
    assert repository.get_usuario_by_google_id(db_session, "google-42") is not None


@pytest.mark.anyio
async def test_login_con_google_usuario_existente_no_duplica(db_session):
    repository.crear_usuario(db_session, google_id="google-42", email="nueva@example.com", nombre="Nueva Persona")

    with patch("modules.auth.service.verify_google_token") as mock_verify:
        mock_verify.return_value = _DATOS_GOOGLE
        _, usuario = await service.login_con_google(db_session, "id-token-google")

    todos = db_session.query(repository.Usuario).filter(repository.Usuario.google_id == "google-42").all()
    assert len(todos) == 1
    assert usuario.id == todos[0].id


@pytest.mark.anyio
async def test_login_con_google_token_invalido_propaga_value_error(db_session):
    with patch("modules.auth.service.verify_google_token") as mock_verify:
        mock_verify.side_effect = ValueError("Token de Google inválido")
        with pytest.raises(ValueError):
            await service.login_con_google(db_session, "token-malo")


@pytest.mark.anyio
async def test_login_con_google_token_incluye_id_y_rol_del_usuario(db_session):
    with patch("modules.auth.service.verify_google_token") as mock_verify:
        mock_verify.return_value = _DATOS_GOOGLE
        access_token, usuario = await service.login_con_google(db_session, "id-token-google")

    from core.security import decode_token
    payload = decode_token(access_token)
    assert payload["sub"] == str(usuario.id)
    assert payload["rol"] == "alumno"


# ── service.get_usuario_actual (helper interno, sin uso en los endpoints) ──

def test_service_get_usuario_actual_encontrado(db_session):
    creado = repository.crear_usuario(db_session, google_id="g1", email="a@a.com", nombre="A")
    assert service.get_usuario_actual(db_session, creado.id).id == creado.id


def test_service_get_usuario_actual_no_encontrado_lanza_value_error(db_session):
    with pytest.raises(ValueError):
        service.get_usuario_actual(db_session, 99999)


# ── controller: POST /api/auth/login ────────────────────────────────────────

def test_endpoint_login_exitoso_devuelve_token_y_usuario(client):
    with patch("modules.auth.service.verify_google_token") as mock_verify:
        mock_verify.return_value = _DATOS_GOOGLE
        response = client.post("/api/auth/login", json={"google_token": "id-token-de-google"})

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["usuario"]["email"] == "nueva@example.com"
    assert "access_token" in body


def test_endpoint_login_token_google_invalido_devuelve_401(client):
    with patch("modules.auth.service.verify_google_token") as mock_verify:
        mock_verify.side_effect = ValueError("Token de Google inválido")
        response = client.post("/api/auth/login", json={"google_token": "token-malo"})

    assert response.status_code == 401


def test_endpoint_login_sin_body_devuelve_422(client):
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 422


def test_endpoint_login_luego_me_con_el_token_recibido(client):
    with patch("modules.auth.service.verify_google_token") as mock_verify:
        mock_verify.return_value = _DATOS_GOOGLE
        login_resp = client.post("/api/auth/login", json={"google_token": "id-token-de-google"})

    token = login_resp.json()["access_token"]
    me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "nueva@example.com"
