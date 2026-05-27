"""
Capa de reglas de negocio.
Coordina la lógica de evaluación, asignación de insignias y desbloqueos.
"""
from sqlalchemy.orm import Session
from . import repository, schema

def procesar_leccion_completada(db: Session, usuario_id: int, progreso: schema.ProgresoLeccionCreate):
    # 1. Registrar el avance en base de datos
    registro = repository.registrar_leccion(db, usuario_id, progreso)
    
    # 2. Obtener historial para validación de reglas
    lecciones_completadas = repository.obtener_lecciones_usuario(db, usuario_id)
    
    # 3. REGLA 1: Insignia "Primeros Pasos" (al completar la 1ra lección)
    if len(lecciones_completadas) == 1:
        # Busca la insignia en la BD (asumiendo que tiene ID 1)
        insignia_base = db.query(repository.Insignia).filter(repository.Insignia.nombre == "Primeros Pasos").first()
        
        if insignia_base:
            # Verifica si el usuario ya la tiene para no duplicarla
            ya_obtenida = db.query(repository.InsigniaObtenida).filter(
                repository.InsigniaObtenida.usuario_id == usuario_id,
                repository.InsigniaObtenida.insignia_id == insignia_base.id
            ).first()
            
            if not ya_obtenida:
                nueva_insignia = repository.InsigniaObtenida(
                    usuario_id=usuario_id,
                    insignia_id=insignia_base.id
                )
                db.add(nueva_insignia)
                db.commit()
        
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