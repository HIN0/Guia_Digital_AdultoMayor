from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.dependencies import get_usuario_actual
from modules.auth import service
from modules.auth.entity import Usuario
from modules.auth.schema import LoginRequest, TokenResponse, UsuarioResponse

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    El frontend envía el id_token de Google.
    Devuelve un JWT propio + datos del usuario.
    """
    try:
        access_token, usuario = await service.login_con_google(db, body.google_token)
        return TokenResponse(access_token=access_token, usuario=usuario)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UsuarioResponse)
def get_me(usuario: Usuario = Depends(get_usuario_actual)):
    """Devuelve los datos del usuario autenticado. Requiere: Authorization: Bearer <token>"""
    return usuario
