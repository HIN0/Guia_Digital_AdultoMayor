from sqlalchemy import Column, Integer, String, Enum
from core.database import Base
import enum

class RolUsuario(str, enum.Enum):
    alumno = "alumno"
    admin = "admin"

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    rol = Column(Enum(RolUsuario), default=RolUsuario.alumno, nullable=False)
