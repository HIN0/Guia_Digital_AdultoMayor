from sqlalchemy.orm import Session

from core.security import create_access_token, verify_google_token
from modules.auth import repository
from modules.auth.entity import Usuario


def generar_token(usuario: Usuario) -> str:
    """Crea un JWT propio con el id del usuario y su rol."""
    return create_access_token({
        "sub": str(usuario.id),
        "rol": usuario.rol.value,
    })


async def login_con_google(db: Session, google_token: str) -> tuple[str, Usuario]:
    """
    1. Verifica el token con Google
    2. Busca o crea el usuario en nuestra DB
    3. Genera un JWT para el frontend
    """
    datos_google = await verify_google_token(google_token)

    # Buscar usuario existente o crear uno nuevo
    usuario = repository.get_usuario_by_google_id(db, datos_google["google_id"])
    if not usuario:
        usuario = repository.crear_usuario(
            db,
            google_id=datos_google["google_id"],
            email=datos_google["email"],
            nombre=datos_google["nombre"],
        )

    return generar_token(usuario), usuario


def get_usuario_actual(db: Session, usuario_id: int) -> Usuario:
    usuario = repository.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise ValueError("Usuario no encontrado")
    return usuario
