"""Tests de integración de los endpoints /api/progreso a través del
TestClient real (routing + dependencias + servicio + repositorio).

Ejecutar desde backend/:  python -m pytest tests/test_progreso_controller.py -v
"""



def _headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_post_leccion_sin_autenticacion_devuelve_422(client):
    response = client.post("/api/progreso/leccion", json={"leccion_id": 1})
    assert response.status_code == 422


def test_post_leccion_marca_completada(client, crear_usuario, token_para, crear_estructura_modulo):
    usuario = crear_usuario()
    token = token_para(usuario)
    leccion = crear_estructura_modulo(orden=1)["lecciones"][0]

    response = client.post(
        "/api/progreso/leccion", json={"leccion_id": leccion.id}, headers=_headers(token)
    )

    assert response.status_code == 200
    body = response.json()
    assert body["leccion_id"] == leccion.id
    assert body["completada"] is True


def test_post_leccion_de_modulo_bloqueado_devuelve_403(client, crear_usuario, token_para, crear_estructura_modulo):
    usuario = crear_usuario()
    token = token_para(usuario)
    crear_estructura_modulo(orden=1, con_quiz=True, quiz_bloqueante=True, minimo_aciertos=1)
    mod2 = crear_estructura_modulo(orden=2, requiere_modulo_previo=True)

    response = client.post(
        "/api/progreso/leccion", json={"leccion_id": mod2["lecciones"][0].id}, headers=_headers(token)
    )

    assert response.status_code == 403


def test_post_leccion_inexistente_devuelve_404(client, crear_usuario, token_para):
    usuario = crear_usuario()
    token = token_para(usuario)

    response = client.post("/api/progreso/leccion", json={"leccion_id": 99999}, headers=_headers(token))

    assert response.status_code == 404


def test_post_quiz_respuestas_correctas_devuelve_aprobado(client, crear_usuario, token_para, crear_estructura_modulo):
    usuario = crear_usuario()
    token = token_para(usuario)
    estructura = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1)

    response = client.post(
        "/api/progreso/quiz",
        json={
            "quiz_id": estructura["quiz"].id,
            "respuestas": [{
                "pregunta_id": estructura["pregunta"].id,
                "opcion_id": estructura["opcion_correcta"].id,
            }],
        },
        headers=_headers(token),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["aprobado"] is True
    assert body["puntaje"] == 1


def test_get_progreso_sin_autenticacion_devuelve_default(client):
    response = client.get("/api/progreso/")

    assert response.status_code == 200
    body = response.json()
    assert body["chatbot_desbloqueado"] is False
    assert body["modulos"][0]["desbloqueado"] is True


def test_get_progreso_con_autenticacion_devuelve_resumen_real(client, crear_usuario, token_para, crear_estructura_modulo):
    usuario = crear_usuario()
    token = token_para(usuario)
    leccion = crear_estructura_modulo(orden=1)["lecciones"][0]

    client.post("/api/progreso/leccion", json={"leccion_id": leccion.id}, headers=_headers(token))
    response = client.get("/api/progreso/", headers=_headers(token))

    assert response.status_code == 200
    body = response.json()
    assert body["lecciones_completadas"] == [leccion.id]
