from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_usuario_actual
from core.rate_limit import limiter
from modules.auth import service
from modules.auth.entity import Usuario
from modules.auth.schema import LoginRequest, TokenResponse, UsuarioResponse

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(request: Request, body: LoginRequest, db: Session = Depends(get_db)):
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


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("20/minute")
def refresh(request: Request, usuario: Usuario = Depends(get_usuario_actual)):
    """
    Renueva el JWT de un usuario ya autenticado (requiere que el token actual
    todavía sea válido) para extender la sesión sin volver a pasar por el
    login de Google cada vez que expira (ACCESS_TOKEN_EXPIRE_MINUTES).
    """
    access_token = service.generar_token(usuario)
    return TokenResponse(access_token=access_token, usuario=usuario)
