"""
Un schema es básicamente un contrato de datos. Define exactamente qué campos tiene un JSON que entra o
sale de tu API.En FastAPI se usan con Pydantic, que es una librería que valida datos automáticamente. 
Cuando defines un schema, Pydantic se encarga de tres cosas por ti:
- Validar que los datos tengan la forma correcta (si esperas un int y llega un texto, Pydantic 
lo rechaza automáticamente con un error claro)
- Convertir tipos cuando puede (el string "3" que viene en una URL lo convierte a int 3)
- Filtrar la respuesta (si tu objeto de base de datos tiene 10 campos pero el schema solo
"""


"""
incluye 5, FastAPI devuelve solo esos 5 al cliente, aunque tu función devuelva el objeto completo)
En este módulo de educación, los schemas definen la forma de los módulos, lecciones y quizzes que se 
envían al frontend.
En el controller, usamos estos schemas para decirle a FastAPI qué forma tiene la respuesta de cada endpoint.
FastAPI entonces se encarga de validar y filtrar automáticamente, lo que hace quenuestro código sea más 
limpio y seguro.
"""

"""
Clase madre de todos los schemas. Heredar de ella activa toda la magia de Pydantic: validación 
automática, conversión de tipos, serialización a JSON.
"""
from pydantic import BaseModel

"""
Any es un tipo especial que significa "acepta cualquier cosa". Lo usas cuando el dato puede tener
 cualquier estructura, como un JSON flexible. Lo vas a ver en contenido.
"""
from typing import Any

"""
class Config: from_attributes = True
Esto aparece en todos los schemas y es importante entenderlo. Por defecto, Pydantic solo sabe leer 
datos de diccionarios Python. Pero SQLAlchemy te devuelve objetos (instancias de tus clases Modulo, 
Leccion, etc.), no diccionarios.
from_attributes = True le dice a Pydantic: "también puedes leer datos desde atributos de objetos". O sea, 
en vez de buscar datos["id"] puede leer objeto.id. Sin esto, FastAPI no podría convertir tus entidades 
de SQLAlchemy a JSON.
"""



class OpcionRespuestaResponse(BaseModel):
    id: int
    texto: str
    # NO incluimos es_correcta aquí — no la mandamos al frontend durante el quiz

    class Config:
        from_attributes = True


class PreguntaQuizResponse(BaseModel):
    id: int
    enunciado: str
    opciones: list[OpcionRespuestaResponse]

    class Config:
        from_attributes = True


class QuizFinalResponse(BaseModel):
    id: int
    minimo_aciertos: int
    bloqueante: bool
    preguntas: list[PreguntaQuizResponse]

    class Config:
        from_attributes = True


class LeccionResponse(BaseModel):
    id: int
    titulo: str
    orden: int
    contenido: Any  # JSON flexible

    class Config:
        from_attributes = True


class ModuloResponse(BaseModel):
    id: int
    nombre: str
    orden: int
    requiere_modulo_previo: bool

    class Config:
        from_attributes = True


class ModuloDetalleResponse(ModuloResponse):
    lecciones: list[LeccionResponse]
    quiz_final: QuizFinalResponse | None
