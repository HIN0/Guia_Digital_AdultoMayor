"""
Preguntas sobre hipertensión arterial (presión alta) para adultos mayores.

Contenido basado en la sección HIPERTENSIÓN ARTERIAL de data/conocimiento.txt
(misma fuente validada que usa el RAG), en lenguaje simple, frases cortas,
sin recomendar dosis ni medicamentos y reforzando siempre la consulta médica.

Nota: la pregunta "¿el dolor de cabeza es por la presión alta?" ya existe en
seeds/cefalea.py; aquí no se repite para no duplicar variantes en la whitelist.

Contexto: Chile (CESFAM, FONASA, GES, urgencia pública, 131).
"""

DATA = {
    "Hipertensión Arterial": [
        {
            "pregunta": "¿Qué es la hipertensión o presión alta?",
            "respuesta": (
                "La hipertensión es cuando la presión de la sangre dentro de las arterias "
                "está demasiado alta de forma persistente. Se considera presión alta cuando "
                "es igual o mayor a 140/90 en reposo y en más de una medición. Es muy "
                "frecuente en personas mayores y en Chile está cubierta por el GES, con "
                "copago reducido para beneficiarios de FONASA."
            ),
            "variantes": [
                "¿qué es la presión alta?",
                "que es la hipertension",
                "tengo la presion alta que significa",
                "que significa ser hipertenso",
                "me dijeron que tengo hipertension",
                "presion arterial alta que es",
                "ke es la hipertension",
                "que es tener la presion alta",
                "cuando se considera presion alta",
                "desde que valor la presion es alta",
                "soy hipertenso que significa",
                "hipertension arterial que es",
            ],
        },
        {
            "pregunta": "¿Por qué tengo que controlar la presión si me siento bien?",
            "respuesta": (
                "Porque la presión alta casi nunca da síntomas; por eso la llaman 'el "
                "asesino silencioso'. Usted puede sentirse bien aunque tenga la presión muy "
                "alta. Sin control, puede dañar el corazón, los riñones, los ojos y el "
                "cerebro, causando un infarto o un derrame. La única forma de saber si su "
                "presión está bien es medirla con regularidad."
            ),
            "variantes": [
                "¿por qué es importante controlar la presión?",
                "me siento bien igual tengo que medirme la presion",
                "para que controlar la presion",
                "que pasa si no me controlo la presion",
                "es grave la presion alta",
                "que daño hace la presion alta",
                "por que es peligrosa la hipertension",
                "la presion alta puede dar infarto",
                "la presion alta da derrame",
                "asesino silencioso presion",
                "no siento nada para que medirme la presion",
                "consecuencias de la presion alta",
            ],
        },
        {
            "pregunta": "¿Cómo se mide bien la presión?",
            "respuesta": (
                "Antes de medirla, siéntese tranquilo al menos 5 minutos, sin haber fumado, "
                "tomado café ni hecho ejercicio en la media hora anterior. La primera vez se "
                "mide en ambos brazos; después, en el que dio el valor más alto. Si se la "
                "mide en casa, anote la fecha, la hora y el valor para mostrárselos a su "
                "médico o enfermera. Un valor alto aislado no confirma hipertensión: se "
                "necesitan varias mediciones."
            ),
            "variantes": [
                "¿cómo me tomo la presión?",
                "como medir la presion en la casa",
                "como se toma bien la presion",
                "pasos para medir la presion",
                "como usar el aparato de la presion",
                "me tomo la presion y sale distinta",
                "cuando medirse la presion",
                "como saber si me tome bien la presion",
                "en que brazo se toma la presion",
                "me salio alta la presion una vez es hipertension",
                "como controlar la presion en casa",
            ],
        },
        {
            "pregunta": "¿La presión alta da síntomas?",
            "respuesta": (
                "Casi nunca. La mayoría de las personas con presión alta no siente nada. "
                "Solo una subida muy brusca y muy alta (crisis hipertensiva) puede dar dolor "
                "de cabeza muy intenso, zumbido en los oídos, visión borrosa, náuseas o "
                "confusión, y eso es una urgencia: llame al 131 o vaya a urgencias. No "
                "intente bajar la presión con medicamentos extra por su cuenta."
            ),
            "variantes": [
                "¿cómo sé si tengo la presión alta?",
                "sintomas de la presion alta",
                "que se siente cuando sube la presion",
                "como saber si ando con la presion alta",
                "señales de presion alta",
                "que es una crisis hipertensiva",
                "se me subio la presion que hago",
                "zumbido en los oidos por la presion",
                "vision borrosa por la presion",
                "como me doy cuenta si tengo hipertension",
                "la hipertension se siente",
            ],
        },
        {
            "pregunta": "¿Cuándo debo ir a urgencias por la presión alta?",
            "respuesta": (
                "Vaya a urgencias o llame al 131 si tiene la presión muy alta junto con: "
                "dolor de pecho, dificultad para respirar, dolor de cabeza muy intenso y "
                "brusco, debilidad o entumecimiento en un lado del cuerpo, o dificultad "
                "para hablar o ver. Estas pueden ser señales de un infarto o de un derrame "
                "cerebral. En esos casos no espere: busque ayuda de inmediato."
            ),
            "variantes": [
                "señales de alarma presion alta",
                "cuando es grave la presion alta",
                "presion alta con dolor de pecho",
                "banderas rojas hipertension",
                "cuando llamar al 131 por la presion",
                "se me durmio un lado del cuerpo",
                "presion alta y no puedo respirar bien",
                "presion alta y no puedo hablar bien",
                "cuando preocuparse por la presion",
                "urgencia por presion alta",
                "tengo la presion muy alta que hago",
            ],
        },
        {
            "pregunta": "¿Puedo dejar los remedios de la presión si me siento bien?",
            "respuesta": (
                "No. Los remedios para la presión deben tomarse todos los días, a la misma "
                "hora, aunque usted se sienta bien: la presión alta no da síntomas y el "
                "remedio es lo que la mantiene controlada. No los suspenda ni cambie la "
                "dosis por su cuenta. Si un remedio le cae mal, consulte a su médico o en "
                "su CESFAM antes de dejarlo, y avise siempre qué otros remedios toma."
            ),
            "variantes": [
                "¿puedo dejar de tomar el remedio de la presión?",
                "me siento bien puedo dejar las pastillas de la presion",
                "hasta cuando tomo el remedio de la presion",
                "puedo saltarme el remedio de la presion",
                "se me olvido tomar el remedio de la presion",
                "el remedio de la presion es para siempre",
                "me cae mal el remedio de la presion",
                "puedo bajar la dosis de mi remedio",
                "dejar el tratamiento de la hipertension",
                "ya tengo la presion normal dejo el remedio",
                "que pasa si dejo los remedios de la presion",
            ],
        },
        {
            "pregunta": "¿Qué puedo hacer para bajar la presión, además de los remedios?",
            "respuesta": (
                "Ayuda mucho comer con menos sal (evitar agregar sal extra, embutidos y "
                "conservas), mantener un peso saludable y caminar unos 30 minutos la mayoría "
                "de los días. También conviene no fumar, limitar el alcohol, dormir bien y "
                "manejar el estrés. Estos cambios ayudan a bajar la presión, pero no "
                "reemplazan los remedios cuando el médico ya los indicó."
            ),
            "variantes": [
                "¿cómo bajar la presión?",
                "como bajar la presion sin remedios",
                "que comer si tengo la presion alta",
                "dieta para la presion alta",
                "la sal sube la presion",
                "que alimentos evitar con hipertension",
                "sirve caminar para la presion",
                "ejercicio para la presion alta",
                "remedios caseros para la presion alta",
                "como cuidarme si soy hipertenso",
                "que hago para que no me suba la presion",
                "consejos para la presion alta",
            ],
        },
        {
            "pregunta": "¿Cada cuánto debo ir a control por la presión?",
            "respuesta": (
                "Si tiene hipertensión, debe ir a sus controles periódicos en el CESFAM "
                "aunque se sienta bien. Ahí le medirán la presión, le revisarán los "
                "medicamentos y le harán exámenes de control. Si no sabe cuándo es su "
                "próximo control, pregunte en el mesón de su CESFAM o del HUAP. Recuerde "
                "que la hipertensión está cubierta por el GES."
            ),
            "variantes": [
                "¿cada cuánto me controlo la presión?",
                "controles por hipertension",
                "cada cuanto tengo que ir al consultorio por la presion",
                "control de presion en el cesfam",
                "cuando me toca control de la presion",
                "tengo que ir a control si me siento bien",
                "donde me controlo la presion",
                "la hipertension esta en el ges",
                "el ges cubre la presion alta",
                "examenes por presion alta",
            ],
        },
    ],
}
