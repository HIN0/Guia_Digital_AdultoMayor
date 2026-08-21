"""
Preguntas sobre infección urinaria (ITU / cistitis) para adultos mayores.

Contenido enriquecido:
  - Variantes ampliadas (coloquial chileno, errores ortográficos comunes y
    abreviaciones tipo WhatsApp, además de versiones formales).
  - Preguntas nuevas sobre la confusión como única señal en personas mayores,
    evidencia real del arándano/cranberry, infecciones a repetición, cuidado de
    sonda vesical y adherencia a antibióticos.
  - Respuestas en lenguaje simple, frases cortas, máximo 4 oraciones, sin
    recomendar dosis ni medicamentos y reforzando siempre la consulta médica.

Contexto: Chile (CESFAM, FONASA, urgencia pública, 131).
Referencias bibliográficas: ver bloque markdown adjunto en la entrega.
"""

DATA = {
    "Urgencias y Síntomas Frecuentes": [
        {
            "pregunta": "¿Qué es la infección urinaria?",
            "respuesta": (
                "La infección urinaria (o cistitis) es una infección de la vejiga, casi "
                "siempre causada por bacterias. Es muy común en las personas mayores, sobre "
                "todo en mujeres. Suele dar ardor al orinar, ganas frecuentes de ir al baño "
                "y orina turbia o con mal olor. En las personas mayores, a veces la única "
                "señal es confusión o decaimiento, sin molestias al orinar."
            ),
            "variantes": [
                "ardor al orinar",
                "¿qué es la cistitis?",
                "infección al riñón",
                "orino seguido y me duele",
                "ITU",
                "infección urinaria",
                "¿por qué orino tanto?",
                "orina con mal olor",
                "me arde cuando hago pipi",
                "ke es la infeccion urinaria",
                "tengo infeccion a la orina",
                "me duele al orinar",
                "orina turbia y mal olor",
                "infeccion a la vejiga",
                "que es una itu",
                "sintomas de la infeccion urinaria",
                "sintomas de infeccion de orina",
                "cuales son los sintomas de la cistitis",
            ],
        },
        {
            "pregunta": "¿Cuándo debo consultar por una infección urinaria?",
            "respuesta": (
                "Consulte a su médico apenas note ardor al orinar o ganas frecuentes, para "
                "recibir tratamiento. Vaya pronto si aparece fiebre, dolor fuerte en la "
                "espalda baja o en los riñones, o confusión repentina. Esas señales pueden "
                "indicar que la infección subió al riñón, que es más serio. Si los síntomas "
                "son leves, igual consulte en su CESFAM: la infección urinaria se trata con "
                "antibióticos."
            ),
            "variantes": [
                "señales de alarma infección urinaria",
                "¿cuándo es grave la infección urinaria?",
                "me duelen los riñones",
                "fiebre con ardor al orinar",
                "cuando consultar por infeccion urinaria",
                "cuando ir al medico por la orina",
                "infeccion urinaria con fiebre",
                "me duele la espalda y orino con ardor",
                "cuando es peligrosa la cistitis",
                "infeccion urinaria subio al riñon",
                "tengo fiebre y me arde al orinar",
                "cuando ir a urgencia por infeccion urinaria",
                "dolor de riñones e infeccion",
            ],
        },
        {
            "pregunta": "¿Cómo prevenir la infección urinaria?",
            "respuesta": (
                "Tome bastante agua durante el día y no aguante las ganas de orinar. "
                "Mantenga una buena higiene en la zona íntima, limpiándose de adelante hacia "
                "atrás. Si usa sonda (un tubo que ayuda a sacar la orina), siga al pie de la "
                "letra las instrucciones de su equipo de salud. Estas medidas simples ayudan "
                "a que las bacterias no se acumulen."
            ),
            "variantes": [
                "¿cómo evitar la infección urinaria?",
                "prevención cistitis",
                "¿qué tomar para no tener infección urinaria?",
                "como prevenir la cistitis",
                "como no tener infeccion urinaria",
                "como evito la itu",
                "que hago para no infectarme la orina",
                "como cuidarme de la infeccion urinaria",
                "prevenir infeccion a la vejiga",
                "como evitar el ardor al orinar",
                "tomar agua para la infeccion urinaria",
            ],
        },
        {
            "pregunta": "Mi familiar mayor está confundido, ¿puede ser una infección urinaria?",
            "respuesta": (
                "Sí, puede ser. En las personas mayores, la infección urinaria a veces no da "
                "ardor ni ganas de orinar. La única señal puede ser que estén de repente más "
                "confundidos, decaídos o agitados. Si nota un cambio así, llévelo a que lo "
                "revisen y le tomen un examen de orina."
            ),
            "variantes": [
                "mi mamá está confundida ¿es infección urinaria?",
                "mi papa esta raro puede ser infeccion urinaria",
                "adulto mayor confundido infeccion urinaria",
                "mi viejito esta agitado sera la orina",
                "confusion en anciano por infeccion urinaria",
                "infeccion urinaria sin sintomas en adulto mayor",
                "mi mama esta decaida sera infeccion urinaria",
                "esta desorientado puede ser la orina",
                "infeccion urinaria solo con confusion",
                "mi abuelo cambio de animo sera infeccion",
                "infeccion urinaria en adulto mayor confusion",
            ],
        },
        {
            "pregunta": "¿Los hombres también tienen infección urinaria?",
            "respuesta": (
                "Sí. Aunque es más común en mujeres, los hombres mayores también pueden "
                "tenerla. Una causa frecuente es la próstata aumentada, que dificulta "
                "vaciar bien la vejiga y favorece que las bacterias se acumulen. La "
                "diabetes, la retención de orina y el uso de sonda también aumentan el "
                "riesgo. Si un hombre tiene ardor al orinar, fiebre o va al baño a cada "
                "rato, debe consultar en su CESFAM."
            ),
            "variantes": [
                "infección urinaria en hombres",
                "los hombres tienen cistitis",
                "mi esposo tiene infeccion a la orina",
                "mi papa tiene infeccion urinaria",
                "soy hombre y me arde al orinar",
                "la prostata da infeccion urinaria",
                "la prostata agrandada causa infeccion",
                "por que los hombres tienen infeccion de orina",
                "el hombre tambien se infecta la orina",
                "infeccion de orina en el hombre mayor",
                "a los hombres les da infeccion urinaria",
            ],
        },
        {
            "pregunta": "¿Sirve el arándano o cranberry para la infección urinaria?",
            "respuesta": (
                "El arándano (cranberry) podría ayudar a algunas mujeres con infecciones a "
                "repetición a tener menos episodios, pero los estudios no son claros, sobre "
                "todo en personas mayores. No sirve para curar una infección que ya tiene: "
                "para eso necesita ver al médico. Si quiere probarlo, coméntelo antes con su "
                "médico o enfermera, y nunca reemplace con él el tratamiento indicado."
            ),
            "variantes": [
                "¿sirve el cranberry para la infección urinaria?",
                "el arandano sirve para la infeccion urinaria",
                "tomar cranberry para la cistitis",
                "el jugo de arandano cura la infeccion urinaria",
                "sirven las capsulas de cranberry",
                "arandano para no tener infeccion urinaria",
                "me recomiendan el cranberry sirve",
                "el arandano rojo ayuda con la orina",
                "cranberry para infeccion urinaria a repeticion",
                "funciona el arandano para la cistitis",
            ],
        },
        {
            "pregunta": "Me da infección urinaria muy seguido, ¿por qué?",
            "respuesta": (
                "En las personas mayores hay varias razones por las que la infección urinaria "
                "se repite: cambios después de la menopausia, vaciar mal la vejiga, usar sonda "
                "o tener diabetes. Si le pasa seguido, es importante que su médico busque la "
                "causa. Mientras tanto, ayude tomando harta agua y orinando cuando tenga "
                "ganas. No use antibióticos que le sobraron de antes: cada infección debe "
                "evaluarse de nuevo."
            ),
            "variantes": [
                "¿por qué me da infección urinaria seguido?",
                "me da cistitis a cada rato",
                "infeccion urinaria a repeticion",
                "siempre tengo infeccion a la orina",
                "por que me repite la infeccion urinaria",
                "infeccion urinaria recurrente adulto mayor",
                "me da infeccion urinaria muy seguido",
                "vuelve y vuelve la infeccion urinaria",
                "por que tengo cistitis tan seguido",
                "infeccion urinaria que no se va",
            ],
        },
        {
            "pregunta": "Tengo sonda urinaria, ¿cómo la cuido para no infectarme?",
            "respuesta": (
                "Lávese bien las manos antes y después de tocar la sonda o la bolsa. Mantenga "
                "la bolsa siempre más abajo que la vejiga, para que la orina no se devuelva. "
                "No tire ni doble la sonda, y siga las indicaciones de su equipo de salud para "
                "limpiarla y cambiarla. Si aparece fiebre, orina con muy mal olor o con sangre, "
                "avise pronto en su CESFAM."
            ),
            "variantes": [
                "¿cómo cuido la sonda urinaria?",
                "tengo sonda como evito infeccion",
                "cuidado de la sonda vesical",
                "como limpiar la sonda urinaria",
                "sonda urinaria infeccion como prevenir",
                "tengo una sonda como la cuido",
                "cuidados con la sonda de la orina",
                "mi mama tiene sonda como evitamos infeccion",
                "como cuidar el cateter urinario",
                "tengo sonda en la vejiga como la cuido",
                "como evitar infeccion con la sonda",
                "cuidados de la sonda foley",
            ],
        },
        {
            "pregunta": "¿Termino los antibióticos aunque ya me sienta bien?",
            "respuesta": (
                "Sí, complete todos los días de antibiótico que le indicó el médico, aunque el "
                "ardor ya se haya quitado. Si los corta antes, la infección puede volver más "
                "fuerte. Avise a su médico si los síntomas regresan poco después de terminar "
                "el tratamiento. No guarde antibióticos ni los use por su cuenta en otra "
                "ocasión."
            ),
            "variantes": [
                "¿termino los antibióticos de la infección urinaria?",
                "puedo dejar el antibiotico si ya no me arde",
                "hasta cuando tomo el antibiotico de la cistitis",
                "ya me siento bien dejo el antibiotico",
                "tengo que terminar todo el antibiotico orina",
                "me volvio la infeccion despues del antibiotico",
                "puedo usar antibioticos que me sobraron",
                "debo completar el tratamiento de la orina",
                "los sintomas volvieron despues del antibiotico",
                "hasta cuando tomo el antibiotico de la orina",
                "puedo cortar el antibiotico antes de terminar",
            ],
        },
    ],
}
