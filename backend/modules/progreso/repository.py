"""
Capa de abstracción de datos.
Aísla todas las transacciones directas (queries) contra la base de datos.
"""
from sqlalchemy.orm import Session
from .entity import ProgresoLeccion, IntentoQuiz, InsigniaObtenida, Insignia
from .schema import ProgresoLeccionCreate, IntentoQuizCreate

def registrar_leccion(db: Session, usuario_id: int, progreso: ProgresoLeccionCreate):
    """Inserta un nuevo registro de lección completada para un usuario."""
    nuevo_progreso = ProgresoLeccion(
        usuario_id=usuario_id, 
        leccion_id=progreso.leccion_id, 
        completada=True
    )
    db.add(nuevo_progreso)
    db.commit()
    db.refresh(nuevo_progreso)
    
    return nuevo_progreso

def obtener_lecciones_usuario(db: Session, usuario_id: int):
    """Retorna todas las lecciones marcadas como completadas por el usuario."""
    return db.query(ProgresoLeccion).filter(
        ProgresoLeccion.usuario_id == usuario_id, 
        ProgresoLeccion.completada == True
    ).all()

def obtener_insignias_usuario(db: Session, usuario_id: int):
    """Ejecuta un JOIN para obtener los detalles de las insignias ganadas por el usuario."""
    return db.query(Insignia).join(InsigniaObtenida).filter(
        InsigniaObtenida.usuario_id == usuario_id
    ).all()