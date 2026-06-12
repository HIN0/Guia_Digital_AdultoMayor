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
            "respuesta": (
                "Puedo responder sus preguntas sobre salud: gastroenteritis, neumonía, infección "
                "urinaria, dolor de cabeza y lumbago. También puedo orientarle sobre cuándo ir a "
                "urgencias y darle información del HUAP. ¿Sobre qué le gustaría saber?"
            ),
            "variantes": ["¿para qué sirves?", "¿en qué me puedes ayudar?",
                          "¿qué sabes hacer?", "ayuda", "¿qué preguntas puedo hacer?"],
        },
    ],

    "Urgencias y Síntomas Frecuentes": [
        # ── GASTROENTERITIS ──────────────────────────────────────────────────
        {
            "pregunta": "¿Qué es la gastroenteritis?",
            "respuesta": (
                "La gastroenteritis es una infección del estómago e intestinos que produce diarrea "
                "y/o vómitos. Habitualmente es causada por virus o bacterias y suele mejorar sola "
                "en pocos días con reposo e hidratación."
            ),
            "variantes": ["tengo diarrea y vómitos ¿qué tengo?", "¿qué es la infección intestinal?",
                          "me duele la guata y tengo diarrea", "¿qué causa la diarrea?",
                          "infección estomacal", "gastroenteritis aguda"],
        },
        {
            "pregunta": "¿Cuándo debo ir a urgencias por diarrea o vómitos?",
            "respuesta": (
                "Acuda a urgencias o llame al 131 si tiene: boca muy seca o muy poca orina "
                "(señales de deshidratación), confusión o desorientación, sangre en las "
                "deposiciones, vómitos que no le permiten tomar líquidos, fiebre alta que no baja, "
                "o si no mejora en 48-72 horas. En adultos mayores la confusión puede ser la única "
                "señal de deshidratación grave."
            ),
            "variantes": ["señales de alarma gastroenteritis", "¿cuándo es grave la diarrea?",
                          "me desidrato con la diarrea", "¿cuándo llamar al médico por vómitos?",
                          "sangre en deposiciones", "diarrea con fiebre"],
        },
        {
            "pregunta": "¿Cómo me cuido si tengo gastroenteritis?",
            "respuesta": (
                "Tomar bastante líquido (agua, sales de rehidratación oral) para no deshidratarse. "
                "Comer en porciones pequeñas cuando tolere. Lavarse bien las manos. No tome "
                "antidiarreicos por cuenta propia si tiene fiebre o sangre en las deposiciones, "
                "ya que pueden ser perjudiciales. Si los síntomas empeoran, consulte a su médico."
            ),
            "variantes": ["¿qué hago si tengo diarrea?", "cuidados para la gastroenteritis",
                          "¿qué tomar para la diarrea?", "me siento mal del estómago"],
        },

        # ── NEUMONÍA ──────────────────────────────────────────────────────────
        {
            "pregunta": "¿Qué es la neumonía?",
            "respuesta": (
                "La neumonía es una infección de los pulmones causada generalmente por bacterias o "
                "virus. Produce tos con flemas, fiebre y dificultad para respirar. En adultos "
                "mayores puede presentarse de forma diferente: solo con confusión, decaimiento o "
                "caídas, a veces sin fiebre."
            ),
            "variantes": ["¿qué es una pulmonía?", "me diagnosticaron neumonía",
                          "infección pulmonar", "¿qué es la neumonía?", "pulmonía"],
        },
        {
            "pregunta": "¿Cuándo debo ir a urgencias por la tos o dificultad para respirar?",
            "respuesta": (
                "Acuda a urgencias o llame al 131 de inmediato si tiene: dificultad marcada para "
                "respirar, labios o uñas de color azulado, confusión o desorientación repentina, "
                "respiración muy rápida o decaimiento intenso. Estos son signos de que los pulmones "
                "no están recibiendo suficiente oxígeno."
            ),
            "variantes": ["me cuesta respirar ¿qué hago?", "señales de alarma neumonía",
                          "¿cuándo es grave la tos?", "dificultad para respirar urgencias",
                          "me ahogo", "falta de aire"],
        },
        {
            "pregunta": "¿Cómo prevenir la neumonía?",
            "respuesta": (
                "Las medidas más importantes son: vacunarse contra la neumonía (vacuna "
                "antineumocócica) y contra la influenza todos los años, no fumar, lavarse las "
                "manos con frecuencia y mantener buena higiene respiratoria."
            ),
            "variantes": ["vacuna contra la neumonía", "¿cómo evitar la pulmonía?",
                          "prevención neumonía adulto mayor", "¿me debo vacunar contra la neumonía?"],
        },

        # ── INFECCIÓN URINARIA (ITU) ──────────────────────────────────────────
        {
            "pregunta": "¿Qué es la infección urinaria?",
            "respuesta": (
                "La infección urinaria baja (también llamada cistitis) es una infección de la "
                "vejiga causada habitualmente por bacterias. Es muy frecuente en adultos mayores, "
                "especialmente en mujeres. Produce ardor al orinar, ganas frecuentes de ir al baño "
                "y orina turbia o con mal olor. En personas mayores puede manifestarse solo como "
                "confusión o decaimiento, sin síntomas urinarios evidentes."
            ),
            "variantes": ["ardor al orinar", "¿qué es la cistitis?", "infección al riñón",
                          "orino seguido y me duele", "ITU", "infección urinaria",
                          "¿por qué orino tanto?", "orina con mal olor"],
        },
        {
            "pregunta": "¿Cuándo debo consultar por una infección urinaria?",
            "respuesta": (
                "Consulte a su médico si aparece fiebre, dolor intenso en la zona de la espalda "
                "alta o los riñones, confusión repentina o malestar general importante. Estos "
                "síntomas pueden indicar que la infección llegó al riñón, lo que requiere atención "
                "médica. Si los síntomas son solo ardor al orinar y ganas frecuentes, igualmente "
                "consulte para recibir tratamiento con antibióticos."
            ),
            "variantes": ["señales de alarma infección urinaria", "¿cuándo es grave la infección urinaria?",
                          "me duelen los riñones", "fiebre con ardor al orinar"],
        },
        {
            "pregunta": "¿Cómo prevenir la infección urinaria?",
            "respuesta": (
                "Tome bastante agua durante el día, no aguante las ganas de orinar, mantenga una "
                "buena higiene en la zona íntima y, si usa sonda vesical, siga las instrucciones "
                "de su equipo de salud para su cuidado."
            ),
            "variantes": ["¿cómo evitar la infección urinaria?", "prevención cistitis",
                          "¿qué tomar para no tener infección urinaria?"],
        },

        # ── CEFALEA ───────────────────────────────────────────────────────────
        {
            "pregunta": "¿Por qué me duele la cabeza?",
            "respuesta": (
                "El dolor de cabeza (cefalea) es un síntoma, no una enfermedad. Las causas más "
                "frecuentes son tensión muscular, estrés, migraña, presión arterial alta o "
                "problemas de cuello. La mayoría son benignas. Sin embargo, algunas pueden ser "
                "señal de algo grave, por lo que es importante conocer las señales de alarma."
            ),
            "variantes": ["me duele la cabeza", "dolor de cabeza frecuente", "¿qué es la cefalea?",
                          "tengo jaqueca", "migraña", "cefalea", "¿por qué tengo dolor de cabeza?"],
        },
        {
            "pregunta": "¿Cuándo es peligroso el dolor de cabeza?",
            "respuesta": (
                "Acuda a urgencias o llame al 131 de inmediato si el dolor de cabeza: aparece de "
                "golpe y es muy intenso (como 'el peor dolor de su vida'), va acompañado de fiebre "
                "y cuello rígido, le produce debilidad, dificultad para hablar o para ver, es nuevo "
                "en una persona mayor de 50 años, apareció después de un golpe en la cabeza, o le "
                "despierta de noche y empeora con el esfuerzo."
            ),
            "variantes": ["señales de alarma dolor de cabeza", "¿cuándo es grave el dolor de cabeza?",
                          "dolor de cabeza muy fuerte de repente", "dolor de cabeza con vómitos",
                          "banderas rojas cefalea", "¿cuándo ir a urgencias por dolor de cabeza?"],
        },
        {
            "pregunta": "¿Cómo aliviar el dolor de cabeza?",
            "respuesta": (
                "Para un dolor de cabeza común: descanse en un lugar tranquilo y con poca luz, "
                "tome bastante agua, y puede tomar un analgésico simple si no tiene "
                "contraindicaciones médicas. Si el dolor se repite seguido o no cede, consulte "
                "a su médico. Evitar el estrés, dormir bien y mantenerse hidratado ayuda a "
                "prevenir los episodios."
            ),
            "variantes": ["¿qué tomar para el dolor de cabeza?", "remedios para la jaqueca",
                          "¿cómo calmar el dolor de cabeza?", "pastilla para el dolor de cabeza"],
        },

        # ── LUMBAGO ───────────────────────────────────────────────────────────
        {
            "pregunta": "¿Qué es el lumbago?",
            "respuesta": (
                "El lumbago es el dolor en la zona baja de la espalda. Es muy frecuente y en la "
                "mayoría de los casos es de origen muscular o mecánico (mala postura, sobrecarga). "
                "Suele mejorar solo en días o semanas con movimiento suave y analgésicos simples."
            ),
            "variantes": ["me duele la espalda baja", "dolor lumbar", "¿qué es el lumbago?",
                          "dolor de espalda", "me duele la cintura", "lumbago"],
        },
        {
            "pregunta": "¿Cuándo debo consultar con urgencia por el dolor de espalda?",
            "respuesta": (
                "Consulte a su médico con urgencia si el dolor de espalda va acompañado de: "
                "una caída o golpe reciente, dolor que empeora de noche sin razón, pérdida de "
                "peso sin explicación, fiebre, debilidad o entumecimiento en las piernas. "
                "Si pierde el control de la orina o las deposiciones, acuda a urgencias de "
                "inmediato, ya que puede ser una emergencia que requiere atención urgente."
            ),
            "variantes": ["señales de alarma lumbago", "¿cuándo es grave el dolor de espalda?",
                          "dolor de espalda con fiebre", "se me duermen las piernas con el dolor de espalda",
                          "banderas rojas lumbago", "¿cuándo ir a urgencias por lumbago?"],
        },
        {
            "pregunta": "¿Cómo cuidarme si tengo lumbago?",
            "respuesta": (
                "Lo más importante es mantenerse activo según lo que tolere: el reposo prolongado "
                "en cama empeora el lumbago. Puede aplicar calor local en la zona y tomar un "
                "analgésico simple si no tiene contraindicaciones. Para prevenirlo: mantenga buena "
                "postura, fortalezca su espalda con ejercicio suave y use técnica correcta al "
                "levantar objetos pesados."
            ),
            "variantes": ["¿qué hago si me duele la espalda?", "tratamiento del lumbago",
                          "ejercicios para el lumbago", "¿qué tomar para el dolor de espalda?",
                          "¿debo hacer reposo por lumbago?"],
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
