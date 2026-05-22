#SQLAlchemy es la librería que conecta Python con PostgreSQL. 
#Aquí importas los tipos de columna que vas a usar para definir las tablas. 
#Cada uno representa un tipo de dato en la base de datos:
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON

#relationship es lo que te permite navegar entre tablas como si fueran objetos Python. 
#Por ejemplo, en vez de hacer un JOIN manual en SQL, 
#puedes escribir modulo.lecciones y te devuelve la lista automáticamente.
from sqlalchemy.orm import relationship

#Base es la clase madre de la que heredan todos tus modelos.Está definida en core/database.py 
#y es lo que le dice a SQLAlchemy "registra esta clase como una tabla de la base de datos"
from core.database import Base

#Declaras una clase Python normal, pero al heredar de Base, SQLAlchemy la trata como una tabla. 
#La clase = la tabla. Las instancias de la clase = las filas.
class Modulo(Base):

    #nombre de la tabla en la base de datos.
    __tablename__ = "modulo"

    #index=True — crea un índice en esa columna, lo que hace las búsquedas por id más rápidas
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    orden = Column(Integer, nullable=False)
    requiere_modulo_previo = Column(Boolean, default=False)

    #Es una relación virtual que SQLAlchemy usa para navegar entre objetos.
    #- "Leccion": apunta a la clase Leccion (en string para evitar problemas de orden de definición)
    #- back_populates="modulo": le dice que en la clase Leccion hay un atributo llamado modulo 
    #que apunta de vuelta a Modulo. Los dos lados se sincronizan
    #- order_by="Leccion.orden": cuando pidas las lecciones de un módulo, 
    #vienen ordenadas por su campo orden automáticamente
    lecciones = relationship("Leccion", back_populates="modulo", order_by="Leccion.orden")

    #uselist=False cambia el comportamiento: en vez de devolver una lista, devuelve un solo objeto (o None).
    #Se usa porque cada módulo tiene exactamente un quiz final, no varios.
    quiz_final = relationship("QuizFinal", back_populates="modulo", uselist=False)


class Leccion(Base):
    __tablename__ = "leccion"

    id = Column(Integer, primary_key=True, index=True)
    modulo_id = Column(Integer, ForeignKey("modulo.id"), nullable=False)
    titulo = Column(String, nullable=False)
    orden = Column(Integer, nullable=False)
    # contenido es JSON flexible: concepto, ejemplos, ejercicio interactivo, etc.
    contenido = Column(JSON, nullable=False)

    modulo = relationship("Modulo", back_populates="lecciones")


class QuizFinal(Base):
    __tablename__ = "quiz_final"

    id = Column(Integer, primary_key=True, index=True)
    modulo_id = Column(Integer, ForeignKey("modulo.id"), nullable=False)
    minimo_aciertos = Column(Integer, nullable=False)
    bloqueante = Column(Boolean, default=False)

    modulo = relationship("Modulo", back_populates="quiz_final")
    preguntas = relationship("PreguntaQuiz", back_populates="quiz_final")


class PreguntaQuiz(Base):
    __tablename__ = "pregunta_quiz"

    id = Column(Integer, primary_key=True, index=True)
    quiz_final_id = Column(Integer, ForeignKey("quiz_final.id"), nullable=False)
    enunciado = Column(String, nullable=False)
    # Texto que aparece cuando el usuario responde mal, explicando por qué está mal
    feedback = Column(String, nullable=False)

    quiz_final = relationship("QuizFinal", back_populates="preguntas")
    opciones = relationship("OpcionRespuesta", back_populates="pregunta")


class OpcionRespuesta(Base):
    __tablename__ = "opcion_respuesta"

    id = Column(Integer, primary_key=True, index=True)
    pregunta_id = Column(Integer, ForeignKey("pregunta_quiz.id"), nullable=False)
    texto = Column(String, nullable=False)
    es_correcta = Column(Boolean, default=False)

    pregunta = relationship("PreguntaQuiz", back_populates="opciones")
