"""
Motor del seed de la whitelist del chatbot. NO editar para agregar contenido:
el contenido vive en modules/chatbot/seeds/ (un archivo por patología/tema).

Idempotente: revisa pregunta por pregunta si ya existe en la BD (por
texto_pregunta exacto) y solo inserta las que faltan. Reiniciar el backend
NUNCA duplica datos, y las respuestas editadas por un admin no se pisan.
"""

import logging
from core.database import SessionLocal
from .entity import Patologia, PreguntaChatbot
from .seeds import SEED_DATA

logger = logging.getLogger(__name__)


def seed_chatbot():
    """Pobla patologías y preguntas de la whitelist desde seeds/.
    Llamar en el startup del backend, ANTES de inicializar_chatbot()
    para que el índice FAISS incluya el seed."""
    db = SessionLocal()
    insertadas = 0
    try:
        for nombre_patologia, preguntas in SEED_DATA.items():
            patologia = db.query(Patologia).filter(Patologia.nombre == nombre_patologia).first()
            if not patologia:
                patologia = Patologia(nombre=nombre_patologia, validada=True)
                db.add(patologia)
                db.commit()
                db.refresh(patologia)

            for item in preguntas:
                existe = (
                    db.query(PreguntaChatbot)
                    .filter(PreguntaChatbot.texto_pregunta == item["pregunta"])
                    .first()
                )
                if existe:
                    existe.respuesta_validada = item["respuesta"]
                    existe.variantes = item.get("variantes", [])
                else:
                    db.add(PreguntaChatbot(
                        patologia_id=patologia.id,
                        texto_pregunta=item["pregunta"],
                        respuesta_validada=item["respuesta"],
                        variantes=item.get("variantes", []),
                        activa=True,
                    ))
                    insertadas += 1

        db.commit()
        if insertadas:
            logger.info("Seed chatbot: %d preguntas nuevas insertadas.", insertadas)
        else:
            logger.info("Seed chatbot: la whitelist ya estaba poblada, nada que insertar.")
    except Exception:
        db.rollback()
        logger.exception("Error ejecutando el seed del chatbot")
        raise
    finally:
        db.close()
