"""
Preguntas sobre lumbago y dolor de espalda para adultos mayores.

Contenido enriquecido:
  - Variantes ampliadas (coloquial chileno, errores ortográficos comunes y
    abreviaciones tipo WhatsApp, además de versiones formales).
  - Preguntas nuevas sobre la caída y la fractura por osteoporosis en personas
    mayores, el mito del reposo en cama, calor versus frío, la interacción de
    antiinflamatorios con otros remedios y la ciática.
  - Respuestas en lenguaje simple, frases cortas, máximo 4 oraciones, sin
    recomendar dosis ni medicamentos y reforzando siempre la consulta médica.

Contexto: Chile (CESFAM, FONASA, urgencia pública, 131).
Referencias bibliográficas: ver bloque markdown adjunto en la entrega.
"""

DATA = {
    "Urgencias y Síntomas Frecuentes": [
        {
            "pregunta": "¿Qué es el lumbago?",
            "respuesta": (
                "El lumbago es el dolor en la parte baja de la espalda. Es muy común y casi "
                "siempre es muscular o por sobrecarga (mala postura, hacer fuerza o un mal "
                "movimiento). Por lo general mejora solo en días o pocas semanas. Lo que más "
                "ayuda es seguir moviéndose con suavidad."
            ),
            "variantes": [
                "me duele la espalda baja",
                "dolor lumbar",
                "¿qué es el lumbago?",
                "dolor de espalda",
                "me duele la cintura",
                "lumbago",
                "me duele la parte baja de la espalda",
                "ke es el lumbago",
                "dolor en los riñones por la espalda",
                "me duele la espalda hace dias",
                "tengo lumbago que es",
                "dolor de espalda baja causas",
                "me duele la zona lumbar",
                "que es el dolor lumbar",
            ],
        },
        {
            "pregunta": "¿Cuándo debo consultar con urgencia por el dolor de espalda?",
            "respuesta": (
                "Consulte pronto si el dolor de espalda viene con fiebre, baja de peso sin "
                "explicación, o si empeora de noche sin razón. También si después de una caída "
                "o un golpe el dolor es fuerte, o si siente debilidad o que se le duermen las "
                "piernas. Si pierde el control de la orina o las deposiciones, vaya a urgencias "
                "de inmediato: puede ser una emergencia. Ante la duda, es mejor que lo revise "
                "un médico."
            ),
            "variantes": [
                "señales de alarma lumbago",
                "¿cuándo es grave el dolor de espalda?",
                "dolor de espalda con fiebre",
                "se me duermen las piernas con el dolor de espalda",
                "banderas rojas lumbago",
                "¿cuándo ir a urgencias por lumbago?",
                "dolor de espalda con baja de peso",
                "dolor de espalda que empeora de noche",
                "cuando consultar por dolor de espalda",
                "dolor de espalda y no controlo la orina",
                "debilidad en las piernas con dolor de espalda",
                "cuando es peligroso el dolor de espalda",
                "dolor de espalda despues de una caida",
            ],
        },
        {
            "pregunta": "¿Cómo cuidarme si tengo lumbago?",
            "respuesta": (
                "Lo más importante es mantenerse activo según lo que aguante: quedarse mucho "
                "rato en cama empeora el lumbago. Puede aplicar calor en la zona y tomar un "
                "analgésico simple si su médico no se lo ha prohibido. Para prevenirlo, cuide "
                "la postura, haga ejercicio suave para la espalda y agáchese doblando las "
                "rodillas al levantar peso. Si el dolor no mejora en unas semanas, consulte en "
                "su CESFAM."
            ),
            "variantes": [
                "¿qué hago si me duele la espalda?",
                "tratamiento del lumbago",
                "ejercicios para el lumbago",
                "¿qué tomar para el dolor de espalda?",
                "¿debo hacer reposo por lumbago?",
                "como me cuido con lumbago",
                "como aliviar el dolor de espalda",
                "que hago para el dolor lumbar",
                "como mejorar el lumbago en casa",
                "que ejercicios sirven para la espalda",
                "como cuidar la espalda baja",
            ],
        },
        {
            "pregunta": "Me caí y ahora me duele la espalda, ¿qué hago?",
            "respuesta": (
                "Después de una caída, un dolor de espalda en una persona mayor merece que lo "
                "revise un médico. Con los años los huesos se vuelven más frágiles "
                "(osteoporosis) y a veces una caída puede quebrar una vértebra, aunque parezca "
                "un golpe leve. No se automedique solo para aguantar el dolor. Acuda a su "
                "CESFAM o a urgencias para que lo evalúen, sobre todo si el dolor es fuerte o "
                "no puede moverse bien."
            ),
            "variantes": [
                "me caí y me duele la espalda",
                "me cai y me duele la cintura",
                "dolor de espalda despues de caerme",
                "me golpee la espalda en una caida",
                "mi mama se cayo y le duele la espalda",
                "me duele la espalda tras una caida",
                "caida y dolor de espalda adulto mayor",
                "me cai y no puedo enderezarme",
                "dolor de espalda fuerte despues de un golpe",
                "sera una fractura por la caida",
                "me caí y me duele la espalda baja",
            ],
        },
        {
            "pregunta": "¿Tengo que hacer reposo en cama por el lumbago?",
            "respuesta": (
                "No. Antes se creía que había que quedarse en cama, pero hoy se sabe que el "
                "reposo largo empeora el lumbago. Lo mejor es seguir moviéndose con suavidad y "
                "hacer sus actividades según lo que tolere. Quédese en cama solo si el dolor es "
                "muy fuerte, y por poco tiempo. Volver de a poco al movimiento ayuda a sanar "
                "más rápido."
            ),
            "variantes": [
                "¿tengo que hacer reposo por el lumbago?",
                "debo quedarme en cama por el dolor de espalda",
                "hago reposo o me muevo con el lumbago",
                "el reposo es bueno para la espalda",
                "tengo que estar en cama por el lumbago",
                "me conviene descansar o caminar con lumbago",
                "reposo en cama dolor de espalda",
                "puedo moverme con dolor de espalda",
                "es malo quedarse en cama con lumbago",
                "cuanto reposo necesito por el lumbago",
            ],
        },
        {
            "pregunta": "¿Me pongo calor o frío en la espalda?",
            "respuesta": (
                "Para el lumbago muscular, el calor suele ser lo más cómodo: relaja los "
                "músculos y alivia. Puede usar una bolsa de agua caliente o una compresa tibia "
                "por ratos, con cuidado de no quemarse la piel. Algunas personas sienten alivio "
                "con frío justo después de un golpe o un tirón. Use lo que mejor le resulte, sin "
                "aplicarlo directo sobre la piel ni por mucho rato seguido."
            ),
            "variantes": [
                "¿calor o frío para la espalda?",
                "me pongo calor o hielo en la espalda",
                "que es mejor calor o frio para el lumbago",
                "bolsa de agua caliente para la espalda",
                "hielo o calor para el dolor lumbar",
                "compresa caliente para la espalda",
                "me pongo frio o calor en la cintura",
                "calor para el dolor de espalda sirve",
                "que aplico en la espalda calor o frio",
                "me pongo hielo en la espalda",
                "sirve el calor para el lumbago",
                "frio o calor para la espalda baja",
            ],
        },
        {
            "pregunta": "¿Puedo tomar un antiinflamatorio para la espalda si tomo otros remedios?",
            "respuesta": (
                "Es mejor consultarlo antes con su médico o farmacéutico. Los antiinflamatorios "
                "pueden afectar el estómago, la presión y los riñones, sobre todo en personas "
                "mayores o que toman remedios para la presión o la diabetes. No los tome por su "
                "cuenta varios días seguidos ni junte distintos calmantes. En su CESFAM o "
                "farmacia le pueden indicar cuál es seguro para usted."
            ),
            "variantes": [
                "¿puedo tomar antiinflamatorio para la espalda?",
                "puedo tomar antiinflamatorio con mis remedios",
                "tomo remedios para la presion puedo tomar antiinflamatorio para la espalda",
                "que tomo para el dolor de espalda si tomo otros remedios",
                "es seguro el antiinflamatorio con mis pastillas",
                "puedo tomar calmante para la espalda con mis remedios",
                "antiinflamatorio para el lumbago es seguro",
                "tomo metformina puedo tomar antiinflamatorio",
                "puedo mezclar el antiinflamatorio con mis remedios",
                "que calmante puedo tomar para la espalda",
            ],
        },
        {
            "pregunta": "El dolor de espalda me baja por la pierna, ¿qué es?",
            "respuesta": (
                "Cuando el dolor baja desde la espalda por la parte de atrás de la pierna, "
                "suele llamarse ciática. Pasa cuando un nervio de la zona baja de la espalda se "
                "irrita o queda apretado. Muchas veces mejora solo con movimiento suave y "
                "tiempo. Pero si siente mucha debilidad en la pierna, se le duerme, o pierde el "
                "control de la orina, consulte pronto o vaya a urgencias."
            ),
            "variantes": [
                "el dolor me baja por la pierna",
                "dolor de espalda que se va a la pierna",
                "me duele la espalda y la pierna",
                "que es la ciatica",
                "dolor que baja por la pierna desde la espalda",
                "se me irradia el dolor a la pierna",
                "tengo ciatica",
                "dolor de espalda y hormigueo en la pierna",
                "el dolor de espalda llega hasta el pie",
                "me duele la espalda baja y la pierna",
            ],
        },
    ],
}