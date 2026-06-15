"""
Esquemas Pydantic para validación de datos de entrada (Request)
y serialización de datos de salida (Response).
"""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ProgresoLeccionCreate(BaseModel):
    leccion_id: int

class IntentoQuizCreate(BaseModel):
    quiz_id: int
    puntaje: int

class RespuestaItem(BaseModel):
    pregunta_id: int
    opcion_id: int

class SubmitQuizCreate(BaseModel):
    quiz_id: int
    respuestas: List[RespuestaItem]

class FeedbackPregunta(BaseModel):
    pregunta_id: int
    opcion_correcta_id: int
    opcion_seleccionada_id: int
    es_correcta: bool
    feedback: str

class InsigniaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    icono_url: str

    class Config:
        from_attributes = True

class ResultadoQuizResponse(BaseModel):
    puntaje: int
    minimo_aciertos: int
    aprobado: bool
    feedbacks: List[FeedbackPregunta]
    insignia_otorgada: Optional[InsigniaResponse] = None

class LeccionCompletadaResponse(BaseModel):
    leccion_id: int
    completada: bool
    insignia_otorgada: Optional[InsigniaResponse] = None

class ResumenProgresoResponse(BaseModel):
    lecciones_completadas: List[int]
    quizzes_aprobados: List[int]
    insignias: List[InsigniaResponse]
