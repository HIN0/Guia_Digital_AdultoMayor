"""Tests de modules/progreso/repository.py: registro de lecciones, corrección
de quizzes y otorgamiento de insignias directamente contra la BD.

Ejecutar desde backend/:  python -m pytest tests/test_progreso_repository.py -v
"""

from modules.progreso import repository, schema

# ── registrar_leccion ────────────────────────────────────────────────────

def test_registrar_leccion_la_persiste(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    estructura = crear_estructura_modulo(orden=1)
    leccion = estructura["lecciones"][0]

    resultado = repository.registrar_leccion(db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=leccion.id))

    assert resultado.completada is True
    assert len(repository.obtener_lecciones_usuario(db_session, usuario.id)) == 1


def test_registrar_leccion_es_idempotente(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    leccion = crear_estructura_modulo(orden=1)["lecciones"][0]
    body = schema.ProgresoLeccionCreate(leccion_id=leccion.id)

    repository.registrar_leccion(db_session, usuario.id, body)
    repository.registrar_leccion(db_session, usuario.id, body)

    assert len(repository.obtener_lecciones_usuario(db_session, usuario.id)) == 1


# ── procesar_quiz ────────────────────────────────────────────────────────

def test_procesar_quiz_todas_correctas_aprueba(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    estructura = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1)
    submit = schema.SubmitQuizCreate(
        quiz_id=estructura["quiz"].id,
        respuestas=[schema.RespuestaItem(
            pregunta_id=estructura["pregunta"].id,
            opcion_id=estructura["opcion_correcta"].id,
        )],
    )

    resultado = repository.procesar_quiz(db_session, usuario.id, submit)

    assert resultado.puntaje == 1
    assert resultado.aprobado is True
    assert resultado.feedbacks[0].es_correcta is True
    assert resultado.feedbacks[0].opcion_correcta_id == estructura["opcion_correcta"].id


def test_procesar_quiz_respuesta_incorrecta_no_aprueba(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    estructura = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1)
    submit = schema.SubmitQuizCreate(
        quiz_id=estructura["quiz"].id,
        respuestas=[schema.RespuestaItem(
            pregunta_id=estructura["pregunta"].id,
            opcion_id=estructura["opcion_incorrecta"].id,
        )],
    )

    resultado = repository.procesar_quiz(db_session, usuario.id, submit)

    assert resultado.puntaje == 0
    assert resultado.aprobado is False
    assert resultado.feedbacks[0].es_correcta is False


def test_procesar_quiz_pregunta_inexistente_se_ignora_sin_contar(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    estructura = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1)
    submit = schema.SubmitQuizCreate(
        quiz_id=estructura["quiz"].id,
        respuestas=[schema.RespuestaItem(pregunta_id=99999, opcion_id=1)],
    )

    resultado = repository.procesar_quiz(db_session, usuario.id, submit)

    assert resultado.puntaje == 0
    assert resultado.feedbacks == []


def test_procesar_quiz_aprobado_otorga_insignia_del_modulo(db_session, crear_usuario, crear_estructura_modulo, crear_insignia):
    usuario = crear_usuario()
    crear_insignia("Conocedor de la IA")  # insignia del módulo 1
    estructura = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1)
    submit = schema.SubmitQuizCreate(
        quiz_id=estructura["quiz"].id,
        respuestas=[schema.RespuestaItem(
            pregunta_id=estructura["pregunta"].id,
            opcion_id=estructura["opcion_correcta"].id,
        )],
    )

    resultado = repository.procesar_quiz(db_session, usuario.id, submit)

    assert resultado.insignia_otorgada is not None
    assert resultado.insignia_otorgada.nombre == "Conocedor de la IA"


def test_procesar_quiz_no_aprobado_no_otorga_insignia(db_session, crear_usuario, crear_estructura_modulo, crear_insignia):
    usuario = crear_usuario()
    crear_insignia("Conocedor de la IA")
    estructura = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1)
    submit = schema.SubmitQuizCreate(
        quiz_id=estructura["quiz"].id,
        respuestas=[schema.RespuestaItem(
            pregunta_id=estructura["pregunta"].id,
            opcion_id=estructura["opcion_incorrecta"].id,
        )],
    )

    resultado = repository.procesar_quiz(db_session, usuario.id, submit)

    assert resultado.insignia_otorgada is None


def test_usuario_aprobo_quiz(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    estructura = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1)

    assert repository.usuario_aprobo_quiz(db_session, usuario.id, estructura["quiz"].id) is False

    submit = schema.SubmitQuizCreate(
        quiz_id=estructura["quiz"].id,
        respuestas=[schema.RespuestaItem(
            pregunta_id=estructura["pregunta"].id,
            opcion_id=estructura["opcion_correcta"].id,
        )],
    )
    repository.procesar_quiz(db_session, usuario.id, submit)

    assert repository.usuario_aprobo_quiz(db_session, usuario.id, estructura["quiz"].id) is True


# ── otorgar_insignia_modulo ──────────────────────────────────────────────

def test_otorgar_insignia_modulo_orden_desconocido_retorna_none(db_session, crear_usuario):
    usuario = crear_usuario()
    assert repository.otorgar_insignia_modulo(db_session, usuario.id, 99) is None


def test_otorgar_insignia_modulo_no_existente_en_bd_retorna_none(db_session, crear_usuario):
    usuario = crear_usuario()
    # orden=1 mapea a "Conocedor de la IA", pero no se sembró en la BD.
    assert repository.otorgar_insignia_modulo(db_session, usuario.id, 1) is None


def test_otorgar_insignia_modulo_no_duplica_si_ya_la_tiene(db_session, crear_usuario, crear_insignia):
    usuario = crear_usuario()
    crear_insignia("Conocedor de la IA")

    primera = repository.otorgar_insignia_modulo(db_session, usuario.id, 1)
    segunda = repository.otorgar_insignia_modulo(db_session, usuario.id, 1)

    assert primera is not None
    assert segunda is None
    assert len(repository.obtener_insignias_usuario(db_session, usuario.id)) == 1


# ── consultas agregadas ──────────────────────────────────────────────────

def test_obtener_lecciones_completadas_de_modulo_filtra_por_modulo(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    mod1 = crear_estructura_modulo(orden=1, n_lecciones=2)
    mod2 = crear_estructura_modulo(orden=2, n_lecciones=1)

    repository.registrar_leccion(db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=mod1["lecciones"][0].id))
    repository.registrar_leccion(db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=mod2["lecciones"][0].id))

    completadas_mod1 = repository.obtener_lecciones_completadas_de_modulo(db_session, usuario.id, mod1["modulo"].id)

    assert completadas_mod1 == [mod1["lecciones"][0].id]


def test_obtener_quizzes_aprobados_solo_incluye_aprobados(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    aprobado = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1)
    reprobado = crear_estructura_modulo(orden=2, con_quiz=True, minimo_aciertos=1)

    repository.procesar_quiz(db_session, usuario.id, schema.SubmitQuizCreate(
        quiz_id=aprobado["quiz"].id,
        respuestas=[schema.RespuestaItem(pregunta_id=aprobado["pregunta"].id, opcion_id=aprobado["opcion_correcta"].id)],
    ))
    repository.procesar_quiz(db_session, usuario.id, schema.SubmitQuizCreate(
        quiz_id=reprobado["quiz"].id,
        respuestas=[schema.RespuestaItem(pregunta_id=reprobado["pregunta"].id, opcion_id=reprobado["opcion_incorrecta"].id)],
    ))

    aprobados = repository.obtener_quizzes_aprobados(db_session, usuario.id)

    assert aprobados == [aprobado["quiz"].id]
