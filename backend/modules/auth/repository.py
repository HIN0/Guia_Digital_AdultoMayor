from sqlalchemy.orm import Session

from modules.auth.entity import Usuario


def get_usuario_by_google_id(db: Session, google_id: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.google_id == google_id).first()

def get_usuario_by_id(db: Session, usuario_id: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def crear_usuario(db: Session, google_id: str, email: str, nombre: str) -> Usuario:
    usuario = Usuario(google_id=google_id, email=email, nombre=nombre)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

