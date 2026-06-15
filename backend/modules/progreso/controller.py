"""
Definición de endpoints HTTP y enrutamiento.
Gestiona la recepción de peticiones web y la inyección de dependencias.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
# from core.dependencies import get_usuario_actual
from . import schema, service

router = APIRouter(prefix="/progreso", tags=["Progreso"])

@router.post("/leccion", response_model=schema.LeccionCompletadaResponse)
def registrar_avance_leccion(
    progreso: schema.ProgresoLeccionCreate, 
    db: Session = Depends(get_db)
):
    """Endpoint para que el frontend notifique la finalización de una lección."""
    # TODO: Reemplazar con Depends(get_usuario_actual) tras integrar el módulo Auth
    usuario_id_simulado = 1 
    
    return service.procesar_leccion_completada(db, usuario_id_simulado, progreso)

@router.post("/quiz", response_model=schema.ResultadoQuizResponse)
def enviar_respuestas_quiz(
    submit: schema.SubmitQuizCreate,
    db: Session = Depends(get_db)
):
    """Recibe las respuestas del quiz final, valida en BD y devuelve resultado con feedback."""
    usuario_id_simulado = 1
    return service.procesar_intento_quiz(db, usuario_id_simulado, submit)

@router.get("/", response_model=schema.ResumenProgresoResponse)
def consultar_estado_progreso(
    db: Session = Depends(get_db)
):
    """Endpoint para recuperar todo el progreso, lecciones e insignias del usuario."""
    # TODO: Reemplazar con Depends(get_usuario_actual) tras integrar el módulo Auth
    usuario_id_simulado = 1
    
    return service.obtener_resumen_usuario(db, usuario_id_simulado)