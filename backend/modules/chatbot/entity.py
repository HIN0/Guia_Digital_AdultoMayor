from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

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
    tipo = Column(String, nullable=False) # Valores esperados: 'usuario', 'bot', 'fallback'
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    
    conversacion = relationship("Conversacion", back_populates="mensajes")