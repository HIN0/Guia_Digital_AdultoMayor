"""Tests de modules/progreso/service.py: las reglas de negocio del proyecto
(desbloqueo de módulos, aprobación de quiz, otorgamiento de insignias,
desbloqueo del chatbot). Es el módulo más parecido a "cálculos de negocio"
del proyecto y el que menos cobertura tenía.

Ejecutar desde backend/:  python -m pytest tests/test_progreso_service.py -v
"""

import pytest
from fastapi import HTTPException

from modules.progreso import repository, schema, service

# ── _modulo_desbloqueado / _validar_acceso_modulo (vía procesar_leccion_completada) ──

def test_modulo_sin_requiere_previo_siempre_desbloqueado(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    estructura = crear_estructura_modulo(orden=1, requiere_modulo_previo=False)

    assert service._modulo_desbloqueado(db_session, usuario.id, estructura["modulo"]) is True


def test_modulo_requiere_previo_pero_no_existe_modulo_anterior_queda_desbloqueado(db_session, crear_usuario, crear_estructura_modulo):
    """Edge case de _modulo_desbloqueado: orden=1 con requiere_modulo_previo=True
    pero no hay módulo con orden 0 -> no debe bloquear."""
    usuario = crear_usuario()
    estructura = crear_estructura_modulo(orden=1, requiere_modulo_previo=True)

    assert service._modulo_desbloqueado(db_session, usuario.id, estructura["modulo"]) is True


def test_modulo_previo_con_quiz_bloqueante_no_aprobado_bloquea(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    crear_estructura_modulo(orden=1, con_quiz=True, quiz_bloqueante=True, minimo_aciertos=1)
    mod2 = crear_estructura_modulo(orden=2, requiere_modulo_previo=True)

    assert service._modulo_desbloqueado(db_session, usuario.id, mod2["modulo"]) is False


def test_modulo_previo_con_quiz_bloqueante_aprobado_desbloquea(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    mod1 = crear_estructura_modulo(orden=1, con_quiz=True, quiz_bloqueante=True, minimo_aciertos=1)
    mod2 = crear_estructura_modulo(orden=2, requiere_modulo_previo=True)

    repository.procesar_quiz(db_session, usuario.id, schema.SubmitQuizCreate(
        quiz_id=mod1["quiz"].id,
        respuestas=[schema.RespuestaItem(pregunta_id=mod1["pregunta"].id, opcion_id=mod1["opcion_correcta"].id)],
    ))

    assert service._modulo_desbloqueado(db_session, usuario.id, mod2["modulo"]) is True


def test_modulo_previo_con_quiz_no_bloqueante_siempre_desbloquea(db_session, crear_usuario, crear_estructura_modulo):
    """bloqueante=False: el módulo previo tiene quiz pero no impide el acceso al siguiente."""
    usuario = crear_usuario()
    crear_estructura_modulo(orden=1, con_quiz=True, quiz_bloqueante=False, minimo_aciertos=1)
    mod2 = crear_estructura_modulo(orden=2, requiere_modulo_previo=True)

    assert service._modulo_desbloqueado(db_session, usuario.id, mod2["modulo"]) is True


def test_modulo_previo_sin_quiz_requiere_todas_las_lecciones_completas(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    mod1 = crear_estructura_modulo(orden=1, n_lecciones=2, con_quiz=False)
    mod2 = crear_estructura_modulo(orden=2, requiere_modulo_previo=True)

    # Solo 1 de 2 lecciones completas -> aún bloqueado.
    repository.registrar_leccion(db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=mod1["lecciones"][0].id))
    assert service._modulo_desbloqueado(db_session, usuario.id, mod2["modulo"]) is False

    # Completa la segunda lección -> ahora desbloqueado.
    repository.registrar_leccion(db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=mod1["lecciones"][1].id))
    assert service._modulo_desbloqueado(db_session, usuario.id, mod2["modulo"]) is True


def test_validar_acceso_modulo_bloqueado_lanza_403(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    crear_estructura_modulo(orden=1, con_quiz=True, quiz_bloqueante=True, minimo_aciertos=1)
    mod2 = crear_estructura_modulo(orden=2, requiere_modulo_previo=True)

    with pytest.raises(HTTPException) as exc:
        service._validar_acceso_modulo(db_session, usuario.id, mod2["modulo"])
    assert exc.value.status_code == 403


# ── procesar_leccion_completada ──────────────────────────────────────────

def test_procesar_leccion_completada_leccion_inexistente_lanza_404(db_session, crear_usuario):
    usuario = crear_usuario()
    with pytest.raises(HTTPException) as exc:
        service.procesar_leccion_completada(db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=99999))
    assert exc.value.status_code == 404


def test_procesar_leccion_completada_modulo_bloqueado_lanza_403(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    crear_estructura_modulo(orden=1, con_quiz=True, quiz_bloqueante=True, minimo_aciertos=1)
    mod2 = crear_estructura_modulo(orden=2, requiere_modulo_previo=True)

    with pytest.raises(HTTPException) as exc:
        service.procesar_leccion_completada(db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=mod2["lecciones"][0].id))
    assert exc.value.status_code == 403


def test_procesar_leccion_completada_modulo_3_otorga_insignia(db_session, crear_usuario, crear_estructura_modulo, crear_insignia):
    usuario = crear_usuario()
    crear_insignia("Asistente de IA")  # insignia del módulo 3
    mod3 = crear_estructura_modulo(orden=3, n_lecciones=1)

    resultado = service.procesar_leccion_completada(
        db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=mod3["lecciones"][0].id)
    )

    assert resultado.completada is True
    assert resultado.insignia_otorgada is not None
    assert resultado.insignia_otorgada.nombre == "Asistente de IA"


def test_procesar_leccion_completada_modulo_distinto_de_3_no_otorga_insignia(db_session, crear_usuario, crear_estructura_modulo, crear_insignia):
    usuario = crear_usuario()
    crear_insignia("Conocedor de la IA")
    mod1 = crear_estructura_modulo(orden=1, n_lecciones=1)

    resultado = service.procesar_leccion_completada(
        db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=mod1["lecciones"][0].id)
    )

    assert resultado.insignia_otorgada is None


# ── procesar_intento_quiz ────────────────────────────────────────────────

def test_procesar_intento_quiz_inexistente_lanza_404(db_session, crear_usuario):
    usuario = crear_usuario()
    with pytest.raises(HTTPException) as exc:
        service.procesar_intento_quiz(db_session, usuario.id, schema.SubmitQuizCreate(quiz_id=99999, respuestas=[]))
    assert exc.value.status_code == 404


def test_procesar_intento_quiz_modulo_bloqueado_lanza_403(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    crear_estructura_modulo(orden=1, con_quiz=True, quiz_bloqueante=True, minimo_aciertos=1)
    mod2 = crear_estructura_modulo(orden=2, requiere_modulo_previo=True, con_quiz=True, minimo_aciertos=1)

    with pytest.raises(HTTPException) as exc:
        service.procesar_intento_quiz(db_session, usuario.id, schema.SubmitQuizCreate(quiz_id=mod2["quiz"].id, respuestas=[]))
    assert exc.value.status_code == 403


def test_procesar_intento_quiz_exitoso_delega_al_repository(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    mod1 = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1)

    resultado = service.procesar_intento_quiz(db_session, usuario.id, schema.SubmitQuizCreate(
        quiz_id=mod1["quiz"].id,
        respuestas=[schema.RespuestaItem(pregunta_id=mod1["pregunta"].id, opcion_id=mod1["opcion_correcta"].id)],
    ))

    assert resultado.aprobado is True


# ── chatbot_esta_desbloqueado ─────────────────────────────────────────────

def test_chatbot_bloqueado_si_no_completo_modulo_2_ni_3(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    crear_estructura_modulo(orden=1)
    crear_estructura_modulo(orden=2, con_quiz=True, minimo_aciertos=1)
    crear_estructura_modulo(orden=3, n_lecciones=1)

    assert service.chatbot_esta_desbloqueado(db_session, usuario.id) is False


def test_chatbot_desbloqueado_al_aprobar_quiz_modulo_2(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    mod2 = crear_estructura_modulo(orden=2, con_quiz=True, minimo_aciertos=1)

    repository.procesar_quiz(db_session, usuario.id, schema.SubmitQuizCreate(
        quiz_id=mod2["quiz"].id,
        respuestas=[schema.RespuestaItem(pregunta_id=mod2["pregunta"].id, opcion_id=mod2["opcion_correcta"].id)],
    ))

    assert service.chatbot_esta_desbloqueado(db_session, usuario.id) is True


def test_chatbot_desbloqueado_al_completar_lecciones_modulo_3_sin_quiz(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    mod3 = crear_estructura_modulo(orden=3, n_lecciones=2, con_quiz=False)

    repository.registrar_leccion(db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=mod3["lecciones"][0].id))
    assert service.chatbot_esta_desbloqueado(db_session, usuario.id) is False

    repository.registrar_leccion(db_session, usuario.id, schema.ProgresoLeccionCreate(leccion_id=mod3["lecciones"][1].id))
    assert service.chatbot_esta_desbloqueado(db_session, usuario.id) is True


# ── obtener_resumen_usuario ───────────────────────────────────────────────

def test_obtener_resumen_usuario_estado_inicial(db_session, crear_usuario, crear_estructura_modulo):
    usuario = crear_usuario()
    crear_estructura_modulo(orden=1, n_lecciones=2)

    resumen = service.obtener_resumen_usuario(db_session, usuario.id)

    assert resumen.lecciones_completadas == []
    assert resumen.chatbot_desbloqueado is False
    assert len(resumen.modulos) == 1
    assert resumen.modulos[0].desbloqueado is True
    assert resumen.modulos[0].completado is False


def test_obtener_resumen_usuario_refleja_progreso_y_desbloqueo(db_session, crear_usuario, crear_estructura_modulo, crear_insignia):
    usuario = crear_usuario()
    crear_insignia("Conocedor de la IA")
    mod1 = crear_estructura_modulo(orden=1, con_quiz=True, minimo_aciertos=1, quiz_bloqueante=True)
    mod2 = crear_estructura_modulo(orden=2, requiere_modulo_previo=True, n_lecciones=1)

    # Antes de aprobar el quiz del módulo 1, el módulo 2 está bloqueado.
    resumen = service.obtener_resumen_usuario(db_session, usuario.id)
    estado_mod2 = next(e for e in resumen.modulos if e.modulo_id == mod2["modulo"].id)
    assert estado_mod2.desbloqueado is False

    # Aprueba el quiz del módulo 1.
    service.procesar_intento_quiz(db_session, usuario.id, schema.SubmitQuizCreate(
        quiz_id=mod1["quiz"].id,
        respuestas=[schema.RespuestaItem(pregunta_id=mod1["pregunta"].id, opcion_id=mod1["opcion_correcta"].id)],
    ))

    resumen = service.obtener_resumen_usuario(db_session, usuario.id)
    estado_mod1 = next(e for e in resumen.modulos if e.modulo_id == mod1["modulo"].id)
    estado_mod2 = next(e for e in resumen.modulos if e.modulo_id == mod2["modulo"].id)
    assert estado_mod1.completado is True
    assert estado_mod2.desbloqueado is True
    assert len(resumen.insignias) == 1
