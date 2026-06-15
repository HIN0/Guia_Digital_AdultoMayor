"""
Capa de reglas de negocio.
Coordina la lógica de evaluación, asignación de insignias y desbloqueos.
"""
from sqlalchemy.orm import Session
from modules.educacion.entity import Leccion, Modulo
from . import repository, schema

def procesar_leccion_completada(db: Session, usuario_id: int, progreso: schema.ProgresoLeccionCreate):
    """
    Registra el avance y evalúa si el usuario cumple los criterios
    para obtener la insignia del Módulo 3 (cuyo progreso viene de la lección, no del quiz final).
    """
    repository.registrar_leccion(db, usuario_id, progreso)

    insignia_response = None
    leccion = db.query(Leccion).filter(Leccion.id == progreso.leccion_id).first()
    if leccion:
        modulo = db.query(Modulo).filter(Modulo.id == leccion.modulo_id).first()
        # Solo el Módulo 3 no tiene quiz_final: su insignia se otorga al completar la lección
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
    return repository.procesar_quiz(db, usuario_id, submit)

def obtener_resumen_usuario(db: Session, usuario_id: int):
    """Compila el estado global del usuario para el dashboard o vistas de perfil."""
    lecciones = repository.obtener_lecciones_usuario(db, usuario_id)
    insignias = repository.obtener_insignias_usuario(db, usuario_id)

    return schema.ResumenProgresoResponse(
        lecciones_completadas=[l.leccion_id for l in lecciones],
        quizzes_aprobados=[],
        insignias=insignias,
    )
