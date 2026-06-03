from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    pregunta: str
    conversacion_id: Optional[int] = None

class ChatResponse(BaseModel):
    respuesta: str
    conversacion_id: int