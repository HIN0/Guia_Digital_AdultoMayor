"""
APIRouter: es el objeto que agrupa endpoints. Equivale a un @RestController en Spring. Luego main.py lo registra en la app
Depends — la inyección de dependencias que ya vimos. Le dice a FastAPI "ejecuta esta función y pásame el resultado"
HTTPException — la forma de devolver errores HTTP (404, 401, 403, etc.) al frontend
"""
from fastapi import APIRouter, Depends, HTTPException

"""
Session para tipar db, y get_db es la función que crea y cierra la conexión a la base de datos.
Va siempre dentro de Depends(get_db).
"""
from sqlalchemy.orm import Session  # noqa: E402

from core.database import get_db  # noqa: E402

"""
Se importa el service para llamar la lógica de negocio, y los schemas para decirle a FastAPI
qué forma tiene el JSON de respuesta.
"""
from modules.educacion import service  # noqa: E402
from modules.educacion.schema import (  # noqa: E402
    LeccionResponse,
    ModuloDetalleResponse,
    ModuloResponse,
)

"""
- prefix="/educacion": todas las rutas de este archivo van a empezar con /educacion. Entonces
cuando escribes @router.get("/modulos"), la URL completa queda /educacion/modulos.
Y como en main.py se registra con /api, la URL final es /api/educacion/modulos
- tags=["Educación"]: solo sirve para organizar la documentación en /docs.
Agrupa todos estos endpoints bajo el título "Educación"
"""
router = APIRouter(prefix="/educacion", tags=["Educación"])


"""
- @router.get("/modulos"): el decorador que convierte esta función en un endpoint. get es el método HTTP.
La URL es /api/educacion/modulos.
- response_model=list[ModuloResponse] — le dice a FastAPI que la respuesta debe tener la forma de una
lista de ModuloResponse. FastAPI automáticamente filtra el objeto que devuelves para que solo incluya
los campos definidos en ese schema. Si tu objeto Modulo tuviera un campo interno que no quieres exponer,
aquí se cortaría.
- db: Session = Depends(get_db) — FastAPI ejecuta get_db() antes de tu función, obtiene la sesión de base
de datos, y la pasa como db. Nunca se crea la sesión manualmente.
- El docstring Lista todos los módulos en orden. aparece como descripción del endpoint en /docs.
Es buena práctica ponerlo.
Este endpoint es simple: no puede fallar (una lista vacía sigue siendo válida), así que no necesita
 try/except.
"""

@router.get("/modulos", response_model=list[ModuloResponse])
def listar_modulos(db: Session = Depends(get_db)):
    """Lista todos los módulos en orden."""
    return service.listar_modulos(db)


@router.get("/modulos/{modulo_id}", response_model=ModuloDetalleResponse)
def detalle_modulo(modulo_id: int, db: Session = Depends(get_db)):
    """Devuelve un módulo con sus lecciones y su quiz."""
    try:
        return service.obtener_modulo_detalle(db, modulo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/lecciones/{leccion_id}", response_model=LeccionResponse)
def detalle_leccion(leccion_id: int, db: Session = Depends(get_db)):
    """Devuelve el contenido de una lección específica."""
    try:
        return service.obtener_leccion(db, leccion_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
