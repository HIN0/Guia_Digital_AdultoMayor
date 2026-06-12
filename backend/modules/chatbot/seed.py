"""
Seed idempotente de la whitelist del chatbot.

Se ejecuta en cada arranque del backend (lifespan). Revisa pregunta por
pregunta si ya existe en la BD (por texto_pregunta exacto) y solo inserta
las que faltan. Reiniciar el servidor NUNCA duplica datos.

Las respuestas están redactadas a partir de conocimiento.txt, en lenguaje
simple para adultos mayores. Cada pregunta servida desde la whitelist
NO consume cuota de Groq.
"""

import logging
from core.database import SessionLocal
from .entity import Patologia, PreguntaChatbot

logger = logging.getLogger(__name__)

SALUDO_FIJO = "Hola. Estoy aquí para responder preguntas sobre salud. ¿En qué puedo ayudarte?"

SEED_DATA = {
    "General": [
        {
            "pregunta": "hola",
            "respuesta": SALUDO_FIJO,
            "variantes": ["buenos días", "buenas tardes", "buenas noches",
                          "hola, ¿cómo estás?", "qué tal", "aló", "hola bot"],
        },
        {
            "pregunta": "gracias",
            "respuesta": "De nada. Si tiene otra pregunta sobre salud, estoy aquí para ayudarle.",
            "variantes": ["muchas gracias", "se agradece", "gracias por la ayuda",
                          "muy amable", "ok gracias"],
        },
        {
            "pregunta": "adiós",
            "respuesta": "Hasta pronto. Cuídese mucho y recuerde asistir a sus controles médicos.",
            "variantes": ["chao", "hasta luego", "nos vemos", "me voy", "eso era todo"],
        },
        {
            "pregunta": "¿qué puedes hacer?",
            "respuesta": "Puedo responder sus preguntas sobre salud, como la diabetes, sus síntomas y cuidados, y también darle información sobre los horarios y servicios del HUAP. ¿Sobre qué le gustaría saber?",
            "variantes": ["¿para qué sirves?", "¿en qué me puedes ayudar?",
                          "¿qué sabes hacer?", "ayuda", "¿qué preguntas puedo hacer?"],
        },
    ],

    "Diabetes": [
        {
            "pregunta": "¿Qué es la diabetes?",
            "respuesta": (
                "La diabetes es una enfermedad crónica que ocurre cuando el páncreas no produce "
                "suficiente insulina o cuando el cuerpo no la utiliza correctamente. La insulina es "
                "una hormona que regula el azúcar en la sangre. Existen dos tipos principales: "
                "Tipo 1 (el cuerpo no produce insulina) y Tipo 2 (el cuerpo no usa bien la insulina). "
                "El Tipo 2 es el más frecuente en adultos mayores."
            ),
            "variantes": ["¿qué significa tener diabetes?", "explíqueme la diabetes",
                          "¿qué es ser diabético?", "¿qué le pasa a uno con la diabetes?",
                          "¿qué es la enfermedad del azúcar?", "háblame de la diabetes"],
        },
        {
            "pregunta": "¿Cuáles son los síntomas de la diabetes?",
            "respuesta": (
                "Los síntomas más comunes de la diabetes son: sed excesiva y boca seca, necesidad "
                "frecuente de orinar (especialmente de noche), cansancio sin razón aparente, visión "
                "borrosa, heridas que tardan en cicatrizar, hormigueo o entumecimiento en manos y pies, "
                "pérdida de peso sin dieta, hambre frecuente e infecciones recurrentes en la piel, "
                "encías o vejiga. Si tiene varios de estos síntomas, consulte a su médico."
            ),
            "variantes": ["¿qué síntomas da la diabetes?", "¿cómo sé si tengo diabetes?",
                          "señales de la diabetes", "¿qué se siente cuando uno tiene diabetes?",
                          "¿qué síntomas da el azúcar alta?", "síntomas de azúcar en la sangre"],
        },
        {
            "pregunta": "¿Cuáles son las causas de la diabetes?",
            "respuesta": (
                "Las principales causas y factores de riesgo de la diabetes son: antecedentes "
                "familiares, sobrepeso u obesidad (especialmente en la zona abdominal), falta de "
                "actividad física, alimentación alta en azúcares y harinas refinadas, edad mayor de "
                "45 años, hipertensión arterial, colesterol o triglicéridos altos, y estrés crónico."
            ),
            "variantes": ["¿por qué da la diabetes?", "¿qué provoca la diabetes?",
                          "¿de dónde viene la diabetes?", "factores de riesgo de la diabetes",
                          "¿la diabetes es hereditaria?"],
        },
        {
            "pregunta": "¿Cómo puedo prevenir o controlar la diabetes?",
            "respuesta": (
                "Para prevenir o controlar la diabetes se recomienda: comer frutas, verduras y "
                "legumbres todos los días, preferir cereales integrales, reducir el azúcar, las "
                "bebidas azucaradas y las frituras, caminar al menos 30 minutos diarios, tomar sus "
                "medicamentos sin saltarse dosis, asistir a sus controles médicos, no fumar y dormir "
                "entre 7 y 8 horas por noche."
            ),
            "variantes": ["¿cómo evito la diabetes?", "¿cómo cuidarme de la diabetes?",
                          "¿qué hago para controlar la diabetes?", "consejos para la diabetes",
                          "¿cómo bajar el azúcar?", "buenas prácticas para la diabetes"],
        },
        {
            "pregunta": "¿Qué alimentos debo comer si tengo diabetes?",
            "respuesta": (
                "Se recomienda consumir frutas, verduras y legumbres todos los días, preferir "
                "cereales integrales como avena, arroz integral y pan integral, comer en porciones "
                "moderadas y a horarios regulares, y beber al menos 8 vasos de agua al día. "
                "Conviene reducir el azúcar, las bebidas azucaradas, los dulces, las frituras y "
                "los alimentos procesados."
            ),
            "variantes": ["¿qué puedo comer con diabetes?", "dieta para diabéticos",
                          "alimentación para la diabetes", "¿qué comida es buena para el azúcar?",
                          "¿qué no debo comer si tengo diabetes?"],
        },
        {
            "pregunta": "¿Qué ejercicio puedo hacer si tengo diabetes?",
            "respuesta": (
                "Se recomienda realizar al menos 30 minutos de caminata diaria, subir escaleras en "
                "lugar de usar el ascensor cuando sea posible, y practicar actividades suaves como "
                "yoga, natación o bicicleta estacionaria. También es importante evitar permanecer "
                "sentado más de 2 horas seguidas."
            ),
            "variantes": ["ejercicios para diabéticos", "¿puedo hacer deporte con diabetes?",
                          "actividad física para la diabetes", "¿cuánto debo caminar?"],
        },
        {
            "pregunta": "¿Qué controles médicos debo hacerme si tengo diabetes?",
            "respuesta": (
                "Debe medir su glucosa en sangre según la indicación de su médico, asistir a los "
                "controles con su médico o enfermera, tomar los medicamentos prescritos sin saltarse "
                "dosis, controlar su presión arterial regularmente y realizarse el examen de "
                "hemoglobina glicosilada (HbA1c) al menos 2 veces al año."
            ),
            "variantes": ["¿cada cuánto debo controlarme la diabetes?", "exámenes para la diabetes",
                          "¿qué es la hemoglobina glicosilada?", "¿cuándo debo medirme el azúcar?"],
        },
        {
            "pregunta": "¿Por qué debo cuidarme los pies si tengo diabetes?",
            "respuesta": (
                "Las personas con diabetes deben revisar sus pies todos los días para detectar "
                "heridas o cambios en la piel, ya que las heridas pueden tardar mucho en cicatrizar. "
                "También se recomienda usar calzado cómodo y adecuado. Si nota una herida que no "
                "sana, consulte a su médico."
            ),
            "variantes": ["cuidado de los pies en diabetes", "¿cómo cuidar mis pies?",
                          "pie diabético", "¿por qué revisar los pies?"],
        },
    ],

    "Información General HUAP": [
        {
            "pregunta": "¿Cuál es el horario de atención del hospital?",
            "respuesta": (
                "El hospital atiende de lunes a viernes de 8:00 de la mañana a 9:00 de la noche. "
                "Los fines de semana, el servicio de urgencias atiende las 24 horas."
            ),
            "variantes": ["¿a qué hora atienden?", "horario del HUAP",
                          "¿cuándo está abierto el hospital?", "¿atienden los fines de semana?",
                          "¿a qué hora abren?", "¿hasta qué hora atienden?"],
        },
        {
            "pregunta": "¿Qué es la Guía Digital del HUAP?",
            "respuesta": (
                "La Guía Digital del HUAP es una plataforma educativa en línea diseñada "
                "especialmente para personas mayores. Ofrece lecciones interactivas sobre "
                "tecnología, salud y bienestar. Cada módulo contiene lecciones con texto, "
                "imágenes y audio para facilitar el aprendizaje."
            ),
            "variantes": ["¿qué es esta aplicación?", "¿qué es la guía digital?",
                          "¿para qué sirve esta plataforma?", "¿qué es esta página?"],
        },
        {
            "pregunta": "¿Dónde puedo pedir ayuda si tengo problemas con la plataforma?",
            "respuesta": (
                "Si tiene problemas para acceder a la plataforma, puede acercarse al mesón de "
                "atención del HUAP de lunes a viernes de 8:00 a 17:00 horas, o llamar al número "
                "de soporte indicado en su tarjeta de atención."
            ),
            "variantes": ["soporte técnico", "no puedo entrar a la plataforma",
                          "¿a quién llamo si tengo problemas?", "ayuda con la aplicación",
                          "tengo problemas para entrar"],
        },
    ],
}


def seed_chatbot():
    """Puebla patologías y preguntas de la whitelist. Idempotente:
    solo inserta lo que no existe. Llamar en el startup del backend,
    ANTES de inicializar_chatbot() para que el índice FAISS incluya el seed."""
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
                    continue

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
