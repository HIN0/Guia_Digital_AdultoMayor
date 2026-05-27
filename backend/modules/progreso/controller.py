"""
Definición de endpoints HTTP y enrutamiento.
Gestiona la recepción de peticiones web y la inyección de dependencias.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from . import schema, service

router = APIRouter(prefix="/progreso", tags=["Progreso"])

# Mock de la dependencia para aislar el módulo hasta que Auth esté finalizado
def get_usuario_actual_mock():
    class UsuarioMock:
        id = 1
    return UsuarioMock()

@router.post("/leccion")
def registrar_avance_leccion(
    progreso: schema.ProgresoLeccionCreate, 
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_actual_mock) # Inyección temporal simulada
):
    return service.procesar_leccion_completada(db, usuario.id, progreso)

@router.get("/", response_model=schema.ResumenProgresoResponse)
def consultar_estado_progreso(
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_actual_mock) # Inyección temporal simulada
):
    return service.obtener_resumen_usuario(db, usuario.id)