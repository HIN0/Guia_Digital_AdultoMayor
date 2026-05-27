"""
Session es el objeto que representa una conexión activa con la base de datos. 
Cada vez que un endpoint recibe una petición, FastAPI le crea una sesión nueva (gracias a get_db()), 
la pasa al repository, y la cierra al terminar. La sesión es la que ejecuta los queries. 
Aquí la importas solo para usarla como tipo en los parámetros de las funciones (db: Session), 
lo que le dice a Python y a tu editor qué tipo de objeto es db.
"""
from sqlalchemy.orm import Session

"""
mportas las clases que representan las tablas. Se necesitan aca porque el query trabaja con ellas:
db.query(Modulo) le dice a SQLAlchemy "quiero buscar en la tabla modulo".
"""
from modules.educacion.entity import Modulo, Leccion, QuizFinal


"""
- db: Session siempre es el primer parámetro. Es la sesión de base de datos que viene desde el endpoint via Depends(get_db)
- Los parámetros siguientes son los filtros o datos que necesita el query
-> tipo_retorno: le dice a Python qué devuelve la función. Es opcional pero ayuda mucho al editor a detectar errores
"""
def get_todos_los_modulos(db: Session) -> list[Modulo]:
    return db.query(Modulo).order_by(Modulo.orden).all()

def get_modulo_por_id(db: Session, modulo_id: int) -> Modulo | None:
    return db.query(Modulo).filter(Modulo.id == modulo_id).first()

def get_leccion_por_id(db: Session, leccion_id: int) -> Leccion | None:
    return db.query(Leccion).filter(Leccion.id == leccion_id).first()

def get_quiz_por_modulo(db: Session, modulo_id: int) -> QuizFinal | None:
    return db.query(QuizFinal).filter(QuizFinal.modulo_id == modulo_id).first()
