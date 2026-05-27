from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import decode_token
from modules.auth import repository as auth_repo
from modules.auth.entity import Usuario


def get_usuario_actual(
    authorization: str = Header(...), db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia que extrae el usuario desde el JWT.
    Úsala en cualquier endpoint que requiera login:
        def mi_endpoint(usuario: Usuario = Depends(get_usuario_actual)):
    """
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        usuario_id = int(payload["sub"])
    except (ValueError, KeyError):
        raise HTTPException(status_code=401, detail="No autenticado")

    usuario = auth_repo.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario


def requiere_admin(usuario: Usuario = Depends(get_usuario_actual)) -> Usuario:
    """Dependencia que además exige rol admin."""
    if usuario.rol.value != "admin":
        raise HTTPException(status_code=403, detail="Requiere permisos de administrador")
    return usuario
