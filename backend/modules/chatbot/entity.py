from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.database import Base


def _ahora() -> datetime:
    """datetime.utcnow() está deprecado desde Python 3.12. Se guarda naive en
    UTC para no cambiar el tipo de la columna ni los datos ya existentes."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Patologia(Base):
    __tablename__ = "patologia"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    validada = Column(Boolean, default=False)

    preguntas = relationship("PreguntaChatbot", back_populates="patologia")


class PreguntaChatbot(Base):
    __tablename__ = "pregunta_chatbot"

    id = Column(Integer, primary_key=True, index=True)
    patologia_id = Column(Integer, ForeignKey("patologia.id"), nullable=False)
    texto_pregunta = Column(String, nullable=False)
    respuesta_validada = Column(Text, nullable=False)
    variantes = Column(JSON, default=list)
    activa = Column(Boolean, default=True)

    patologia = relationship("Patologia", back_populates="preguntas")


class Conversacion(Base):
    __tablename__ = "conversacion"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False, index=True)
    fecha_inicio = Column(DateTime, default=_ahora)

    mensajes = relationship("MensajeChat", back_populates="conversacion", cascade="all, delete-orphan")


class MensajeChat(Base):
    __tablename__ = "mensaje_chat"

    id = Column(Integer, primary_key=True, index=True)
    conversacion_id = Column(Integer, ForeignKey("conversacion.id"), nullable=False, index=True)
    pregunta_chatbot_id = Column(Integer, ForeignKey("pregunta_chatbot.id"), nullable=True)
    tipo = Column(String, nullable=False)  # 'usuario', 'bot', 'fallback', 'emergencia'
    contenido = Column(Text, nullable=False)
    valoracion = Column(String, nullable=True)  # 'positiva', 'negativa', null
    # Secciones del conocimiento con las que se generó la respuesta. Sin esto,
    # cuando alguien marca 👎 no hay forma de auditar con qué contexto
    # respondió el bot. Solo se llena en las respuestas del LLM.
    secciones = Column(JSON, nullable=True)
    fecha = Column(DateTime, default=_ahora)

    conversacion = relationship("Conversacion", back_populates="mensajes")
