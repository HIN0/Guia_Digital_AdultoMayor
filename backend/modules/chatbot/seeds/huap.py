"""Preguntas institucionales sobre el HUAP y la Guía Digital.

Contenido enriquecido: variantes ampliadas (coloquial chileno, errores
ortográficos comunes y abreviaciones tipo WhatsApp) y dos preguntas nuevas
de ruteo a canales oficiales (dirección/teléfono y cómo atenderse), redactadas
sin afirmar datos operativos no verificables.

IMPORTANTE: los datos institucionales (horarios, soporte) se mantienen según
lo definido por el equipo del proyecto. Deben verificarse y mantenerse al día
con la información oficial del hospital. No se incluyen referencias externas
para este módulo por tratarse de información operativa de la institución.
"""

DATA = {
    "Información General HUAP": [
        {
            "pregunta": "¿A qué hora atiende el hospital?",
            "respuesta": (
                "El hospital atiende de lunes a viernes, de 8 de la mañana a 9 de la noche. "
                "Los fines de semana, el servicio de urgencias atiende las 24 horas. Si tiene "
                "una emergencia fuera del horario de atención, vaya a la urgencia más cercana "
                "o llame al 131. Para confirmar los horarios, también puede preguntar en el "
                "mesón de atención del hospital."
            ),
            "variantes": [
                "¿a qué hora atienden?",
                "horario del HUAP",
                "¿cuándo está abierto el hospital?",
                "¿atienden los fines de semana?",
                "¿a qué hora abren?",
                "¿hasta qué hora atienden?",
                "horario de atencion",
                "a que hora cierran",
                "atienden el sabado",
                "el hospital abre los domingos",
                "cual es el horario",
                "hasta que hora estan abiertos",
                "atienden de noche",
                "que dias atienden",
            ],
        },
        {
            "pregunta": "¿Qué es la Guía Digital del HUAP?",
            "respuesta": (
                "La Guía Digital del HUAP es una plataforma educativa en línea pensada para "
                "las personas mayores. Ofrece lecciones simples sobre tecnología, salud y "
                "bienestar. Cada tema trae texto, imágenes y audio para que sea fácil de "
                "seguir. La idea es que usted aprenda a su ritmo, paso a paso."
            ),
            "variantes": [
                "¿qué es esta aplicación?",
                "¿qué es la guía digital?",
                "¿para qué sirve esta plataforma?",
                "¿qué es esta página?",
                "que es esto",
                "para que sirve la guia digital",
                "que es esta app",
                "de que se trata esta plataforma",
                "que puedo hacer aqui",
                "que es la guia del huap",
                "para que es esta pagina",
            ],
        },
        {
            "pregunta": "¿A quién pido ayuda si tengo problemas con la plataforma?",
            "respuesta": (
                "Si tiene problemas para entrar a la plataforma, puede acercarse al mesón de "
                "atención del HUAP, de lunes a viernes de 8:00 a 17:00 horas. También puede "
                "llamar al número de soporte que aparece en su tarjeta de atención. Si no "
                "encuentra el número, pregunte en el mesón y le ayudarán. No se preocupe: "
                "siempre hay alguien para apoyarle."
            ),
            "variantes": [
                "soporte técnico",
                "no puedo entrar a la plataforma",
                "¿a quién llamo si tengo problemas?",
                "ayuda con la aplicación",
                "tengo problemas para entrar",
                "no me deja entrar",
                "no funciona la plataforma",
                "como pido ayuda con la app",
                "no puedo iniciar sesion",
                "tengo un problema tecnico",
                "a quien le pido ayuda",
                "se me cayo la pagina",
            ],
        },
        {
            "pregunta": "¿Cuál es la dirección o el teléfono del hospital?",
            "respuesta": (
                "Para tener la dirección y los teléfonos correctos y al día del HUAP, lo mejor "
                "es revisar la información oficial del hospital o preguntar en el mesón de "
                "atención. Así se asegura de no usar datos antiguos. Si necesita ayuda urgente, "
                "recuerde que puede llamar al 131. Para trámites, su CESFAM también puede "
                "orientarle."
            ),
            "variantes": [
                "¿dónde queda el hospital?",
                "direccion del huap",
                "telefono del hospital",
                "donde esta el huap",
                "como llego al hospital",
                "cual es el telefono del huap",
                "donde queda la posta",
                "numero de telefono del hospital",
                "direccion del hospital",
                "como contacto al hospital",
            ],
        },
        {
            "pregunta": "¿Cómo me atiendo o pido una hora en el hospital?",
            "respuesta": (
                "Para saber cómo atenderse o pedir una hora, consulte directamente en el HUAP "
                "o en su CESFAM, según corresponda a su caso. Ellos le dirán los pasos exactos "
                "y los documentos que necesita. Si es una urgencia, no espere una hora: acuda a "
                "la urgencia o llame al 131. Tener a mano su carnet y sus datos de FONASA "
                "facilita el trámite."
            ),
            "variantes": [
                "¿cómo pido una hora?",
                "como me atiendo en el hospital",
                "como saco hora",
                "como me atienden en el huap",
                "necesito una hora medica",
                "como pido atencion",
                "como reservo una hora",
                "donde pido hora",
                "como me toman",
                "quiero atenderme en el hospital",
            ],
        },
    ],
}