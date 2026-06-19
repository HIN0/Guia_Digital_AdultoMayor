from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import decode_token
from modules.auth import service
from modules.auth.schema import LoginRequest, TokenResponse, UsuarioResponse

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/invitado", response_model=TokenResponse)
async def login_invitado(db: Session = Depends(get_db)):
    """
    Crea un usuario invitado único y devuelve un JWT para acceder a la plataforma.
    """
    try:
        access_token, usuario = await service.login_como_invitado(db)
        return TokenResponse(access_token=access_token, usuario=usuario)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
def get_me(authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    Devuelve los datos del usuario autenticado.
    El frontend debe enviar: Authorization: Bearer <token>
    """
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        usuario_id = int(payload["sub"])
        usuario = service.get_usuario_actual(db, usuario_id)
        return usuario
    except (ValueError, KeyError):
        raise HTTPException(status_code=401, detail="No autenticado")
