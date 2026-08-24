"""Preguntas generales: saludos, despedidas, identidad del bot,
medicamentos (derivación al médico) y ayuda de uso.

Contenido enriquecido: variantes ampliadas (coloquial chileno, errores
ortográficos comunes y abreviaciones tipo WhatsApp) y dos preguntas nuevas:
ruta de emergencia (131) y aclaración de que el bot no reemplaza al médico.
Se mantiene intacta la derivación de medicamentos como pilar de seguridad.
Referencias bibliográficas: ver bloque markdown adjunto en la entrega.
"""

SALUDO_FIJO = "Hola. Estoy aquí para responder preguntas sobre salud. ¿En qué puedo ayudarte?"

DATA = {
    "General": [
        {
            "pregunta": "hola",
            "respuesta": SALUDO_FIJO,
            "variantes": ["buenos días", "buenas tardes", "buenas noches",
                          "hola, ¿cómo estás?", "qué tal", "aló", "hola bot",
                          "holaa", "buenas", "ola", "hola que tal", "buen dia",
                          "estimado", "hola asistente", "ke tal"],
        },
        {
            "pregunta": "gracias",
            "respuesta": "De nada. Si tiene otra pregunta sobre salud, estoy aquí para ayudarle.",
            "variantes": ["muchas gracias", "se agradece", "gracias por la ayuda",
                          "muy amable", "ok gracias", "graciaa", "mil gracias",
                          "gracias totales", "te pasaste gracias", "muchas grasias",
                          "ya gracias", "perfecto gracias", "buenisimo gracias",
                          "se lo agradezco", "gracias por la informacion",
                          "muchas gracias por su ayuda", "gracias eso queria saber",
                          "excelente gracias", "me sirvio mucho gracias"],
        },
        {
            "pregunta": "adiós",
            "respuesta": "Hasta pronto. Cuídese mucho y recuerde asistir a sus controles médicos.",
            "variantes": ["chao", "hasta luego", "nos vemos", "me voy", "eso era todo",
                          "chau", "adios", "hasta pronto", "me despido", "gracias chao",
                          "nos vemos luego", "hasta la proxima", "ya me voy",
                          "chaito", "chao chao", "que este bien", "cuidese",
                          "hasta mañana", "me retiro", "un gusto hasta luego",
                          "listo eso era", "ya eso seria todo"],
        },
        {
            "pregunta": "¿qué puedes hacer?",
            "respuesta": (
                "Puedo responder sus preguntas sobre salud: presión alta, caídas, "
                "gastroenteritis, neumonía, infección urinaria, dolor de cabeza y lumbago. "
                "También le explico términos como CESFAM, FONASA o GES, le oriento sobre "
                "cuándo ir a urgencias o llamar al 131, y le doy información del HUAP. "
                "¿Sobre qué le gustaría saber?"
            ),
            "variantes": ["¿para qué sirves?", "¿en qué me puedes ayudar?",
                          "¿qué sabes hacer?", "ayuda", "¿qué preguntas puedo hacer?",
                          "que haces", "para que sirve esto", "en que me ayudas",
                          "que cosas sabes", "que me puedes responder",
                          "sobre que puedo preguntar", "que temas manejas",
                          "que puedo preguntarte", "ayudame",
                          "menu", "opciones", "que temas cubres",
                          "de que puedo hablar contigo", "muestrame los temas",
                          "que informacion tienes", "lista de temas"],
        },
        {
            "pregunta": "¿quién eres?",
            "respuesta": (
                "Soy el asistente virtual de la Guía Digital del HUAP. Estoy aquí para "
                "responder sus preguntas sobre salud con información validada por el "
                "hospital. Recuerde que no reemplazo a su médico: ante cualquier duda sobre "
                "su salud personal, consulte siempre con un profesional."
            ),
            "variantes": ["¿eres una persona?", "¿eres un robot?", "¿con quién hablo?",
                          "¿eres de verdad?", "¿quién me responde?", "eres humano",
                          "quien me habla", "que eres", "eres una maquina",
                          "con quien estoy hablando", "eres real", "eres un bot",
                          "quien eres tu"],
        },
        {
            "pregunta": "¿Qué medicamento debo tomar?",
            "respuesta": (
                "No puedo recomendar medicamentos ni dosis, porque eso depende de la "
                "situación de cada persona. Tomar remedios por cuenta propia puede ser "
                "riesgoso, sobre todo en personas mayores que ya usan varios fármacos. Por "
                "favor, consulte siempre con su médico o enfermera de cabecera antes de "
                "tomar, cambiar o dejar cualquier medicamento."
            ),
            "variantes": ["¿qué remedio me sirve?", "¿cuánta dosis debo tomar?",
                          "¿puedo dejar de tomar mi remedio?", "¿qué pastilla es buena para el dolor?",
                          "¿me puedes recetar algo?", "¿puedo tomar este remedio?",
                          "que remedio me tomo", "que pastilla me sirve",
                          "cuanto debo tomar de este remedio", "me recomiendas un remedio",
                          "que medicamento es bueno", "puedo tomar mas dosis",
                          "que me tomo para esto", "dame una receta", "que antibiotico tomo"],
        },
        {
            "pregunta": "no entiendo",
            "respuesta": (
                "No se preocupe, estoy aquí para ayudarle. Intente escribir su pregunta con "
                "otras palabras, de forma simple. Por ejemplo: '¿Qué es la gastroenteritis?' "
                "o '¿A qué hora atiende el hospital?'"
            ),
            "variantes": ["no entendí", "no me quedó claro", "¿me puedes explicar de nuevo?",
                          "no sé cómo preguntar", "estoy perdido", "no entiendo nada",
                          "no cacho", "no comprendo", "me lo repites", "no te entiendo",
                          "explicame de nuevo", "no entendi nada", "no se que preguntar"],
        },
        {
            "pregunta": "Me siento muy mal, creo que es una emergencia",
            "respuesta": (
                "Si cree que es una emergencia, no espere: llame de inmediato al 131 (la "
                "ambulancia, SAMU) o vaya a la urgencia más cercana. Yo solo doy información "
                "general y no puedo atender emergencias. Si está con otra persona, pídale "
                "ayuda ahora mismo. Su salud es lo primero."
            ),
            "variantes": ["me siento muy mal", "creo que es una emergencia",
                          "necesito ayuda urgente", "es una emergencia",
                          "me siento muy mal ahora", "ayuda urgente", "estoy muy mal",
                          "me estoy sintiendo pesimo", "creo que me va a pasar algo",
                          "es urgente", "me siento grave", "necesito un doctor ahora",
                          "auxilio"],
        },
        {
            "pregunta": "¿Reemplazas al médico?",
            "respuesta": (
                "No, no reemplazo a su médico ni a su enfermera. Le doy información general "
                "validada para orientarle, pero no puedo examinarle ni darle un diagnóstico. "
                "Ante cualquier duda sobre su salud, consulte siempre con un profesional. "
                "Para eso están su CESFAM y el sistema de salud."
            ),
            "variantes": ["¿reemplazas al médico?", "esto reemplaza al doctor",
                          "eres mi medico", "puedo dejar de ir al medico",
                          "me sirves en vez del medico", "esto es como ir al doctor",
                          "ya no necesito ir al medico", "reemplazas al doctor",
                          "puedo confiar en ti en vez del medico", "esto es un diagnostico"],
        },
    ],
}
