"""
Preguntas sobre caídas en adultos mayores.

Contenido basado en la sección CAÍDAS EN ADULTOS MAYORES de data/conocimiento.txt
(misma fuente validada que usa el RAG), en lenguaje simple, frases cortas,
sin recomendar dosis ni medicamentos y reforzando siempre la consulta médica.

Nota: "me caí y me duele la espalda" ya existe en seeds/lumbago.py; aquí las
variantes se centran en la caída en general, la fractura de cadera, el golpe
en la cabeza, la prevención y el miedo a volver a caer, sin repetir esas frases.

Contexto: Chile (CESFAM, urgencia pública, 131).
"""

DATA = {
    "Caídas en Adultos Mayores": [
        {
            "pregunta": "¿Por qué son peligrosas las caídas en las personas mayores?",
            "respuesta": (
                "Una caída puede parecer menor, pero en personas mayores puede causar "
                "fracturas (sobre todo de cadera, muñeca y columna), lesiones en la cabeza "
                "y pérdida de confianza para moverse. Con los años los huesos se vuelven "
                "más frágiles por la osteoporosis, así que incluso una caída leve puede "
                "quebrar un hueso. Por eso toda caída en una persona mayor merece atención."
            ),
            "variantes": [
                "¿son graves las caídas en los adultos mayores?",
                "por que son peligrosas las caidas",
                "que puede pasar si se cae un adulto mayor",
                "consecuencias de las caidas en ancianos",
                "es grave que se caiga una persona mayor",
                "caidas en adultos mayores",
                "por que preocupan las caidas en los abuelos",
                "que riesgo tiene una caida en un adulto mayor",
                "las caidas son peligrosas a mi edad",
            ],
        },
        {
            "pregunta": "¿Por qué se caen más las personas mayores?",
            "respuesta": (
                "Las causas más frecuentes son: debilidad en las piernas, problemas de "
                "equilibrio, visión disminuida y mareos (por medicamentos, presión baja al "
                "pararse o problemas del oído). También influyen las alfombras sueltas, el "
                "piso mojado, la mala iluminación, el calzado inadecuado y levantarse muy "
                "rápido de la cama o de una silla. Si se ha caído o siente inestabilidad, "
                "coméntelo en su CESFAM para buscar la causa."
            ),
            "variantes": [
                "¿por qué me caigo tanto?",
                "causas de las caidas en adultos mayores",
                "por que se caen los ancianos",
                "me mareo y me caigo",
                "me caigo seguido que puede ser",
                "por que pierdo el equilibrio",
                "mi papa se cae a cada rato",
                "que hace que una persona mayor se caiga",
                "los remedios pueden hacer que me caiga",
                "me tambaleo al caminar",
                "ando perdiendo el equilibrio",
            ],
        },
        {
            "pregunta": "¿Qué hago si una persona mayor se cae?",
            "respuesta": (
                "No intente levantarla de inmediato: primero vea si está consciente y si "
                "puede moverse. Si tiene dolor intenso, no puede mover un brazo o una "
                "pierna, o perdió el conocimiento aunque fuera un momento, llame al 131 o "
                "vaya a urgencias. Aunque parezca estar bien, igual debe ser evaluada "
                "pronto, sobre todo si le duele la espalda, la cadera, la muñeca o la "
                "cabeza. Un golpe en la cabeza en una persona mayor siempre merece revisión "
                "médica."
            ),
            "variantes": [
                "¿qué hago si se cae un adulto mayor?",
                "se cayo mi abuela que hago",
                "mi mama se cayo que tengo que hacer",
                "como ayudo a alguien que se cayo",
                "se cayo mi esposo lo levanto",
                "que hacer despues de una caida",
                "me cai que tengo que hacer",
                "hay que levantar altiro a alguien que se cae",
                "se golpeo la cabeza al caerse",
                "mi papa se cayo y se pego en la cabeza",
                "una persona mayor se cayo en la casa",
            ],
        },
        {
            "pregunta": "¿Cuándo debo llamar al 131 por una caída?",
            "respuesta": (
                "Llame al 131 o vaya a urgencias de inmediato si la persona: perdió el "
                "conocimiento o está confundida, no puede mover una pierna o un brazo, "
                "tiene dolor muy intenso en la cadera o la espalda, o tiene una herida con "
                "sangrado que no se detiene. Ante la duda, es mejor que la evalúen: en "
                "personas mayores una caída puede ser más seria de lo que parece."
            ),
            "variantes": [
                "señales de alarma despues de una caida",
                "cuando ir a urgencias por una caida",
                "cuando llamar la ambulancia por una caida",
                "se cayo y no se puede parar",
                "se cayo y esta confundido",
                "se cayo y no mueve el brazo",
                "se cayo y sangra mucho",
                "caida grave que hacer",
                "se cayo y perdio el conocimiento",
                "banderas rojas caidas",
            ],
        },
        {
            "pregunta": "¿Cómo saber si se quebró la cadera?",
            "respuesta": (
                "La fractura de cadera produce un dolor muy fuerte en la zona de la cadera "
                "o en la ingle, la persona no puede pararse ni caminar, y la pierna puede "
                "verse girada hacia afuera. Es una urgencia: llame al 131 o llévela a "
                "urgencias sin demorar. No intente hacerla caminar para 'probar' si está "
                "bien."
            ),
            "variantes": [
                "señales de fractura de cadera",
                "como saber si se fracturo la cadera",
                "se cayo y le duele la cadera",
                "dolor en la ingle despues de una caida",
                "se cayo y no puede caminar",
                "fractura de cadera en adulto mayor",
                "se quebro la cadera mi mama",
                "la pierna le quedo torcida despues de caerse",
                "sintomas de cadera quebrada",
                "se cayo y no se puede poner de pie",
            ],
        },
        {
            "pregunta": "¿Cómo puedo evitar las caídas en la casa?",
            "respuesta": (
                "Revise su casa: quite las alfombras sueltas y los cables del suelo, "
                "mejore la iluminación (sobre todo de noche, camino al baño) y ponga barras "
                "de apoyo en el baño y la ducha. Use calzado con suela antideslizante que "
                "sujete bien el pie, y no se levante rápido de la cama: siéntese unos "
                "segundos antes de pararse. En su CESFAM pueden orientarle sobre ejercicios "
                "para mejorar el equilibrio y la fuerza."
            ),
            "variantes": [
                "¿cómo prevenir las caídas?",
                "como evitar caerme en la casa",
                "consejos para no caerse",
                "como hacer la casa mas segura para un adulto mayor",
                "prevencion de caidas en el hogar",
                "que zapatos usar para no caerme",
                "barras de apoyo en el baño",
                "como evitar que mi mama se caiga",
                "ejercicios para el equilibrio",
                "me levanto y me mareo como lo evito",
                "como prevenir caidas en ancianos",
            ],
        },
        {
            "pregunta": "¿Qué es la osteoporosis?",
            "respuesta": (
                "La osteoporosis hace que los huesos se vuelvan más frágiles, y por eso una "
                "caída leve puede quebrarlos. Muchas personas mayores la tienen sin saberlo, "
                "porque no da síntomas hasta que ocurre una fractura. El médico puede "
                "indicar exámenes para evaluarla y, si es necesario, un tratamiento. No "
                "tome calcio ni vitamina D por su cuenta: consulte primero en su CESFAM."
            ),
            "variantes": [
                "que son los huesos fragiles",
                "por que se quiebran los huesos en los viejos",
                "tengo los huesos debiles",
                "como saber si tengo osteoporosis",
                "examen para la osteoporosis",
                "puedo tomar calcio por mi cuenta",
                "sirve la vitamina d para los huesos",
                "osteoporosis en adultos mayores",
                "los huesos se debilitan con la edad",
            ],
        },
        {
            "pregunta": "Después de caerme me da miedo caminar, ¿qué hago?",
            "respuesta": (
                "Es muy común tener miedo después de una caída, pero moverse menos debilita "
                "los músculos y aumenta el riesgo de volver a caer. No se quede sin "
                "moverse: coméntelo con el médico o la enfermera de su CESFAM, que pueden "
                "indicarle ejercicios seguros y apoyo para recuperar la confianza. Paso a "
                "paso se puede volver a caminar tranquilo."
            ),
            "variantes": [
                "me da miedo caerme de nuevo",
                "desde que me cai no quiero caminar",
                "tengo miedo de volver a caerme",
                "mi mama no quiere caminar desde que se cayo",
                "miedo a las caidas",
                "no salgo por miedo a caerme",
                "como perder el miedo a caminar",
                "despues de la caida quedo con miedo",
                "es normal tener miedo despues de una caida",
                "ando insegura al caminar despues de caerme",
            ],
        },
    ],
}
