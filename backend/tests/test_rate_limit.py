"""Tests del rate limiting (slowapi) en endpoints sensibles: /auth/login y
/auth/refresh. Confirma que el decorador realmente está activo (no solo
declarado) y que el límite es por sesión/IP, no global.

Ejecutar desde backend/:  python -m pytest tests/test_rate_limit.py -v
"""

from unittest.mock import patch

_DATOS_GOOGLE = {"google_id": "google-rl", "email": "rl@example.com", "nombre": "RL"}


def test_login_bloquea_despues_del_limite(client):
    """@limiter.limit("10/minute") en /auth/login: la petición 11 debe dar 429."""
    with patch("modules.auth.service.verify_google_token") as mock_verify:
        mock_verify.return_value = _DATOS_GOOGLE
        respuestas = [
            client.post("/api/auth/login", json={"google_token": "t"})
            for _ in range(11)
        ]

    codigos = [r.status_code for r in respuestas]
    assert codigos[:10] == [200] * 10
    assert codigos[10] == 429


def test_refresh_bloquea_despues_del_limite(client, crear_usuario, token_para):
    """@limiter.limit("20/minute") en /auth/refresh, keyed por el propio token."""
    usuario = crear_usuario()
    token = token_para(usuario)
    headers = {"Authorization": f"Bearer {token}"}

    respuestas = [client.post("/api/auth/refresh", headers=headers) for _ in range(21)]

    codigos = [r.status_code for r in respuestas]
    assert codigos[:20] == [200] * 20
    assert codigos[20] == 429


def test_rate_limit_es_por_sesion_no_global(client, crear_usuario, token_para):
    """Dos usuarios con tokens distintos no comparten el mismo contador."""
    usuario_a = crear_usuario(google_id="a", email="a@example.com")
    usuario_b = crear_usuario(google_id="b", email="b@example.com")
    headers_a = {"Authorization": f"Bearer {token_para(usuario_a)}"}
    headers_b = {"Authorization": f"Bearer {token_para(usuario_b)}"}

    for _ in range(20):
        assert client.post("/api/auth/refresh", headers=headers_a).status_code == 200

    # El usuario B no debería verse afectado por el consumo del usuario A.
    assert client.post("/api/auth/refresh", headers=headers_b).status_code == 200
