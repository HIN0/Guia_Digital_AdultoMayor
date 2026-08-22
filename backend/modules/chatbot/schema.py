from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime


# ── Esquemas de chat (usuario) ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    pregunta: str = Field(..., min_length=1, max_length=500)
    conversacion_id: Optional[int] = None

    @field_validator("pregunta")
    @classmethod
    def _no_puede_ser_solo_espacios(cls, valor: str) -> str:
        """min_length=1 dejaba pasar " " o un salto de línea: el mensaje en
        blanco se guardaba, gastaba una llamada a Groq y ensuciaba el panel de
        revisión."""
        if not valor.strip():
            raise ValueError("La pregunta no puede estar vacía")
        return valor

class ChatResponse(BaseModel):
    respuesta: str
    conversacion_id: int
    mensaje_id: int
    # Permite al frontend destacar una emergencia (aviso del 131) en vez de
    # pintarla como una respuesta cualquiera.
    tipo: Literal["bot", "fallback", "emergencia"] = "bot"


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


# ── Esquemas de revisión de calidad (admin) ──────────────────────────────────

class ResumenChatbotOut(BaseModel):
    preguntas: int
    respuestas: int
    fallbacks: int
    emergencias: int
    valoraciones_positivas: int
    valoraciones_negativas: int

class RevisionItemOut(BaseModel):
    mensaje_id: int
    conversacion_id: int
    fecha: datetime
    motivo: Literal["fallback", "valoracion_negativa"]
    pregunta: str
    respuesta: str
    # Secciones del conocimiento usadas; vacío si la respuesta no vino del LLM.
    secciones: List[str] = []


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
