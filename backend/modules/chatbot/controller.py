from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db

# 1. Importamos tu dependencia de seguridad real y el esquema de Usuario
from core.dependencies import get_usuario_actual
from modules.auth.entity import Usuario 

from .schema import ChatRequest, ChatResponse
from .service import generar_y_guardar_respuesta

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/preguntar", response_model=ChatResponse)
def hacer_pregunta(
    request: ChatRequest, 
    db: Session = Depends(get_db),
    # 2. Inyectamos el usuario logueado usando tu función
    usuario: Usuario = Depends(get_usuario_actual) 
):
    try:
        resultado = generar_y_guardar_respuesta(
            db=db, 
            usuario_id=usuario.id, # 3. Pasamos el ID del usuario extraído de la dependencia
            pregunta=request.pregunta, 
            conversacion_id=request.conversacion_id
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))