"""
Preguntas sobre cefalea y dolor de cabeza para adultos mayores.

Contenido enriquecido:
  - Variantes ampliadas (coloquial chileno, errores ortográficos comunes y
    abreviaciones tipo WhatsApp, además de versiones formales).
  - Preguntas nuevas sobre la creencia de que el dolor de cabeza es por la
    presión, el sobreuso de analgésicos (dolor de rebote), la interacción de
    calmantes con otros remedios, la cefalea tensional y la prevención.
  - Respuestas en lenguaje simple, frases cortas, máximo 4 oraciones, sin
    recomendar dosis ni medicamentos y reforzando siempre la consulta médica.

Contexto: Chile (CESFAM, FONASA, urgencia pública, 131).
Referencias bibliográficas: ver bloque markdown adjunto en la entrega.
"""

DATA = {
    "Urgencias y Síntomas Frecuentes": [
        {
            "pregunta": "¿Por qué me duele la cabeza?",
            "respuesta": (
                "El dolor de cabeza (cefalea) es un síntoma, no una enfermedad. Las causas "
                "más comunes son la tensión muscular, el estrés, el cansancio, la falta de "
                "sueño o no tomar suficiente agua. La gran mayoría de los dolores de cabeza "
                "no son graves. Aun así, conviene conocer las señales de alarma para saber "
                "cuándo consultar."
            ),
            "variantes": [
                "me duele la cabeza",
                "dolor de cabeza frecuente",
                "¿qué es la cefalea?",
                "tengo jaqueca",
                "migraña",
                "cefalea",
                "¿por qué tengo dolor de cabeza?",
                "me duele la cabeza seguido",
                "ke es la jaqueca",
                "por que me duele tanto la cabeza",
                "tengo migraña que es",
                "me duele la cabeza hace dias",
                "siempre me duele la cabeza",
                "dolor de cabeza causas",
                "que es un dolor de cabeza",
            ],
        },
        {
            "pregunta": "¿Cuándo es peligroso el dolor de cabeza?",
            "respuesta": (
                "Vaya a urgencias o llame al 131 si el dolor aparece de golpe y es el más "
                "fuerte de su vida, o si viene con fiebre y el cuello duro. También si le da "
                "debilidad, dificultad para hablar o para ver, o si empezó después de un golpe "
                "en la cabeza. Es señal de alarma cuando es la primera vez que le da un dolor "
                "así después de los 50 años o si lo despierta de noche. En estos casos no "
                "espere y busque ayuda médica de inmediato."
            ),
            "variantes": [
                "señales de alarma dolor de cabeza",
                "¿cuándo es grave el dolor de cabeza?",
                "dolor de cabeza muy fuerte de repente",
                "dolor de cabeza con vómitos",
                "banderas rojas cefalea",
                "¿cuándo ir a urgencias por dolor de cabeza?",
                "el peor dolor de cabeza de mi vida",
                "dolor de cabeza con fiebre y cuello tieso",
                "cuando preocuparse por dolor de cabeza",
                "dolor de cabeza despues de un golpe",
                "dolor de cabeza con debilidad en un lado",
                "me duele la cabeza y no puedo hablar bien",
                "dolor de cabeza me despierta de noche",
                "cuando llamar al 131 por dolor de cabeza",
            ],
        },
        {
            "pregunta": "¿Cómo aliviar el dolor de cabeza?",
            "respuesta": (
                "Para un dolor de cabeza común: descanse en un lugar tranquilo y con poca luz, "
                "y tome agua. Puede tomar un analgésico simple si su médico no se lo ha "
                "prohibido. Si el dolor se repite muy seguido o no se pasa, consulte en su "
                "CESFAM. Dormir bien, mantenerse hidratado y evitar el estrés ayuda a que "
                "aparezca menos."
            ),
            "variantes": [
                "¿qué tomar para el dolor de cabeza?",
                "remedios para la jaqueca",
                "¿cómo calmar el dolor de cabeza?",
                "pastilla para el dolor de cabeza",
                "como aliviar el dolor de cabeza",
                "que hago para que se me pase la jaqueca",
                "como quitar el dolor de cabeza",
                "remedio casero para el dolor de cabeza",
                "como calmar la migraña",
                "que me tomo para la cabeza",
                "como hacer que se pase el dolor de cabeza",
            ],
        },
        {
            "pregunta": "¿El dolor de cabeza es por la presión alta?",
            "respuesta": (
                "Casi nunca. La presión alta (hipertensión) en general no da síntomas; por "
                "eso la llaman 'el asesino silencioso'. Solo una subida muy brusca y muy alta "
                "de la presión puede dar dolor de cabeza, y eso es una urgencia. La única "
                "forma de saber cómo está su presión es medirla, no por cómo se siente, así "
                "que no deje de controlarla."
            ),
            "variantes": [
                "¿el dolor de cabeza es por la presión?",
                "me duele la cabeza sera la presion alta",
                "dolor de cabeza por presion",
                "tengo la presion alta por eso me duele la cabeza",
                "el dolor de cabeza significa presion alta",
                "cefalea e hipertension",
                "me duele la cabeza tendre la presion alta",
                "dolor de cabeza presion arterial",
                "si me duele la cabeza es presion",
                "la presion me da dolor de cabeza",
                "como saber si el dolor es por la presion",
            ],
        },
        {
            "pregunta": "Tomo muchos analgésicos para la cabeza, ¿es malo?",
            "respuesta": (
                "Sí, puede ser un problema. Cuando se toman calmantes para la cabeza muchos "
                "días a la semana, el cuerpo se acostumbra y el dolor puede volver más seguido "
                "(se llama dolor de rebote). Por eso no conviene automedicarse todos los días. "
                "Si necesita calmantes muy seguido, consulte en su CESFAM para buscar la causa "
                "y un mejor tratamiento."
            ),
            "variantes": [
                "tomo muchos analgésicos para la cabeza",
                "es malo tomar tantos calmantes",
                "tomo paracetamol todos los dias",
                "abuso de calmantes para la cabeza",
                "tomo muchas pastillas para el dolor de cabeza",
                "el calmante ya no me hace efecto",
                "dolor de cabeza por tomar tantos remedios",
                "es malo tomar analgesicos seguido",
                "me tomo calmantes todos los dias para la cabeza",
                "dolor de rebote por calmantes",
                "tomo muchos remedios para la jaqueca es malo",
            ],
        },
        {
            "pregunta": "¿Puedo tomar un analgésico si tomo remedios para la presión o la diabetes?",
            "respuesta": (
                "Es mejor preguntárselo a su médico o a su farmacéutico antes. Algunos "
                "calmantes, como los antiinflamatorios, pueden subir la presión o afectar los "
                "riñones, sobre todo si toma remedios para la presión o tiene diabetes. No "
                "mezcle remedios por su cuenta ni repita dosis. En su CESFAM o farmacia le "
                "pueden decir cuál es seguro para usted."
            ),
            "variantes": [
                "¿puedo tomar analgésico con mis remedios?",
                "puedo tomar calmante si tomo remedios para la presion",
                "tomo remedios para la presion puedo tomar antiinflamatorio",
                "puedo tomar paracetamol con mis remedios",
                "calmante para la cabeza con remedios para la diabetes",
                "puedo mezclar el calmante con mis pastillas",
                "es seguro tomar antiinflamatorio con mis remedios",
                "que calmante puedo tomar si soy hipertenso",
                "tomo metformina puedo tomar calmante para la cabeza",
                "puedo tomar remedio para el dolor con mis otros remedios",
            ],
        },
        {
            "pregunta": "Me duele la cabeza por tensión o por el cuello, ¿qué hago?",
            "respuesta": (
                "El dolor de cabeza por tensión es el más común y se siente como una banda "
                "apretada alrededor de la cabeza. Suele venir del estrés o de tener tensos los "
                "músculos del cuello y los hombros. Puede ayudar descansar, soltar los "
                "hombros, aplicar calor en el cuello y dormir bien. Si el dolor es muy seguido "
                "o no mejora, consulte en su CESFAM."
            ),
            "variantes": [
                "me duele la cabeza por el cuello",
                "dolor de cabeza por tension",
                "cefalea tensional",
                "dolor de cabeza por estres",
                "me duele la cabeza y el cuello",
                "dolor de cabeza como banda apretada",
                "tengo la cabeza apretada por tension",
                "dolor de cabeza por contractura del cuello",
                "me duele la nuca y la cabeza",
                "dolor de cabeza por estar tenso",
                "dolor de cabeza por los hombros tensos",
            ],
        },
        {
            "pregunta": "¿Cómo puedo prevenir los dolores de cabeza?",
            "respuesta": (
                "Ayuda mucho cuidar las rutinas: dormir bien, tomar agua durante el día y no "
                "saltarse comidas. Trate de manejar el estrés y descansar la vista si pasa "
                "mucho rato leyendo o en el celular. Si nota que algo en especial le gatilla "
                "el dolor, anótelo para evitarlo. Si los dolores son frecuentes, su médico "
                "puede ayudarle a prevenirlos mejor."
            ),
            "variantes": [
                "¿cómo prevenir el dolor de cabeza?",
                "como evitar los dolores de cabeza",
                "como prevenir la jaqueca",
                "que hago para que no me duela la cabeza",
                "como evitar la migraña",
                "prevenir dolor de cabeza frecuente",
                "como tener menos dolores de cabeza",
                "que hago para no tener jaqueca",
                "como evito que me duela la cabeza tan seguido",
                "consejos para prevenir el dolor de cabeza",
            ],
        },
    ],
}