"""
Igual que antes, Session para tipar el parámetro db. Luego se importa el repository completo
(no funciones sueltas) para llamarlo como repository.get_algo(...), y 
las entidades para usarlas como tipos de retorno.
"""

from sqlalchemy.orm import Session
from modules.educacion import repository
from modules.educacion.entity import Modulo, Leccion


def listar_modulos(db: Session) -> list[Modulo]:
    return repository.get_todos_los_modulos(db)


def obtener_modulo_detalle(db: Session, modulo_id: int) -> Modulo:
    modulo = repository.get_modulo_por_id(db, modulo_id)
    if not modulo:
        raise ValueError("Módulo no encontrado")
    return modulo


def obtener_leccion(db: Session, leccion_id: int) -> Leccion:
    leccion = repository.get_leccion_por_id(db, leccion_id)
    if not leccion:
        raise ValueError("Lección no encontrada")
    return leccion
