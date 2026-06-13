"""Información institucional del HUAP: horarios, guía digital, soporte."""

DATA = {
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
