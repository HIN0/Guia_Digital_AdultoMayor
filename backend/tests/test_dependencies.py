"""Tests de core/dependencies.py: extracción de usuario desde el JWT y
la restricción de rol admin. Se prueban tanto llamando las funciones
directamente como a través de los endpoints reales que las usan.

Ejecutar desde backend/:  python -m pytest tests/test_dependencies.py -v
"""

import pytest
from fastapi import HTTPException

from core.dependencies import get_usuario_actual, get_usuario_opcional, requiere_admin
from modules.auth.entity import RolUsuario

# ── get_usuario_actual (unitario) ───────────────────────────────────────────

def test_get_usuario_actual_header_sin_bearer_lanza_401(db_session):
    with pytest.raises(HTTPException) as exc:
        get_usuario_actual(authorization="Token abc123", db=db_session)
    assert exc.value.status_code == 401


def test_get_usuario_actual_token_invalido_lanza_401(db_session):
    with pytest.raises(HTTPException) as exc:
        get_usuario_actual(authorization="Bearer token-basura", db=db_session)
    assert exc.value.status_code == 401


def test_get_usuario_actual_token_valido_usuario_inexistente_lanza_401(db_session):
    from core.security import create_access_token

    # Token válido "en forma" pero para un usuario_id que nunca se guardó en la BD.
    token = create_access_token({"sub": "999", "rol": "alumno"})

    with pytest.raises(HTTPException) as exc:
        get_usuario_actual(authorization=f"Bearer {token}", db=db_session)
    assert exc.value.status_code == 401


def test_get_usuario_actual_token_valido_retorna_usuario(db_session, crear_usuario, token_para):
    usuario = crear_usuario()
    token = token_para(usuario)

    resultado = get_usuario_actual(authorization=f"Bearer {token}", db=db_session)

    assert resultado.id == usuario.id
    assert resultado.email == usuario.email


# ── get_usuario_opcional (unitario) ─────────────────────────────────────────

def test_get_usuario_opcional_sin_header_retorna_none(db_session):
    assert get_usuario_opcional(authorization=None, db=db_session) is None


def test_get_usuario_opcional_token_invalido_retorna_none(db_session):
    assert get_usuario_opcional(authorization="Bearer basura", db=db_session) is None


def test_get_usuario_opcional_token_valido_retorna_usuario(db_session, crear_usuario, token_para):
    usuario = crear_usuario()
    token = token_para(usuario)

    resultado = get_usuario_opcional(authorization=f"Bearer {token}", db=db_session)

    assert resultado is not None
    assert resultado.id == usuario.id


# ── requiere_admin (unitario) ────────────────────────────────────────────────

def test_requiere_admin_con_alumno_lanza_403(db_session, crear_usuario):
    alumno = crear_usuario(rol=RolUsuario.alumno)
    with pytest.raises(HTTPException) as exc:
        requiere_admin(usuario=alumno)
    assert exc.value.status_code == 403


def test_requiere_admin_con_admin_retorna_usuario(db_session, crear_usuario):
    admin = crear_usuario(google_id="g-admin", email="admin@example.com", rol=RolUsuario.admin)
    resultado = requiere_admin(usuario=admin)
    assert resultado.id == admin.id


# ── A través de un endpoint real protegido (GET /api/auth/me) ──────────────

def test_endpoint_protegido_sin_header_retorna_422(client):
    """authorization: str = Header(...) es obligatorio a nivel de FastAPI:
    si falta, ni siquiera se ejecuta el cuerpo del endpoint."""
    response = client.get("/api/auth/me")
    assert response.status_code == 422


def test_endpoint_protegido_con_token_valido_retorna_usuario(client, crear_usuario, token_para):
    usuario = crear_usuario(email="bearer@example.com")
    token = token_para(usuario)

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["email"] == "bearer@example.com"


def test_endpoint_protegido_con_token_malformado_retorna_401(client):
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer no-es-un-jwt"})
    assert response.status_code == 401
