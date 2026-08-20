from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


def _key_por_sesion_o_ip(request: Request) -> str:
    """Limita por token de sesión cuando existe (evita que varios usuarios
    detrás del mismo NAT/wifi compartan el mismo límite); si no hay token
    (ej. /auth/login, antes de tener uno) cae a la IP."""
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:]
    return get_remote_address(request)


limiter = Limiter(key_func=_key_por_sesion_o_ip)
