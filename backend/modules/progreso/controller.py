"""
Definición de endpoints HTTP y enrutamiento.
Gestiona la recepción de peticiones web y la inyección de dependencias.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_usuario_actual, get_usuario_opcional
from modules.auth.entity import Usuario

from . import schema, service

router = APIRouter(prefix="/progreso", tags=["Progreso"])


@router.post("/leccion", response_model=schema.LeccionCompletadaResponse)
def registrar_avance_leccion(
    progreso: schema.ProgresoLeccionCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_actual),
):
    """Endpoint para que el frontend notifique la finalización de una lección."""
    return service.procesar_leccion_completada(db, usuario.id, progreso)


@router.post("/quiz", response_model=schema.ResultadoQuizResponse)
def enviar_respuestas_quiz(
    submit: schema.SubmitQuizCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_actual),
):
    """Recibe las respuestas del quiz final, valida en BD y devuelve resultado con feedback."""
    return service.procesar_intento_quiz(db, usuario.id, submit)


@router.get("/", response_model=schema.ResumenProgresoResponse)
def consultar_estado_progreso(
    db: Session = Depends(get_db),
    usuario: Usuario | None = Depends(get_usuario_opcional),
):
    """Endpoint para recuperar todo el progreso, lecciones e insignias del usuario."""
    if not usuario:
        return schema.ResumenProgresoResponse(
            lecciones_completadas=[],
            quizzes_aprobados=[],
            insignias=[],
            modulos=[schema.EstadoModulo(
                modulo_id=0, orden=1, desbloqueado=True,
                completado=False, lecciones_completadas=[],
            )],
            chatbot_desbloqueado=False,
        )
    return service.obtener_resumen_usuario(db, usuario.id)
