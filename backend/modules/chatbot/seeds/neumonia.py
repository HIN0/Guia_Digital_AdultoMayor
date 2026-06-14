"""
Preguntas sobre neumonía para adultos mayores.

Contenido enriquecido:
  - Variantes ampliadas (coloquial chileno, errores ortográficos comunes y
    abreviaciones tipo WhatsApp, además de versiones formales).
  - Preguntas nuevas sobre presentación atípica en personas mayores (confusión,
    caídas, decaimiento), diferencia con resfrío, vacunación gratuita (PNI),
    recuperación y adherencia a antibióticos.
  - Respuestas en lenguaje simple, frases cortas, máximo 4 oraciones, sin
    recomendar dosis ni medicamentos y reforzando siempre la consulta médica.

Contexto: Chile (CESFAM, FONASA, GES neumonía 65+, PNI, urgencia pública, 131).
Referencias bibliográficas: ver bloque markdown adjunto en la entrega.
"""

DATA = {
    "Urgencias y Síntomas Frecuentes": [
        {
            "pregunta": "¿Qué es la neumonía?",
            "respuesta": (
                "La neumonía es una infección de los pulmones, causada por bacterias o "
                "virus. Provoca tos con flemas, fiebre y dificultad para respirar. En las "
                "personas mayores puede verse distinta: a veces solo hay confusión, "
                "decaimiento o caídas, y puede no haber fiebre. Por eso conviene estar "
                "atento a cualquier cambio brusco en una persona mayor."
            ),
            "variantes": [
                "¿qué es una pulmonía?",
                "me diagnosticaron neumonía",
                "infección pulmonar",
                "pulmonía",
                "ke es la neumonia",
                "que es la neumonia",
                "tengo neumonia que significa",
                "que es una infeccion al pulmon",
                "me dijeron que tengo pulmonia",
                "neumonia en adulto mayor que es",
                "que es la bronconeumonia",
                "tos con flema y fiebre que sera",
                "diferencia entre neumonia y pulmonia",
                "que significa tener neumonia",
            ],
        },
        {
            "pregunta": "¿Cuándo debo ir a urgencias por la tos o dificultad para respirar?",
            "respuesta": (
                "Vaya a urgencias o llame al 131 de inmediato si le cuesta mucho respirar, "
                "si los labios o las uñas se ponen azulados, o si aparece confusión de "
                "repente. También si respira muy rápido o está muy decaído. Estas son "
                "señales de que los pulmones no reciben suficiente oxígeno. No espere: en "
                "estos casos la atención rápida puede salvar la vida."
            ),
            "variantes": [
                "me cuesta respirar ¿qué hago?",
                "señales de alarma neumonía",
                "¿cuándo es grave la tos?",
                "dificultad para respirar urgencias",
                "me ahogo",
                "falta de aire",
                "me falta el aire que hago",
                "labios morados y me cuesta respirar",
                "cuando ir a urgencia por neumonia",
                "respiro muy rapido y me canso",
                "no puedo respirar bien",
                "tengo los labios azules",
                "cuando llamar al 131 por falta de aire",
                "me agito mucho al respirar",
                "dificultad para respirar adulto mayor",
            ],
        },
        {
            "pregunta": "¿Cómo prevenir la neumonía?",
            "respuesta": (
                "Lo más importante es vacunarse: la vacuna contra la neumonía "
                "(antineumocócica) y la vacuna contra la influenza todos los años. En Chile "
                "son gratis en su CESFAM para las personas de 65 años y más. También ayuda "
                "no fumar, lavarse seguido las manos y abrigarse en invierno. Pregunte en su "
                "consultorio cuándo le toca su vacuna."
            ),
            "variantes": [
                "vacuna contra la neumonía",
                "¿cómo evitar la pulmonía?",
                "prevención neumonía adulto mayor",
                "¿me debo vacunar contra la neumonía?",
                "como prevenir la neumonia",
                "como no enfermarme de los pulmones",
                "vacuna neumonia adulto mayor",
                "como cuidarme de la neumonia",
                "como evito la neumonia en invierno",
                "que hago para no tener pulmonia",
                "prevenir infeccion al pulmon",
                "me conviene vacunarme contra la neumonia",
                "vacuna para los pulmones",
            ],
        },
        {
            "pregunta": "Mi familiar mayor está confundido o decaído, ¿puede ser neumonía?",
            "respuesta": (
                "Sí, puede ser. En las personas mayores, la neumonía a veces no da tos ni "
                "fiebre. La única señal puede ser que estén más confundidos, muy cansados, "
                "sin ganas de comer o que se caigan. Si nota un cambio así de un día para "
                "otro, llévelo a que lo revisen pronto o llame al 131."
            ),
            "variantes": [
                "mi mamá está confundida ¿puede ser neumonía?",
                "mi papa esta decaido puede ser pulmonia",
                "el abuelo no quiere comer y esta cansado",
                "adulto mayor confundido neumonia",
                "mi viejito esta raro puede ser neumonia",
                "se cae y esta decaido sera neumonia",
                "neumonia sin fiebre en anciano",
                "mi mama esta muy dormilona puede ser pulmonia",
                "confusion en adulto mayor neumonia",
                "decaimiento puede ser neumonia",
                "mi familiar mayor no reacciona bien",
                "neumonia atipica adulto mayor sintomas",
            ],
        },
        {
            "pregunta": "¿Cómo sé si es un resfrío o una neumonía?",
            "respuesta": (
                "Puede ser difícil notar la diferencia, porque empiezan parecido. Sospeche "
                "neumonía si la tos, la fiebre o el cansancio no mejoran en unos días o si "
                "empeoran. La falta de aire, el dolor en el pecho al respirar o la confusión "
                "apuntan a algo más serio que un resfrío. Ante la duda, consulte en su CESFAM "
                "para que lo examinen."
            ),
            "variantes": [
                "¿es resfrío o neumonía?",
                "como se si es resfrio o pulmonia",
                "diferencia entre resfrio y neumonia",
                "tengo tos sera neumonia o resfrio",
                "como saber si es gripe o neumonia",
                "mi resfrio no se me pasa sera neumonia",
                "cuando un resfrio es neumonia",
                "resfrio que empeora sera pulmonia",
                "como distinguir gripe de neumonia",
                "llevo dias resfriado y no mejoro",
                "sera solo un resfrio o algo mas",
            ],
        },
        {
            "pregunta": "¿La vacuna contra la neumonía es gratis y dónde me la pongo?",
            "respuesta": (
                "Sí, es gratis. En Chile, la vacuna contra la neumonía (antineumocócica) la "
                "entrega el Programa Nacional de Inmunizaciones a las personas de 65 años y "
                "más, sin costo. Se la pueden poner en su CESFAM o consultorio. Pregunte "
                "también por la vacuna de la influenza, que se coloca una vez al año."
            ),
            "variantes": [
                "¿la vacuna de la neumonía es gratis?",
                "donde me vacuno contra la neumonia",
                "la vacuna neumococica es gratis",
                "donde pongo la vacuna de la pulmonia",
                "vacuna neumonia gratis adulto mayor",
                "cuanto cuesta la vacuna de la neumonia",
                "donde me dan la vacuna para los pulmones",
                "la vacuna de la neumonia la cubre fonasa",
                "me toca la vacuna de la neumonia",
                "vacuna neumococo donde",
                "como consigo la vacuna de la neumonia",
            ],
        },
        {
            "pregunta": "¿Cuánto demora en recuperarse de una neumonía?",
            "respuesta": (
                "La mejoría es lenta y es distinta en cada persona. La tos y el cansancio "
                "pueden durar varias semanas, aunque la fiebre suele bajar antes con el "
                "tratamiento. Descanse, tome harto líquido y vaya a sus controles. Si en vez "
                "de mejorar empeora, vuelve la fiebre o le cuesta respirar, consulte de nuevo."
            ),
            "variantes": [
                "¿cuánto dura la recuperación de la neumonía?",
                "cuanto demoro en mejorar de la neumonia",
                "cuanto tiempo dura la neumonia",
                "cuando me voy a recuperar de la pulmonia",
                "cuanto dura la tos despues de la neumonia",
                "me sigo sintiendo cansado despues de la neumonia",
                "cuanto tarda en sanar la neumonia",
                "hace cuanto deberia estar mejor de la neumonia",
                "recuperacion neumonia adulto mayor",
                "sigo con tos despues de la pulmonia",
                "cuanto dura el cansancio de la neumonia",
            ],
        },
        {
            "pregunta": "¿Tengo que terminar todos los antibióticos aunque me sienta mejor?",
            "respuesta": (
                "Sí, es muy importante completar todos los días de antibiótico que le indicó "
                "el médico, aunque ya se sienta bien. Si los corta antes, la infección puede "
                "volver y hacerse más difícil de tratar. No comparta sus antibióticos ni los "
                "guarde para otra vez. Si un remedio le cae mal, no lo suspenda solo: llame a "
                "su médico o a su CESFAM."
            ),
            "variantes": [
                "¿tengo que terminar los antibióticos?",
                "puedo dejar el antibiotico si me siento bien",
                "termino los antibioticos de la neumonia",
                "hasta cuando tomo el antibiotico",
                "ya me siento bien puedo parar el antibiotico",
                "debo terminar todo el tratamiento",
                "el antibiotico me cae mal puedo dejarlo",
                "puedo guardar antibioticos para despues",
                "tengo que tomar todo el antibiotico igual",
                "dejar el antibiotico antes es malo",
                "puedo cortar el antibiotico antes",
            ],
        },
    ],
}