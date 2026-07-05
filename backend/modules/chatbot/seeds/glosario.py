"""Glosario de salud: términos que las propias respuestas del bot usan
constantemente (CESFAM, FONASA, GES, 131/SAMU) y orientación sobre cuándo
ir a urgencias versus al consultorio.

Sin esto, el bot decía "consulte en su CESFAM" o "está cubierto por el GES"
pero caía al fallback si la persona preguntaba qué significan esas siglas.

Contenido respaldado por la sección GLOSARIO DE SALUD de data/conocimiento.txt
(misma fuente que usa el RAG). Contexto: Chile.
"""

DATA = {
    "Glosario de Salud": [
        {
            "pregunta": "¿Qué es el CESFAM?",
            "respuesta": (
                "El CESFAM (Centro de Salud Familiar) es el consultorio de su barrio. Ahí "
                "se hacen los controles de enfermedades crónicas (como la presión o la "
                "diabetes), se colocan las vacunas, se entregan medicamentos y se pide hora "
                "con el médico general. Cada persona se atiende en el CESFAM que corresponde "
                "a su domicilio: para inscribirse basta ir con su carnet de identidad."
            ),
            "variantes": [
                "que significa cesfam",
                "que es el consultorio",
                "cesfam que es",
                "que hacen en el cesfam",
                "para que sirve el cesfam",
                "que es un centro de salud familiar",
                "donde me inscribo en el consultorio",
                "como me inscribo en el cesfam",
                "que atienden en el consultorio",
                "cual es mi consultorio",
                "el cesfam es lo mismo que el consultorio",
            ],
        },
        {
            "pregunta": "¿Qué es FONASA?",
            "respuesta": (
                "FONASA (Fondo Nacional de Salud) es el seguro público de salud de Chile, y "
                "la mayoría de las personas mayores son beneficiarias. Con su carnet de "
                "identidad puede atenderse en el sistema público: CESFAM y hospitales. Según "
                "su tramo, muchas atenciones son gratuitas o con un copago reducido. Para "
                "conocer su tramo, pregunte en su CESFAM o revise la información oficial de "
                "FONASA."
            ),
            "variantes": [
                "que significa fonasa",
                "fonasa que es",
                "para que sirve fonasa",
                "soy de fonasa que significa",
                "que cubre fonasa",
                "como se si soy de fonasa",
                "que tramo de fonasa tengo",
                "fonasa es gratis",
                "que es el fondo nacional de salud",
                "me atienden con fonasa en el hospital",
                "sirve mi fonasa en el consultorio",
            ],
        },
        {
            "pregunta": "¿Qué es el GES o AUGE?",
            "respuesta": (
                "El GES (Garantías Explícitas en Salud), antes llamado AUGE, es un plan que "
                "garantiza por ley la atención de una lista de enfermedades, con plazos "
                "máximos y costos conocidos. Por ejemplo, la hipertensión está cubierta "
                "desde los 15 años, y el tratamiento de la neumonía en personas de 65 años "
                "y más tiene copago $0 para beneficiarios de FONASA. Si le diagnostican una "
                "enfermedad GES, en su CESFAM u hospital deben informárselo y activar la "
                "garantía."
            ),
            "variantes": [
                "que significa ges",
                "ges que es",
                "que es el auge",
                "que cubre el ges",
                "que enfermedades cubre el ges",
                "el ges y el auge son lo mismo",
                "como funciona el ges",
                "que garantias tiene el ges",
                "mi enfermedad esta en el ges",
                "el ges es gratis",
                "que es una patologia ges",
                "como se activa el ges",
            ],
        },
        {
            "pregunta": "¿Qué es el 131?",
            "respuesta": (
                "El 131 es el número de teléfono de la ambulancia (SAMU) en Chile. La "
                "llamada es gratuita y atiende las 24 horas. Llame al 131 ante una "
                "emergencia: dolor de pecho, dificultad para respirar, pérdida de "
                "conocimiento, una caída con dolor intenso, debilidad repentina en un lado "
                "del cuerpo o dificultad para hablar. Al llamar, diga con calma qué pasó y "
                "dónde está, y siga las indicaciones del operador."
            ),
            "variantes": [
                "que es el samu",
                "cual es el numero de la ambulancia",
                "como llamo una ambulancia",
                "numero de emergencia en chile",
                "a que numero llamo si hay una emergencia",
                "para que sirve el 131",
                "cuando llamar al 131",
                "el 131 es gratis",
                "que numero es la ambulancia",
                "como pido una ambulancia",
                "telefono de la ambulancia",
                "cuando debo llamar la ambulancia",
            ],
        },
        {
            "pregunta": "¿Cuándo voy a urgencias y cuándo al consultorio?",
            "respuesta": (
                "Si hay señales de alarma (dolor de pecho, falta de aire, confusión "
                "repentina, sangrado que no se detiene, o una caída con dolor fuerte), vaya "
                "a urgencias o llame al 131 sin esperar. Si la molestia no es urgente (un "
                "control, un ardor al orinar sin fiebre, un dolor que lleva días pero es "
                "soportable), consulte en su CESFAM. Y ante la duda de si es grave o no, es "
                "mejor ir a urgencias: ahí le orientarán."
            ),
            "variantes": [
                "¿voy a la urgencia o al consultorio?",
                "cuando ir a urgencias",
                "cuando ir al consultorio",
                "voy a la posta o al cesfam",
                "donde me atiendo si no es grave",
                "es mejor ir al cesfam o a la urgencia",
                "cuando corresponde ir a la urgencia",
                "para que cosas voy al consultorio",
                "no se si ir a la urgencia",
                "esto es para urgencia o consultorio",
                "donde consulto si no es una emergencia",
            ],
        },
    ],
}
