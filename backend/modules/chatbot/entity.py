from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.database import Base


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
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    fecha_inicio = Column(DateTime, default=datetime.utcnow)

    mensajes = relationship("MensajeChat", back_populates="conversacion", cascade="all, delete-orphan")


class MensajeChat(Base):
    __tablename__ = "mensaje_chat"

    id = Column(Integer, primary_key=True, index=True)
    conversacion_id = Column(Integer, ForeignKey("conversacion.id"), nullable=False)
    pregunta_chatbot_id = Column(Integer, ForeignKey("pregunta_chatbot.id"), nullable=True)
    tipo = Column(String, nullable=False)  # 'usuario', 'bot', 'fallback'
    contenido = Column(Text, nullable=False)
    valoracion = Column(String, nullable=True)  # 'positiva', 'negativa', null
    fecha = Column(DateTime, default=datetime.utcnow)

    conversacion = relationship("Conversacion", back_populates="mensajes")
