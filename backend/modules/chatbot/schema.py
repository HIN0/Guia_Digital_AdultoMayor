from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

# ── Esquemas de chat (usuario) ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    pregunta: str = Field(..., min_length=1, max_length=500)
    conversacion_id: Optional[int] = None

class ChatResponse(BaseModel):
    respuesta: str
    conversacion_id: int
    mensaje_id: int


# ── Esquemas de valoración (feedback) ───────────────────────────────────────

class FeedbackRequest(BaseModel):
    mensaje_id: int
    valoracion: Literal["positiva", "negativa"]

class FeedbackResponse(BaseModel):
    ok: bool


# ── Esquemas de historial ────────────────────────────────────────────────────

class MensajeOut(BaseModel):
    id: int
    tipo: str
    contenido: str
    valoracion: Optional[str] = None
    fecha: datetime

    class Config:
        from_attributes = True

class ConversacionOut(BaseModel):
    id: int
    fecha_inicio: datetime
    preview: str
    total_mensajes: int

    class Config:
        from_attributes = True


# ── Esquemas de Patologia ────────────────────────────────────────────────────

class PatologiaCreate(BaseModel):
    nombre: str

class PatologiaOut(BaseModel):
    id: int
    nombre: str
    validada: bool

    class Config:
        from_attributes = True


# ── Esquemas de PreguntaChatbot (whitelist) ──────────────────────────────────

class PreguntaChatbotCreate(BaseModel):
    patologia_id: int
    texto_pregunta: str
    respuesta_validada: str
    variantes: Optional[List[str]] = []

class PreguntaChatbotUpdate(BaseModel):
    texto_pregunta: Optional[str] = None
    respuesta_validada: Optional[str] = None
    variantes: Optional[List[str]] = None
    activa: Optional[bool] = None

class PreguntaChatbotOut(BaseModel):
    id: int
    patologia_id: int
    texto_pregunta: str
    respuesta_validada: str
    variantes: List[str]
    activa: bool

    class Config:
        from_attributes = True
