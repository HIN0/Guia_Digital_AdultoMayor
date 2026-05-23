"""
Mapean las entidades del dominio de Progreso a tablas físicas en PostgreSQL. Modelos ORM de SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from core.database import Base 
from datetime import datetime

class ProgresoLeccion(Base):
    __tablename__ = "progreso_leccion"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False) # Relación lógica con el módulo Auth
    leccion_id = Column(Integer, nullable=False) # Relación lógica con el módulo Educación
    completada = Column(Boolean, default=False)
    fecha_completado = Column(DateTime, default=datetime.utcnow)

class IntentoQuiz(Base):
    __tablename__ = "intento_quiz"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    quiz_id = Column(Integer, nullable=False)
    puntaje = Column(Integer, default=0)
    aprobado = Column(Boolean, default=False)
    fecha_intento = Column(DateTime, default=datetime.utcnow)

class Insignia(Base):
    __tablename__ = "insignia"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)
    icono_url = Column(String)

class InsigniaObtenida(Base):
    __tablename__ = "insignia_obtenida"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    insignia_id = Column(ForeignKey("insignia.id"))
    fecha_obtencion = Column(DateTime, default=datetime.utcnow)