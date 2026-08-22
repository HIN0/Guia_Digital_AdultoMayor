import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_usuario_actual, requiere_admin
from core.rate_limit import limiter
from modules.auth.entity import Usuario
from modules.progreso.service import chatbot_esta_desbloqueado

from . import repository as repo
from .schema import (
    ChatRequest,
    ChatResponse,
    ConversacionOut,
    FeedbackRequest,
    FeedbackResponse,
    MensajeOut,
    PatologiaCreate,
    PatologiaOut,
    PreguntaChatbotCreate,
    PreguntaChatbotOut,
    PreguntaChatbotUpdate,
    ResumenChatbotOut,
    RevisionItemOut,
)
from .service import (
    cargar_preguntas_validadas,
    generar_y_guardar_respuesta,
    inicializar_base_conocimiento,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


# ── Endpoint de usuario ──────────────────────────────────────────────────────

@router.post("/preguntar", response_model=ChatResponse)
@limiter.limit("15/minute")
def hacer_pregunta(
    request: Request,
    body: ChatRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_actual),
):
    if not chatbot_esta_desbloqueado(db, usuario.id):
        raise HTTPException(
            status_code=403,
            detail="Debes completar el Módulo 2 para acceder al asistente.",
        )
    try:
        resultado = generar_y_guardar_respuesta(
            db=db,
            usuario_id=usuario.id,
            pregunta=body.pregunta,
            conversacion_id=body.conversacion_id,
        )
        return resultado
    except Exception:
        logger.exception("Error en /chatbot/preguntar (usuario_id=%s)", usuario.id)
        raise HTTPException(
            status_code=503,
            detail="El asistente no está disponible en este momento. Por favor intente de nuevo en unos minutos.",
        )


# ── Valoración de mensajes ───────────────────────────────────────────────────

@router.post("/valorar", response_model=FeedbackResponse)
@limiter.limit("30/minute")
def valorar_mensaje(
    request: Request,
    body: FeedbackRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_actual),
):
    ok = repo.valorar_mensaje(db, body.mensaje_id, usuario.id, body.valoracion)
    return {"ok": ok}


# ── Historial de conversaciones ──────────────────────────────────────────────

@router.get("/conversaciones", response_model=list[ConversacionOut])
@limiter.limit("60/minute")
def listar_conversaciones(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_actual),
):
    return repo.listar_conversaciones(db, usuario.id)


@router.get("/conversaciones/{conversacion_id}/mensajes", response_model=list[MensajeOut])
@limiter.limit("60/minute")
def obtener_mensajes(
    request: Request,
    conversacion_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_actual),
):
    mensajes = repo.obtener_mensajes_conversacion(db, conversacion_id, usuario.id)
    if mensajes is None:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    return mensajes


# ── Endpoints admin — Revisión de calidad ────────────────────────────────────

@router.get("/admin/resumen", response_model=ResumenChatbotOut)
def resumen_chatbot(
    db: Session = Depends(get_db),
    _: Usuario = Depends(requiere_admin),
):
    """Cómo se está portando el bot: cuántas preguntas contestó, cuántas cayeron
    en fallback y cómo las valoraron los usuarios."""
    return repo.resumen_chatbot(db)


@router.get("/admin/revision", response_model=list[RevisionItemOut])
def listar_para_revision(
    limite: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: Usuario = Depends(requiere_admin),
):
    """Preguntas que el bot no supo responder o cuya respuesta fue valorada
    negativamente. Es el insumo para decidir qué agregar a la whitelist."""
    return repo.listar_para_revision(db, limite=limite)


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
    try:
        cargar_preguntas_validadas()
        return {"detail": "Whitelist recargada correctamente"}
    except Exception:
        logger.exception("Error recargando whitelist")
        raise HTTPException(status_code=500, detail="No se pudo recargar la whitelist")


@router.post("/admin/recargar-conocimiento", status_code=200)
def recargar_conocimiento(_: Usuario = Depends(requiere_admin)):
    """Reconstruye el índice FAISS desde conocimiento.txt. Sin esto había que
    reiniciar el backend para que un cambio en el archivo tuviera efecto."""
    try:
        inicializar_base_conocimiento()
        return {"detail": "Base de conocimiento recargada correctamente"}
    except Exception:
        logger.exception("Error recargando la base de conocimiento")
        raise HTTPException(
            status_code=500, detail="No se pudo recargar la base de conocimiento"
        )
