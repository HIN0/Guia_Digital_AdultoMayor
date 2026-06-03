from sqlalchemy.orm import Session
from .entity import Conversacion, MensajeChat

def obtener_o_crear_conversacion(db: Session, usuario_id: int, conversacion_id: int = None) -> Conversacion:
    if conversacion_id:
        conv = db.query(Conversacion).filter(
            Conversacion.id == conversacion_id, 
            Conversacion.usuario_id == usuario_id
        ).first()
        if conv:
            return conv
            
    nueva_conv = Conversacion(usuario_id=usuario_id)
    db.add(nueva_conv)
    db.commit()
    db.refresh(nueva_conv)
    return nueva_conv

def guardar_mensaje(db: Session, conversacion_id: int, tipo: str, contenido: str) -> MensajeChat:
    mensaje = MensajeChat(
        conversacion_id=conversacion_id, 
        tipo=tipo, 
        contenido=contenido
    )
    db.add(mensaje)
    db.commit()
    db.refresh(mensaje)
    return mensaje