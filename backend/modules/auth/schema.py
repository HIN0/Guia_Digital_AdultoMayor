from pydantic import BaseModel
from modules.auth.entity import RolUsuario

class LoginRequest(BaseModel):
    """Lo que el frontend envía al hacer login con Google."""
    google_token: str

class UsuarioResponse(BaseModel):
    """Lo que devolvemos del usuario (nunca el token de Google)."""
    id: int
    email: str
    nombre: str
    rol: RolUsuario
    es_invitado: bool = False

    class Config:
        from_attributes = True  # Permite leer desde objetos SQLAlchemy

class TokenResponse(BaseModel):
    """Respuesta del login: JWT + datos del usuario."""
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
