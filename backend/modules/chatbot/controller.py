import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.dependencies import get_usuario_actual, requiere_admin
from modules.auth.entity import Usuario

from .schema import (
    ChatRequest, ChatResponse,
    PreguntaChatbotCreate, PreguntaChatbotUpdate, PreguntaChatbotOut,
    PatologiaCreate, PatologiaOut,
)
from .service import generar_y_guardar_respuesta, cargar_preguntas_validadas
from . import repository as repo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


# ── Endpoint de usuario ──────────────────────────────────────────────────────

@router.post("/preguntar", response_model=ChatResponse)
def hacer_pregunta(
    request: ChatRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_actual),
):
    try:
        resultado = generar_y_guardar_respuesta(
            db=db,
            usuario_id=usuario.id,
            pregunta=request.pregunta,
            conversacion_id=request.conversacion_id,
        )
        return resultado
    except Exception:
        logger.exception("Error en /chatbot/preguntar (usuario_id=%s)", usuario.id)
        raise HTTPException(
            status_code=503,
            detail="El asistente no está disponible en este momento. Por favor intente de nuevo en unos minutos.",
        )


# ── Endpoints admin — Patologías ─────────────────────────────────────────────

@router.get("/admin/patologias", response_model=list[PatologiaOut])
def listar_patologias(
    db: Session = Depends(get_db),
    _: Usuario = Depends(requiere_admin),
):
    return repo.listar_patologias(db)


@router.post("/admin/patologias", response_model=PatologiaOut, status_code=201)
def crear_patologia(
    body: PatologiaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requiere_admin),
):
    return repo.crear_patologia(db, nombre=body.nombre)


# ── Endpoints admin — Preguntas validadas (whitelist) ────────────────────────

@router.get("/admin/preguntas", response_model=list[PreguntaChatbotOut])
def listar_preguntas(
    db: Session = Depends(get_db),
    _: Usuario = Depends(requiere_admin),
):
    return repo.listar_todas_las_preguntas(db)


@router.post("/admin/preguntas", response_model=PreguntaChatbotOut, status_code=201)
def crear_pregunta(
    body: PreguntaChatbotCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requiere_admin),
):
    return repo.crear_pregunta(
        db,
        patologia_id=body.patologia_id,
        texto_pregunta=body.texto_pregunta,
        respuesta_validada=body.respuesta_validada,
        variantes=body.variantes,
    )


@router.patch("/admin/preguntas/{pregunta_id}", response_model=PreguntaChatbotOut)
def actualizar_pregunta(
    pregunta_id: int,
    body: PreguntaChatbotUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requiere_admin),
):
    actualizada = repo.actualizar_pregunta(db, pregunta_id, body.model_dump(exclude_none=True))
    if not actualizada:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return actualizada


@router.delete("/admin/preguntas/{pregunta_id}", status_code=204)
def eliminar_pregunta(
    pregunta_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requiere_admin),
):
    eliminada = repo.eliminar_pregunta(db, pregunta_id)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")


# ── Recarga del índice FAISS de whitelist ────────────────────────────────────

@router.post("/admin/recargar-whitelist", status_code=200)
def recargar_whitelist(_: Usuario = Depends(requiere_admin)):
    """Reconstruye el índice FAISS de preguntas validadas desde la BD."""
    try:
        cargar_preguntas_validadas()
        return {"detail": "Whitelist recargada correctamente"}
    except Exception:
        logger.exception("Error recargando whitelist")
        raise HTTPException(status_code=500, detail="No se pudo recargar la whitelist")
