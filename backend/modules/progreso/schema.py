"""
Esquemas Pydantic para validación de datos de entrada (Request) 
y serialización de datos de salida (Response).
"""
from pydantic import BaseModel
from datetime import datetime
from typing import List

class ProgresoLeccionCreate(BaseModel):
    leccion_id: int

class IntentoQuizCreate(BaseModel):
    quiz_id: int
    puntaje: int

class InsigniaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    icono_url: str

    class Config:
        # Permite a Pydantic leer los datos directamente desde los objetos ORM de SQLAlchemy
        from_attributes = True

class ResumenProgresoResponse(BaseModel):
    lecciones_completadas: List[int]
    quizzes_aprobados: List[int]
    insignias: List[InsigniaResponse]