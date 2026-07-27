"""
Capa de reglas de negocio.
Coordina la lógica de evaluación, asignación de insignias y desbloqueos.
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.educacion.entity import Leccion, Modulo, QuizFinal
from . import repository, schema


def _modulo_desbloqueado(db: Session, usuario_id: int, modulo: Modulo) -> bool:
    """Determina si el usuario tiene acceso a este módulo según las reglas de desbloqueo."""
    if not modulo.requiere_modulo_previo:
        return True

    previo = db.query(Modulo).filter(Modulo.orden == modulo.orden - 1).first()
    if not previo:
        return True

    if previo.quiz_final:
        if previo.quiz_final.bloqueante:
            return repository.usuario_aprobo_quiz(db, usuario_id, previo.quiz_final.id)
        return True

    total_lecciones = len(previo.lecciones)
    completadas = repository.obtener_lecciones_completadas_de_modulo(db, usuario_id, previo.id)
    return len(completadas) >= total_lecciones


def _validar_acceso_modulo(db: Session, usuario_id: int, modulo: Modulo):
    """Lanza 403 si el usuario no tiene acceso al módulo."""
    if not _modulo_desbloqueado(db, usuario_id, modulo):
        raise HTTPException(
            status_code=403,
            detail="Debe completar el módulo anterior antes de acceder a este contenido",
        )


def procesar_leccion_completada(db: Session, usuario_id: int, progreso: schema.ProgresoLeccionCreate):
    """
    Registra el avance y evalúa si el usuario cumple los criterios
    para obtener la insignia del Módulo 3 (cuyo progreso viene de la lección, no del quiz final).
    """
    leccion = db.query(Leccion).filter(Leccion.id == progreso.leccion_id).first()
    if not leccion:
        raise HTTPException(status_code=404, detail="Lección no encontrada")

    modulo = db.query(Modulo).filter(Modulo.id == leccion.modulo_id).first()
    if modulo:
        _validar_acceso_modulo(db, usuario_id, modulo)

    repository.registrar_leccion(db, usuario_id, progreso)

    insignia_response = None
    if modulo and modulo.orden == 3:
        insignia_orm = repository.otorgar_insignia_modulo(db, usuario_id, 3)
        if insignia_orm:
            insignia_response = schema.InsigniaResponse.model_validate(insignia_orm)

    return schema.LeccionCompletadaResponse(
        leccion_id=progreso.leccion_id,
        completada=True,
        insignia_otorgada=insignia_response,
    )


def procesar_intento_quiz(db: Session, usuario_id: int, submit: schema.SubmitQuizCreate):
    quiz = db.query(QuizFinal).filter(QuizFinal.id == submit.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")

    modulo = db.query(Modulo).filter(Modulo.id == quiz.modulo_id).first()
    if modulo:
        _validar_acceso_modulo(db, usuario_id, modulo)

    return repository.procesar_quiz(db, usuario_id, submit)


def chatbot_esta_desbloqueado(db: Session, usuario_id: int) -> bool:
    """Verifica en BD si el usuario completó Módulo 2 o Módulo 3."""
    quizzes_aprobados = set(repository.obtener_quizzes_aprobados(db, usuario_id))
    modulos = db.query(Modulo).filter(Modulo.orden.in_([2, 3])).all()
    for modulo in modulos:
        if modulo.quiz_final:
            if modulo.quiz_final.id in quizzes_aprobados:
                return True
        else:
            completadas = set(repository.obtener_lecciones_completadas_de_modulo(
                db, usuario_id, modulo.id
            ))
            if completadas and len(completadas) >= len(modulo.lecciones):
                return True
    return False


def obtener_resumen_usuario(db: Session, usuario_id: int):
    """Compila el estado global del usuario para el dashboard o vistas de perfil."""
    lecciones = repository.obtener_lecciones_usuario(db, usuario_id)
    quizzes = repository.obtener_quizzes_aprobados(db, usuario_id)
    insignias = repository.obtener_insignias_usuario(db, usuario_id)

    all_modulos = db.query(Modulo).order_by(Modulo.orden).all()
    estados = []

    for modulo in all_modulos:
        lecciones_mod = repository.obtener_lecciones_completadas_de_modulo(
            db, usuario_id, modulo.id
        )
        desbloqueado = _modulo_desbloqueado(db, usuario_id, modulo)

        if modulo.quiz_final:
            completado = modulo.quiz_final.id in quizzes
        else:
            completado = len(lecciones_mod) >= len(modulo.lecciones) and len(modulo.lecciones) > 0

        estados.append(schema.EstadoModulo(
            modulo_id=modulo.id,
            orden=modulo.orden,
            desbloqueado=desbloqueado,
            completado=completado,
            lecciones_completadas=lecciones_mod,
        ))

    mod2_completado = any(e.completado and e.orden == 2 for e in estados)
    mod3_completado = any(e.completado and e.orden == 3 for e in estados)
    chatbot_desbloqueado = mod2_completado or mod3_completado

    return schema.ResumenProgresoResponse(
        lecciones_completadas=[l.leccion_id for l in lecciones],
        quizzes_aprobados=quizzes,
        insignias=insignias,
        modulos=estados,
        chatbot_desbloqueado=chatbot_desbloqueado,
    )
