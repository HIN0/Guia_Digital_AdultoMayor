"""
Capa de reglas de negocio.
Coordina la lógica de evaluación, asignación de insignias y desbloqueos.
"""
from sqlalchemy.orm import Session
from . import repository, schema

def procesar_leccion_completada(db: Session, usuario_id: int, progreso: schema.ProgresoLeccionCreate):
    """
    Registra el avance y evalúa si el usuario cumple los criterios 
    para obtener una nueva insignia o desbloquear contenido.
    """
    registro = repository.registrar_leccion(db, usuario_id, progreso)
    
    lecciones_completadas = repository.obtener_lecciones_usuario(db, usuario_id)
    
    # TODO: Implementar motor de reglas para insignias según el Sprint 2
    if len(lecciones_completadas) == 1:
        pass 
        
    return registro

def obtener_resumen_usuario(db: Session, usuario_id: int):
    """Compila el estado global del usuario para el dashboard o vistas de perfil."""
    lecciones = repository.obtener_lecciones_usuario(db, usuario_id)
    insignias = repository.obtener_insignias_usuario(db, usuario_id)
    
    return schema.ResumenProgresoResponse(
        lecciones_completadas=[l.leccion_id for l in lecciones],
        quizzes_aprobados=[], # TODO: Integrar con repository.obtener_quizzes_usuario
        insignias=insignias
    )