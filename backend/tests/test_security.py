"""Tests de core/security.py: emisión/validación de JWT propios y
verificación del id_token de Google (mockeada, sin red).

Ejecutar desde backend/:  python -m pytest tests/test_security.py -v
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.config import settings
from core.security import create_access_token, decode_token, verify_google_token

# ── JWT propio (create_access_token / decode_token) ────────────────────────

def test_create_and_decode_access_token_roundtrip():
    token = create_access_token({"sub": "42", "rol": "alumno"})
    payload = decode_token(token)
    assert payload["sub"] == "42"
    assert payload["rol"] == "alumno"
    assert "exp" in payload


def test_decode_token_token_invalido_lanza_value_error():
    with pytest.raises(ValueError):
        decode_token("esto-no-es-un-jwt-valido")


def test_decode_token_firma_alterada_lanza_value_error():
    token = create_access_token({"sub": "1"})
    # Alterar el último carácter de la firma para invalidar el token.
    alterado = token[:-1] + ("A" if token[-1] != "A" else "B")
    with pytest.raises(ValueError):
        decode_token(alterado)


def test_decode_token_expirado_lanza_value_error(monkeypatch):
    monkeypatch.setattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", -1)
    token = create_access_token({"sub": "1"})
    with pytest.raises(ValueError):
        decode_token(token)


# ── Verificación de Google (verify_google_token) ────────────────────────────

def _fake_google_response(status_code=200, data=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = data or {}
    return resp


def _run(coro):
    return asyncio.run(coro)


@patch("core.security.httpx.AsyncClient")
def test_verify_google_token_exitoso(mock_async_client_cls):
    data = {"sub": "google-999", "email": "user@example.com", "name": "User", "aud": settings.GOOGLE_CLIENT_ID}
    mock_client = AsyncMock()
    mock_client.get.return_value = _fake_google_response(200, data)
    mock_async_client_cls.return_value.__aenter__.return_value = mock_client

    resultado = _run(verify_google_token("un-id-token"))

    assert resultado == {
        "google_id": "google-999",
        "email": "user@example.com",
        "nombre": "User",
    }


@patch("core.security.httpx.AsyncClient")
def test_verify_google_token_status_no_200_lanza_value_error(mock_async_client_cls):
    mock_client = AsyncMock()
    mock_client.get.return_value = _fake_google_response(400, {})
    mock_async_client_cls.return_value.__aenter__.return_value = mock_client

    with pytest.raises(ValueError):
        _run(verify_google_token("token-invalido"))


@patch("core.security.httpx.AsyncClient")
def test_verify_google_token_aud_no_coincide_lanza_value_error(mock_async_client_cls):
    data = {"sub": "google-999", "email": "user@example.com", "name": "User", "aud": "otra-app-distinta"}
    mock_client = AsyncMock()
    mock_client.get.return_value = _fake_google_response(200, data)
    mock_async_client_cls.return_value.__aenter__.return_value = mock_client

    with pytest.raises(ValueError):
        _run(verify_google_token("token-de-otra-app"))


@patch("core.security.httpx.AsyncClient")
def test_verify_google_token_sin_nombre_usa_string_vacio(mock_async_client_cls):
    data = {"sub": "google-1", "email": "sinnombre@example.com", "aud": settings.GOOGLE_CLIENT_ID}
    mock_client = AsyncMock()
    mock_client.get.return_value = _fake_google_response(200, data)
    mock_async_client_cls.return_value.__aenter__.return_value = mock_client

    resultado = _run(verify_google_token("token"))

    assert resultado["nombre"] == ""
