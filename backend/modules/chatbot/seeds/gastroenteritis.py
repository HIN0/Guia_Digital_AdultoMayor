"""
Preguntas sobre gastroenteritis para adultos mayores.

Contenido enriquecido:
  - Variantes ampliadas (lenguaje coloquial chileno, errores ortográficos
    frecuentes y abreviaciones tipo WhatsApp, además de versiones formales).
  - Preguntas nuevas sobre síntomas atípicos en personas mayores (confusión,
    caídas, decaimiento) e interacción con medicamentos de uso habitual.
  - Respuestas en lenguaje simple, frases cortas, máximo 4 oraciones, sin
    recomendar dosis ni medicamentos y reforzando siempre la consulta médica.

Contexto: Chile (CESFAM, FONASA, urgencia pública, 131/SAMU).
Referencias bibliográficas: ver bloque markdown adjunto en la entrega.
"""

DATA = {
    "Urgencias y Síntomas Frecuentes": [
        {
            "pregunta": "¿Qué es la gastroenteritis?",
            "respuesta": (
                "La gastroenteritis es una infección del estómago y los intestinos. "
                "Provoca diarrea, vómitos o las dos cosas. Casi siempre la causa un "
                "virus o una bacteria (germen muy pequeño que produce infección). En "
                "general mejora sola en pocos días si descansa y toma harto líquido."
            ),
            "variantes": [
                "tengo diarrea y vómitos ¿qué tengo?",
                "¿qué es la infección intestinal?",
                "me duele la guata y tengo diarrea",
                "¿qué causa la diarrea?",
                "infección estomacal",
                "gastroenteritis aguda",
                "ke es la gastroenteritis",
                "estoy con la guata suelta",
                "ando descompuesto del estomago",
                "me hizo mal la comida y tengo diarea",
                "estoy con diarrea hace rato",
                "xq tengo diarrea y vomito",
                "me dio diarrea de repente",
                "estoy mal del estomago que sera",
                "vomito y diarrea que tengo",
                "infeccion al estomago",
                "que es una virosis estomacal",
                "sintomas de la gastroenteritis",
                "sintomas de infeccion estomacal",
                "cuales son los sintomas de la gastroenteritis",
            ],
        },
        {
            "pregunta": "¿Cuándo debo ir a urgencias por diarrea o vómitos?",
            "respuesta": (
                "Vaya a urgencias o llame al 131 si tiene la boca muy seca, orina muy "
                "poco o está confundido. En las personas mayores, la confusión puede ser "
                "la única señal de que al cuerpo le falta líquido (deshidratación). También "
                "consulte si hay sangre en las deposiciones, si los vómitos no le dejan tomar "
                "líquido o si no mejora en 2 o 3 días. Ante la duda, es mejor que lo revise "
                "un médico."
            ),
            "variantes": [
                "señales de alarma gastroenteritis",
                "¿cuándo es grave la diarrea?",
                "me desidrato con la diarrea",
                "¿cuándo llamar al médico por vómitos?",
                "sangre en deposiciones",
                "diarrea con fiebre",
                "kuando ir a urgencia por diarrea",
                "tengo diarrea y fiebre alta",
                "vomito todo lo que tomo",
                "estoy muy debil con la diarrea",
                "cuando llamar al 131 por diarrea",
                "diarrea con sangre que hago",
                "no puedo tomar agua de tanto vomitar",
                "llevo dias con diarrea y no mejoro",
                "es peligrosa la diarrea",
                "deshidratacion sintomas adulto mayor",
                "cuando ir a la urgencia por vomitos",
            ],
        },
        {
            "pregunta": "¿Cómo me cuido si tengo gastroenteritis?",
            "respuesta": (
                "Tome harto líquido en sorbos pequeños: agua o sales de rehidratación oral "
                "(sobres que reponen el líquido y las sales que se pierden). Coma de a poco "
                "cuando se sienta capaz y lávese bien las manos para no contagiar. No tome "
                "remedios para cortar la diarrea por su cuenta, sobre todo si tiene fiebre o "
                "sangre en las deposiciones. Si empeora, consulte en su CESFAM o llame al 131."
            ),
            "variantes": [
                "¿qué hago si tengo diarrea?",
                "cuidados para la gastroenteritis",
                "¿qué tomar para la diarrea?",
                "me siento mal del estómago",
                "como me cuido con diarrea",
                "ke hago si tengo diarrea y vomitos",
                "remedios caseros para la diarrea",
                "como parar la diarrea",
                "que hago para la descompostura",
                "como me mejoro de la guata",
                "puedo tomar suero para la diarrea",
                "sales de rehidratacion como se toman",
                "tratamiento gastroenteritis en casa",
                "como cuidarme en casa diarrea",
                "que hago para sentirme mejor del estomago",
            ],
        },
        {
            "pregunta": "Mi familiar mayor está confundido y con diarrea, ¿qué hago?",
            "respuesta": (
                "En las personas mayores, una infección como la gastroenteritis puede mostrarse "
                "distinta. A veces la única señal es que están más confundidos, decaídos o que "
                "se caen más seguido. Esto puede pasar porque al cuerpo le falta líquido "
                "(deshidratación). No espere a que aparezcan más síntomas: llévelo a urgencias "
                "o llame al 131 para que lo revisen pronto."
            ),
            "variantes": [
                "mi mamá está confundida y con diarrea",
                "mi papa esta raro y tiene diarrea",
                "mi familiar mayor esta decaido con diarrea",
                "el abuelo esta confundido y descompuesto",
                "diarrea y confusion en adulto mayor",
                "mi viejito anda perdido y con diarrea",
                "se cae mas seguido y tiene diarrea",
                "esta desorientado con la diarrea",
                "diarrea en anciano confundido",
                "mi mama no esta bien de la cabeza y tiene diarrea",
                "confusion por diarrea en persona mayor",
                "decaimiento y diarrea adulto mayor",
                "esta dormilon y con diarrea",
            ],
        },
        {
            "pregunta": "¿Puedo seguir tomando mis remedios si tengo diarrea y vómitos?",
            "respuesta": (
                "Es una buena pregunta para su médico, porque algunos remedios necesitan "
                "ajustarse cuando uno está con diarrea o vómitos. Por ejemplo, ciertos remedios "
                "para la presión, para la diabetes (como la metformina) o para el dolor "
                "(antiinflamatorios) pueden afectar más si el cuerpo está deshidratado. No los "
                "suspenda ni los cambie por su cuenta. Llame a su CESFAM o a su médico para que "
                "le indique qué hacer."
            ),
            "variantes": [
                "¿puedo tomar mis remedios con diarrea?",
                "tomo metformina y tengo diarrea",
                "puedo seguir con mis pastillas si vomito",
                "remedios para la presion con diarrea",
                "puedo tomar mis medicamentos con vomitos",
                "tomo remedios para la diabetes y estoy con diarrea",
                "antiinflamatorios con diarrea",
                "debo suspender mis remedios con diarrea",
                "puedo tomar mis pastillas si estoy descompuesto",
                "mis remedios y la deshidratacion",
                "tomo pastillas para la presion y vomito",
                "puedo tomar mi metformina si tengo diarrea",
                "que hago con mis remedios si estoy con diarrea",
                "sigo tomando mis remedios con vomitos y diarrea",
            ],
        },
        {
            "pregunta": "¿Qué puedo comer si tengo diarrea?",
            "respuesta": (
                "Coma de a poco y en porciones pequeñas, cuando se sienta capaz. Puede probar "
                "alimentos suaves como arroz, fideos, papas cocidas, pollo, plátano o manzana. "
                "Por unos días evite las frituras, los lácteos y las comidas muy condimentadas, "
                "porque cuestan más de digerir. Lo más importante es tomar harto líquido para "
                "no deshidratarse."
            ),
            "variantes": [
                "¿qué puedo comer con diarrea?",
                "que comida puedo comer con diarrea",
                "que puedo comer si estoy descompuesto",
                "dieta para la diarrea",
                "ke comer cuando tengo diarrea",
                "puedo comer con diarrea",
                "alimentos para la diarrea",
                "que no debo comer con diarrea",
                "puedo tomar leche con diarrea",
                "que comer para la guata mala",
                "comida blanda para la diarrea",
                "que alimentos evitar con diarrea",
                "que le doy de comer a mi mama con diarrea",
            ],
        },
        {
            "pregunta": "¿Por qué me dio gastroenteritis?",
            "respuesta": (
                "Casi siempre la causa un virus o una bacteria. Se contagia por alimentos "
                "o agua contaminada, o por contacto con personas enfermas, sobre todo a "
                "través de las manos sucias. Comer algo en mal estado o mal cocido también "
                "puede provocarla. Por eso es tan importante lavarse bien las manos y "
                "mantener buena higiene en la cocina."
            ),
            "variantes": [
                "¿qué causa la gastroenteritis?",
                "por que da la gastroenteritis",
                "de donde viene la gastroenteritis",
                "me enferme por algo que comi",
                "comi algo en mal estado y estoy con diarrea",
                "la comida puede darme diarrea",
                "el agua puede darme diarrea",
                "por que me enferme del estomago",
                "que produce la infeccion estomacal",
                "me intoxique con la comida",
                "puede ser por la comida la diarrea",
            ],
        },
        {
            "pregunta": "¿Se contagia la gastroenteritis?",
            "respuesta": (
                "Sí, muchas gastroenteritis se contagian de una persona a otra, sobre todo por "
                "las manos sucias. Para no contagiar a su familia, lávese bien las manos con "
                "agua y jabón después de ir al baño y antes de comer. Mientras esté enfermo, use "
                "su propio vaso, cubiertos y toalla. También ayuda limpiar bien el baño si hay "
                "más personas en la casa."
            ),
            "variantes": [
                "¿se contagia la gastroenteritis?",
                "la diarrea se pega",
                "se contagia la diarrea",
                "como evitar contagiar la diarrea",
                "es contagiosa la gastroenteritis",
                "mi familia se puede contagiar",
                "como no contagiar a mi familia",
                "se transmite la gastroenteritis",
                "puedo contagiar a mis nietos",
                "como evito que se contagien en casa",
                "la infeccion estomacal se pega",
                "es contagioso el vomito y la diarrea",
                "se pega la guata mala",
            ],
        },
        {
            "pregunta": "¿Cuánto dura la gastroenteritis?",
            "respuesta": (
                "La mayoría de las gastroenteritis mejoran solas en 2 a 4 días. En ese tiempo "
                "lo más importante es descansar y tomar harto líquido. Si pasan más de 3 días y "
                "no mejora, o si se siente peor, consulte en su CESFAM. Y si aparece confusión, "
                "sangre en las deposiciones o no puede tomar líquido, vaya a urgencias o llame "
                "al 131."
            ),
            "variantes": [
                "¿cuánto dura la gastroenteritis?",
                "cuanto dura la diarrea",
                "cuantos dias dura la diarrea",
                "cuando deberia mejorar",
                "cuanto tiempo dura la descompostura",
                "llevo 3 dias con diarrea es normal",
                "cuando se me va a pasar la diarrea",
                "cuanto dura el vomito y la diarrea",
                "en cuanto tiempo mejora la gastroenteritis",
                "diarrea que no se pasa",
                "cuanto demora en mejorar la guata",
                "llevo varios dias con diarrea",
                "hace cuantos dias deberia estar mejor",
            ],
        },
    ],
}