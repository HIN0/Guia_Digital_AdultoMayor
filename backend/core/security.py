from datetime import datetime, timedelta
from jose import JWTError, jwt
import httpx
from core.config import settings

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"


async def verify_google_token(token: str) -> dict:
    """Verifica el id_token de Google y retorna los datos del usuario."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GOOGLE_TOKEN_INFO_URL, params={"id_token": token}
        )
    if response.status_code != 200:
        raise ValueError("Token de Google inválido")
    
    data = response.json()
    
    # Verificar que el token es para nuestra app
    if data.get("aud") != settings.GOOGLE_CLIENT_ID:
        raise ValueError("Token no corresponde a esta aplicación")
    
    return {
        "google_id": data["sub"],
        "email": data["email"],
        "nombre": data.get("name", ""),
    }


def create_access_token(data: dict) -> str:
    """Genera un JWT para que el frontend use en sus requests."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    """Decodifica y valida un JWT. Lanza excepción si es inválido."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Token inválido o expirado")
