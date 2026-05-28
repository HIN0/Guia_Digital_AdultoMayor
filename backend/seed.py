"""
seed.py — Puebla la base de datos con el contenido real del proyecto.

Cómo ejecutar:
    cd backend
    python seed.py

Solo ejecutar UNA VEZ. Para re-poblar desde cero:
    python seed.py --reset
"""
import sys
from sqlalchemy.orm import Session

sys.path.insert(0, ".")

from core.database import SessionLocal, Base, engine
from modules.auth.entity import Usuario
from modules.educacion.entity import Modulo, Leccion, QuizFinal, PreguntaQuiz, OpcionRespuesta
from modules.progreso.entity import ProgresoLeccion, IntentoQuiz, Insignia, InsigniaObtenida
# from modules.chatbot.entity import Patologia  # pendiente: módulo chatbot sin entity aún


def crear_tablas():
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas / verificadas")


LECCIONES_DATA = [
  {
    "leccion_id": "1.1",
    "modulo_id": 1,
    "orden": 1,
    "titulo": "Bienvenida y navegación",
    "duracion_min": 3,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "saludo",
          "titulo": "¡Bienvenido!",
          "texto": "Hola, te vamos a enseñar a usar esta aplicación paso a paso. No te preocupes si te equivocas: puedes volver atrás cuando quieras. Aquí nadie te apura.",
          "apoyo_visual": "Ilustración cálida de una persona mayor sonriendo frente a un teléfono. Botón verde grande \"Comenzar\"."
        },
        {
          "n": 2,
          "tipo": "tour",
          "titulo": "Los botones que vas a usar",
          "texto": "Esta aplicación tiene pocos botones y son siempre los mismos. Te los presentamos una sola vez y los reconocerás en todas las pantallas.",
          "apoyo_visual": "Flechas animadas señalando: ① la flecha ← para Volver, ② el menú principal (Inicio), ③ el botón de Chat, ④ el botón de progreso, ⑤ el selector de tamaño de letra."
        },
        {
          "n": 3,
          "tipo": "tour",
          "titulo": "Si algo se ve muy chico",
          "texto": "¿La letra se ve pequeña? Elige el tamaño Grande para agrandarla. Puedes hacerlo en cualquier momento, en cualquier pantalla.",
          "apoyo_visual": "Demostración del selector Pequeño / Mediano / Grande cambiando el tamaño del texto en vivo."
        },
        {
          "n": 4,
          "tipo": "mini_practica",
          "titulo": "Practiquemos juntos",
          "texto": "Vamos a practicar sin riesgo. Sigue las instrucciones: \"Toca el botón azul para continuar\" → \"Excelente, ahora toca la flecha para volver\" → \"Perfecto, así puedes navegar siempre\".",
          "apoyo_visual": "Guía paso a paso con refuerzo positivo después de cada toque."
        },
        {
          "n": 5,
          "tipo": "cierre",
          "titulo": "¡Lo estás haciendo muy bien!",
          "texto": "Ya conoces los botones más importantes. Recuerda: la flecha ← siempre te lleva atrás y el botón Inicio te lleva al menú principal. Nunca te vas a perder.",
          "apoyo_visual": "Mensaje de felicitación con marca de avance del módulo."
        }
      ],
      "ejercicio": {
        "tipo": "tocar_boton_correcto",
        "instruccion": "Toca el botón que sirve para volver atrás.",
        "descripcion": "Una pantalla con cuatro botones desordenados. Si el usuario falla, se le muestra cuál era la respuesta correcta. Sin penalización.",
        "items": [
          {
            "opcion": "Atrás (flecha ←)",
            "correcta": True
          },
          {
            "opcion": "Menú",
            "correcta": False
          },
          {
            "opcion": "Chatbot",
            "correcta": False
          },
          {
            "opcion": "Ajustes",
            "correcta": False
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
          {
            "pregunta": "Si te pierdes en una lección, ¿qué botón usas para volver al menú principal?",
            "opciones": [
              {
                "texto": "El botón Inicio",
                "correcta": True
              },
              {
                "texto": "Apagar el teléfono",
                "correcta": False
              },
              {
                "texto": "Esperar a que se cierre solo",
                "correcta": False
              }
            ],
            "feedback": "El botón Inicio siempre te lleva al menú principal desde cualquier pantalla. No tienes que apagar nada."
          },
          {
            "pregunta": "¿Puedes hacer la letra de la app más grande o más pequeña?",
            "opciones": [
              {
                "texto": "Sí, con el selector de tamaño de letra",
                "correcta": True
              },
              {
                "texto": "No, la letra es fija",
                "correcta": False
              },
              {
                "texto": "Solo llamando al hospital",
                "correcta": False
              }
            ],
            "feedback": "Sí. El selector Grande agranda la letra y Pequeño la achica, en cualquier momento."
          },
          {
            "pregunta": "Si no entiendes algo, ¿qué puedes hacer?",
            "opciones": [
              {
                "texto": "Volver a leer la lección",
                "correcta": True
              },
              {
                "texto": "Cerrar la app y no volver",
                "correcta": False
              },
              {
                "texto": "Nada, seguir aunque no entiendas",
                "correcta": False
              }
            ],
            "feedback": "Puedes volver atrás a releer cuantas veces quieras. Equivocarse es parte de aprender."
          }
        ],
        "resultado": {
          "umbral_aprobado": 2,
          "titulo_aprobado": "¡Excelente Trabajo!",
          "mensaje_aprobado": "Tienes una buena comprensión de este tema. ¡Sigue así!",
          "titulo_fallido": "¡Casi lo logras!",
          "mensaje_fallido": "No te preocupes, puedes volver a repasar la lección cuando quieras."
        }
      }
    }
  },
  {
    "leccion_id": "1.2",
    "modulo_id": 1,
    "orden": 2,
    "titulo": "¿Qué es la IA?",
    "duracion_min": 4,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "concepto",
          "titulo": "¿Qué es la inteligencia artificial?",
          "texto": "La inteligencia artificial, o \"IA\", es un programa de computador que aprende de la información y ayuda a responder preguntas o ayudarte con tareas. No piensa ni siente como una persona: solo encuentra patrones muy rápido.",
          "apoyo_visual": "Ilustración simple: un computador rodeado de ejemplos con una flecha que sale hacia una respuesta."
        },
        {
          "n": 2,
          "tipo": "ejemplos",
          "titulo": "Ya la has usado sin darte cuenta",
          "texto": "Probablemente ya conviviste con la IA: cuando tu teléfono reconoce tu cara, cuando el corrector te arregla una palabra, cuando una app te sugiere la ruta más rápida o cuando le hablas a un asistente de voz. Todo eso es inteligencia artificial.",
          "apoyo_visual": "Cuatro tarjetas: 📷 reconocer cara, ✍️ corregir texto, 🗺️ sugerir ruta, 🔊 asistente de voz."
        },
        {
          "n": 3,
          "tipo": "concepto",
          "titulo": "¿Cómo aprende la IA?",
          "texto": "La IA lee millones de textos de internet para aprender patrones. Puede escribir respuestas útiles, pero también puede cometer errores porque no entiende las cosas como lo hace una persona.",
          "apoyo_visual": "Analogía visual del aprendizaje por ejemplos."
        },
        {
          "n": 4,
          "tipo": "concepto",
          "titulo": "La IA no es mágica ni infalible",
          "texto": "Es importante recordar: la IA no sabe todo, no siempre tiene la razón, y no reemplaza a un médico. Es una herramienta útil, como una calculadora: ayuda, pero hay que saber usarla.",
          "apoyo_visual": "Comparación: calculadora 🧮 = herramienta útil / IA 🤖 = herramienta útil."
        },
        {
          "n": 5,
          "tipo": "concepto",
          "titulo": "Chatbots de IA",
          "texto": "Los chatbots como ChatGPT pueden responder tus preguntas en lenguaje natural. Suenan muy seguros, pero pueden dar información incorrecta. Siempre verifica las respuestas sobre salud.",
          "apoyo_visual": "Ilustración de un chatbot conversando con un usuario."
        },
        {
          "n": 6,
          "tipo": "cierre",
          "titulo": "Punto Clave",
          "texto": "La IA es una herramienta útil, no un reemplazo de tu doctor. Úsala para aprender y preparar preguntas, pero siempre confirma la información importante de salud con un profesional.",
          "apoyo_visual": "Resumen con tres viñetas y marca de avance."
        }
      ],
      "ejercicio": {
        "tipo": "clasificar_es_ia",
        "instruccion": "¿Esto usa inteligencia artificial? Toca SÍ o NO.",
        "descripcion": "Aparecen situaciones una por una. El usuario clasifica si hay IA detrás. Sin penalización.",
        "items": [
          {
            "situacion": "Tu teléfono reconoce tu cara para desbloquearse",
            "respuesta": "SÍ"
          },
          {
            "situacion": "Una linterna que se enciende con un interruptor",
            "respuesta": "NO"
          },
          {
            "situacion": "Un asistente de voz que responde tus preguntas",
            "respuesta": "SÍ"
          },
          {
            "situacion": "Una calculadora que suma dos números",
            "respuesta": "NO"
          },
          {
            "situacion": "Una app que te sugiere la ruta más rápida",
            "respuesta": "SÍ"
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
          {
            "pregunta": "¿Qué es, en palabras simples, la inteligencia artificial?",
            "opciones": [
              {
                "texto": "Un programa que aprende de muchos ejemplos para ayudarte",
                "correcta": True
              },
              {
                "texto": "Un robot con sentimientos que vive en el teléfono",
                "correcta": False
              },
              {
                "texto": "Una persona del hospital que responde en secreto",
                "correcta": False
              }
            ],
            "feedback": "La IA es un programa que encuentra patrones en muchos ejemplos. No es una persona ni siente emociones."
          },
          {
            "pregunta": "¿La IA siempre tiene la razón?",
            "opciones": [
              {
                "texto": "No, también se equivoca",
                "correcta": True
              },
              {
                "texto": "Sí, nunca falla",
                "correcta": False
              },
              {
                "texto": "Solo se equivoca de noche",
                "correcta": False
              }
            ],
            "feedback": "La IA aprende de ejemplos y a veces se equivoca. Por eso hay que usarla con criterio, sobre todo en salud."
          },
          {
            "pregunta": "¿La IA puede reemplazar a tu médico?",
            "opciones": [
              {
                "texto": "No, es solo una herramienta de apoyo",
                "correcta": True
              },
              {
                "texto": "Sí, es igual que un doctor",
                "correcta": False
              },
              {
                "texto": "Sí, pero solo los fines de semana",
                "correcta": False
              }
            ],
            "feedback": "La IA puede ayudarte a entender información, pero nunca reemplaza la evaluación de un profesional de salud."
          }
        ],
        "resultado": {
          "umbral_aprobado": 2,
          "titulo_aprobado": "¡Excelente Trabajo!",
          "mensaje_aprobado": "Tienes una buena comprensión de este tema. ¡Sigue así!",
          "titulo_fallido": "¡Casi lo logras!",
          "mensaje_fallido": "No te preocupes, puedes volver a repasar la lección cuando quieras."
        }
      }
    }
  },
  {
    "leccion_id": "1.3",
    "modulo_id": 1,
    "orden": 3,
    "titulo": "La IA en salud",
    "duracion_min": 4,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "concepto",
          "titulo": "La IA puede ayudarte con tu salud",
          "texto": "En temas de salud, la IA puede ser una buena aliada para entender mejor la información. Recuerda siempre: te orienta y te explica, pero no te diagnostica ni te receta. La última palabra siempre la tiene tu médico.",
          "apoyo_visual": "Ícono de corazón con un signo de ayuda."
        },
        {
          "n": 2,
          "tipo": "ejemplos",
          "titulo": "Para qué SÍ sirve",
          "texto": "Usa la IA para: explicar qué significa un diagnóstico en palabras sencillas, entender efectos secundarios de medicamentos, preparar una lista de preguntas para tu cita, o aprender sobre hábitos saludables.",
          "apoyo_visual": "Tres tarjetas: 📖 explicar palabras, ℹ️ información general, ⏰ recordatorios."
        },
        {
          "n": 3,
          "tipo": "ejemplo_real",
          "titulo": "Un ejemplo cercano",
          "texto": "Don Luis empezó un medicamento nuevo y le daba mareos. Le preguntó a la app si era normal y entendió que era un efecto secundario común. Con esa información, anotó la pregunta para su médico y llegó preparado a la consulta.",
          "apoyo_visual": "Viñeta ilustrada de don Luis consultando la app en casa."
        },
        {
          "n": 4,
          "tipo": "advertencia",
          "titulo": "Lo Que NO Debes Hacer",
          "texto": "Nunca uses la IA para: autodiagnosticarte, cambiar tu medicación, reemplazar la visita al doctor, o tomar decisiones urgentes de salud. La IA es para aprender, no para decisiones médicas.",
          "apoyo_visual": "Lista con íconos rojos de \"no\" frente a cada límite."
        },
        {
          "n": 5,
          "tipo": "cierre",
          "titulo": "En resumen",
          "texto": "La IA en salud sirve para entender, informarte y recordar cuidados generales. Nunca para diagnosticar ni reemplazar a tu doctor.",
          "apoyo_visual": "Resumen con tres viñetas y marca de avance."
        }
      ],
      "ejercicio": {
        "tipo": "clasificar_uso_apropiado",
        "instruccion": "¿La IA es buena para esto? Toca SÍ PUEDE AYUDAR o ESO ES DEL MÉDICO.",
        "descripcion": "El usuario distingue entre usos orientativos y tareas clínicas. Sin penalización.",
        "items": [
          {
            "situacion": "Explicarme qué significa la palabra \"colesterol\"",
            "respuesta": "SÍ PUEDE AYUDAR"
          },
          {
            "situacion": "Decirme qué dosis de remedio tomar",
            "respuesta": "ESO ES DEL MÉDICO"
          },
          {
            "situacion": "Darme ideas de preguntas para mi control",
            "respuesta": "SÍ PUEDE AYUDAR"
          },
          {
            "situacion": "Interpretar el resultado de mi examen de sangre",
            "respuesta": "ESO ES DEL MÉDICO"
          },
          {
            "situacion": "Recordarme tomar agua durante el día",
            "respuesta": "SÍ PUEDE AYUDAR"
          },
          {
            "situacion": "Decirme si el dolor que siento es grave",
            "respuesta": "ESO ES DEL MÉDICO"
          },
          {
            "situacion": "Usar la IA para cambiar la dosis de tu medicamento",
            "respuesta": "ESO ES DEL MÉDICO"
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
          {
            "pregunta": "¿Para cuál de estas cosas SÍ sirve la IA en salud?",
            "opciones": [
              {
                "texto": "Explicarte qué significa una palabra médica",
                "correcta": True
              },
              {
                "texto": "Recetarte un medicamento",
                "correcta": False
              },
              {
                "texto": "Decirte el resultado de tus exámenes",
                "correcta": False
              }
            ],
            "feedback": "La IA sirve para orientarte y explicarte información general. Recetar e interpretar exámenes es tarea exclusiva de tu médico."
          },
          {
            "pregunta": "¿Puede la IA diagnosticarte una enfermedad?",
            "opciones": [
              {
                "texto": "Sí, si le das muchos detalles",
                "correcta": False
              },
              {
                "texto": "No, solo un médico puede diagnosticar",
                "correcta": True
              },
              {
                "texto": "Sí, igual que en el hospital",
                "correcta": False
              }
            ],
            "feedback": "Un diagnóstico necesita examen físico, historia clínica y exámenes. La IA no puede hacer eso; solo orienta."
          },
          {
            "pregunta": "Tu doctor mencionó una palabra que no entendiste. ¿Cómo te ayuda la IA?",
            "opciones": [
              {
                "texto": "Cambiando tu tratamiento",
                "correcta": False
              },
              {
                "texto": "Cancelando tu próxima consulta",
                "correcta": False
              },
              {
                "texto": "Explicándote qué significa esa palabra",
                "correcta": True
              }
            ],
            "feedback": "La IA es excelente para explicar términos médicos en palabras simples, y así llegas más preparado a tu control."
          }
        ],
        "resultado": {
          "umbral_aprobado": 2,
          "titulo_aprobado": "¡Excelente Trabajo!",
          "mensaje_aprobado": "Tienes una buena comprensión de este tema. ¡Sigue así!",
          "titulo_fallido": "¡Casi lo logras!",
          "mensaje_fallido": "No te preocupes, puedes volver a repasar la lección cuando quieras."
        }
      }
    }
  },
  {
    "leccion_id": "1.4",
    "modulo_id": 1,
    "orden": 4,
    "titulo": "Riesgos y limitaciones",
    "duracion_min": 5,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "concepto",
          "titulo": "La IA se puede equivocar (y suena segura)",
          "texto": "Lo más importante de esta lección: la IA a veces se equivoca, pero lo dice con mucha seguridad. Por eso no hay que creerle todo solo porque suena convincente.",
          "apoyo_visual": "Ilustración de un robot hablando con tono seguro mientras un signo de interrogación flota encima."
        },
        {
          "n": 2,
          "tipo": "concepto",
          "titulo": "1) La IA puede inventar cosas",
          "texto": "A veces la IA inventa información que parece real pero es falsa. Se le llama alucinación. Puede inventar el nombre de un remedio, una dosis o hasta un dato de un hospital. Por eso, lo importante de salud siempre hay que confirmarlo.",
          "apoyo_visual": "Ejemplo de una respuesta inventada marcada con una lupa y la palabra \"alucinación\"."
        },
        {
          "n": 3,
          "tipo": "concepto",
          "titulo": "2) La IA puede estar desactualizada",
          "texto": "La IA aprendió hasta cierta fecha. Puede no saber de un remedio nuevo, de un cambio de horario del hospital o de una recomendación reciente. La información médica cambia, y la IA no siempre está al día.",
          "apoyo_visual": "Calendario con una fecha de corte y un reloj indicando \"puede estar atrasada\"."
        },
        {
          "n": 4,
          "tipo": "concepto",
          "titulo": "3) La IA no conoce TU caso",
          "texto": "La IA da respuestas generales. Pero tú tienes tu edad, tus remedios, tus otras enfermedades. Algo que sirve para la mayoría puede no servirte a ti. Tu médico sí conoce tu caso completo.",
          "apoyo_visual": "Comparación: una multitud (lo general) frente a una sola persona destacada (tu caso)."
        },
        {
          "n": 5,
          "tipo": "ejemplo_real",
          "titulo": "Un caso para recordar",
          "texto": "La señora Rosa le preguntó a una IA por un dolor y la IA le sugirió un remedio con mucha seguridad. Por suerte, Rosa lo consultó con su doctora, quien le explicó que ese remedio le hacía mal por otro medicamento que ya tomaba. Confirmar le evitó un problema serio.",
          "apoyo_visual": "Viñeta del caso con mensaje: \"confirmar la salvó de un error\"."
        },
        {
          "n": 6,
          "tipo": "cierre",
          "titulo": "En resumen",
          "texto": "La IA puede inventar datos, estar desactualizada y no conocer tu caso. Regla de oro: en salud, lo importante siempre se confirma con un profesional.",
          "apoyo_visual": "Resumen con tres riesgos y la regla de oro destacada."
        }
      ],
      "ejercicio": {
        "tipo": "detectar_riesgo",
        "instruccion": "¿Qué riesgo hay en cada respuesta de la IA? Arrastra la etiqueta correcta.",
        "descripcion": "Se muestran respuestas de IA y el usuario identifica el riesgo.",
        "items": [
          {
            "respuesta_ia": "\"El medicamento Curalina-5 cura la artrosis en 3 días.\" (un remedio que no existe)",
            "etiqueta": "Puede estar inventando"
          },
          {
            "respuesta_ia": "\"El horario del hospital es de 8 a 14 horas.\" (cambió hace un mes)",
            "etiqueta": "Puede estar desactualizada"
          },
          {
            "respuesta_ia": "\"Para el dolor, lo normal es tomar este remedio.\" (sin saber tus otras enfermedades)",
            "etiqueta": "No conoce mi caso"
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
          {
            "pregunta": "Cuando la IA inventa información falsa que parece real, eso se llama:",
            "opciones": [
              {
                "texto": "Diagnóstico",
                "correcta": False
              },
              {
                "texto": "Alucinación",
                "correcta": True
              },
              {
                "texto": "Receta",
                "correcta": False
              }
            ],
            "feedback": "Se llama alucinación. La IA puede inventar datos con mucha seguridad. Por eso lo importante se confirma."
          },
          {
            "pregunta": "La IA te responde con mucha seguridad sobre un remedio. ¿Le crees de inmediato?",
            "opciones": [
              {
                "texto": "No, lo confirmo con un profesional",
                "correcta": True
              },
              {
                "texto": "Sí, porque sonó muy segura",
                "correcta": False
              },
              {
                "texto": "Sí, si usa palabras difíciles",
                "correcta": False
              }
            ],
            "feedback": "Sonar segura no significa tener la razón. En salud, lo importante siempre se confirma con tu médico."
          },
          {
            "pregunta": "¿Por qué un consejo general de la IA puede no servirte a ti?",
            "opciones": [
              {
                "texto": "Porque la IA no habla español",
                "correcta": False
              },
              {
                "texto": "Porque no conoce tu edad, tus remedios ni tus otras enfermedades",
                "correcta": True
              },
              {
                "texto": "Porque siempre se equivoca a propósito",
                "correcta": False
              }
            ],
            "feedback": "La IA da respuestas para la mayoría. Tu médico conoce tu caso completo, y eso hace toda la diferencia."
          }
        ],
        "resultado": {
          "umbral_aprobado": 2,
          "titulo_aprobado": "¡Excelente Trabajo!",
          "mensaje_aprobado": "Tienes una buena comprensión de este tema. ¡Sigue así!",
          "titulo_fallido": "¡Casi lo logras!",
          "mensaje_fallido": "No te preocupes, puedes volver a repasar la lección cuando quieras."
        }
      }
    }
  },
  {
    "leccion_id": "1.5",
    "modulo_id": 1,
    "orden": 5,
    "titulo": "Privacidad y datos",
    "duracion_min": 4,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "analogia",
          "titulo": "Hablarle a la IA no es hablar en privado",
          "texto": "Cuando le hablas a la IA, es como gritar tu mensaje en una plaza llena de gente. Algunas IAs guardan todo lo que escribes. No es como hablar en privado con tu doctor en su consulta.",
          "apoyo_visual": "Ilustración de una plaza con mucha gente escuchando, frente a una consulta médica cerrada."
        },
        {
          "n": 2,
          "tipo": "lista_si",
          "titulo": "Qué SÍ puedes compartir",
          "texto": "Puedes compartir sin problema información general que no te identifica: tus síntomas en general, dudas sobre una enfermedad y preguntas de orientación.",
          "apoyo_visual": "Lista verde: síntomas en general, dudas sobre una enfermedad, preguntas de orientación."
        },
        {
          "n": 3,
          "tipo": "lista_no",
          "titulo": "Qué NO debes compartir nunca",
          "texto": "Nunca compartas datos que te identifican o que dan acceso a tu dinero: tu RUT, tu dirección, tu número de Fonasa, fotos de exámenes con tu nombre, datos de tarjeta bancaria y contraseñas.",
          "apoyo_visual": "Lista roja: RUT, dirección, Fonasa, fotos con nombre, tarjeta bancaria, contraseñas."
        },
        {
          "n": 4,
          "tipo": "ejemplo_real",
          "titulo": "Lo que le pasó a María",
          "texto": "María le contó a una IA que tenía depresión y le dio su correo. A las dos semanas empezó a recibir publicidad de medicamentos. ¿Por qué pasó? Porque sus datos quedaron guardados y se usaron sin que ella quisiera.",
          "apoyo_visual": "Viñeta del caso de María recibiendo publicidad no deseada."
        },
        {
          "n": 5,
          "tipo": "cierre",
          "titulo": "Recuerda siempre",
          "texto": "Los datos personales se guardan para ti y tu doctor, no para la IA. Si una IA te pide datos personales para ayudarte mejor, desconfía: una IA confiable nunca necesita tu RUT ni tu dirección para responder dudas de salud.",
          "apoyo_visual": "Mensaje de cierre destacado con candado 🔒."
        }
      ],
      "ejercicio": {
        "tipo": "semaforo_privacidad",
        "instruccion": "¿Esto se puede compartir con la IA? Toca el botón VERDE (sí) o ROJO (no).",
        "descripcion": "Aparecen ocho frases una por una. El usuario decide si es seguro compartirlas. Sin penalización.",
        "items": [
          {
            "frase": "Tengo dolor de cabeza desde hace 3 días",
            "respuesta": "VERDE"
          },
          {
            "frase": "Mi RUT es 12.345.678-9 y tengo presión alta",
            "respuesta": "ROJO"
          },
          {
            "frase": "¿Qué es la diabetes tipo 2?",
            "respuesta": "VERDE"
          },
          {
            "frase": "Soy Juan Pérez, vivo en calle Los Aromos 234",
            "respuesta": "ROJO"
          },
          {
            "frase": "Mi madre tomaba este remedio, ¿es seguro?",
            "respuesta": "VERDE"
          },
          {
            "frase": "Aquí está mi tarjeta bancaria para que me cobres la consulta",
            "respuesta": "ROJO"
          },
          {
            "frase": "Tengo 70 años y me cuesta dormir",
            "respuesta": "VERDE"
          },
          {
            "frase": "Mi clave del banco es 1234",
            "respuesta": "ROJO"
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
          {
            "pregunta": "Si una IA te pide tu RUT y tu dirección para ayudarte mejor, ¿qué haces?",
            "opciones": [
              {
                "texto": "No se los das y desconfías",
                "correcta": True
              },
              {
                "texto": "Se los das",
                "correcta": False
              },
              {
                "texto": "Le das solo el RUT",
                "correcta": False
              }
            ],
            "feedback": "Una IA confiable nunca necesita tu RUT ni tu dirección para responder dudas de salud."
          },
          {
            "pregunta": "¿Está bien preguntarle a una IA qué es el colesterol alto?",
            "opciones": [
              {
                "texto": "No, nunca se le pregunta nada a la IA",
                "correcta": False
              },
              {
                "texto": "Solo si le das tu dirección primero",
                "correcta": False
              },
              {
                "texto": "Sí, es información general, no datos personales",
                "correcta": True
              }
            ],
            "feedback": "Correcto. Preguntar por información general es seguro. El problema son los datos que te identifican."
          },
          {
            "pregunta": "Tu nieto te dice que mandes una foto de tu carnet porque una IA del hospital la necesita. ¿Qué haces?",
            "opciones": [
              {
                "texto": "No la mando y llamo directamente al hospital para confirmar",
                "correcta": True
              },
              {
                "texto": "La mando de inmediato",
                "correcta": False
              },
              {
                "texto": "Mando solo la mitad de la foto",
                "correcta": False
              }
            ],
            "feedback": "Ningún hospital pide eso por WhatsApp. Ante la duda, confirma llamando directamente al número oficial."
          }
        ],
        "resultado": {
          "umbral_aprobado": 2,
          "titulo_aprobado": "¡Excelente Trabajo!",
          "mensaje_aprobado": "Tienes una buena comprensión de este tema. ¡Sigue así!",
          "titulo_fallido": "¡Casi lo logras!",
          "mensaje_fallido": "No te preocupes, puedes volver a repasar la lección cuando quieras."
        }
      }
    }
  },
  {
    "leccion_id": "1.6",
    "modulo_id": 1,
    "orden": 6,
    "titulo": "Reconocer engaños",
    "duracion_min": 4,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "concepto",
          "titulo": "No todo lo que parece un hospital lo es",
          "texto": "No todo lo que parece un hospital o un doctor en internet, lo es. Hay personas que crean páginas y mensajes falsos para engañarte y quitarte tu dinero o tus datos. Aprender a reconocerlos te protege.",
          "apoyo_visual": "Ilustración de un mensaje con disfraz de hospital y una alerta."
        },
        {
          "n": 2,
          "tipo": "concepto",
          "titulo": "Tres señales de alerta",
          "texto": "Desconfía siempre que algo: ① te promete curas milagrosas, ② te apura (responde ya o pierdes el cupo), o ③ te pide pagar antes de explicarte nada. Los servicios de salud de verdad no funcionan así.",
          "apoyo_visual": "Tres tarjetas de alerta: 🪄 cura milagrosa, ⏱️ te apura, 💳 te pide pagar."
        },
        {
          "n": 3,
          "tipo": "concepto",
          "titulo": "Cómo verificar si algo es real",
          "texto": "Para saber si una página o mensaje es real: busca el nombre del hospital en Google, llama por teléfono al hospital usando el número oficial, y nunca hagas clic en links que te llegan por WhatsApp de desconocidos.",
          "apoyo_visual": "Pasos ilustrados: buscar en Google, llamar al número oficial, no tocar links de WhatsApp."
        },
        {
          "n": 4,
          "tipo": "ejemplo_real",
          "titulo": "Mira estos casos reales",
          "texto": "Un médico de verdad nunca te escribe por WhatsApp ofreciéndote remedios gratis. Una página oficial termina en gob.cl y usa lenguaje formal. Un anuncio que dice baja 10 kilos en una semana con esta hierba es siempre sospechoso.",
          "apoyo_visual": "Capturas comparadas: mensaje falso vs. sitio oficial gob.cl."
        },
        {
          "n": 5,
          "tipo": "cierre",
          "titulo": "En resumen",
          "texto": "Las estafas de salud prometen milagros, te apuran y te piden dinero o datos. Ante cualquier duda: cuelga, no toques el link, y llama tú mismo al hospital al número oficial. Más vale confirmar que lamentar.",
          "apoyo_visual": "Resumen con las tres señales y la acción de verificar."
        }
      ],
      "ejercicio": {
        "tipo": "detective_estafas",
        "instruccion": "¿Es confiable o sospechoso? Marca cada caso.",
        "descripcion": "Se muestran cinco casos y el usuario marca cada uno, con explicación al fallar.",
        "items": [
          {
            "caso": "WhatsApp: Hola abuelita, soy Dr. Ramírez del HUAP, le tengo un remedio gratis para la artrosis, mándeme su dirección",
            "respuesta": "SOSPECHOSO",
            "motivo": "Un médico real no contacta así ni pide tu dirección por WhatsApp."
          },
          {
            "caso": "Sitio oficial: huap.redsalud.gob.cl con información sobre horarios",
            "respuesta": "CONFIABLE",
            "motivo": "Dominio gob.cl y lenguaje formal: señales de sitio oficial."
          },
          {
            "caso": "Anuncio: Médicos odian este truco. Baja 10 kilos en una semana con esta hierba milagrosa",
            "respuesta": "SOSPECHOSO",
            "motivo": "Promesa milagrosa + lenguaje sensacionalista."
          },
          {
            "caso": "Email: Estimado paciente, su próxima consulta en HUAP es el 15 de mayo. Confirme respondiendo SÍ",
            "respuesta": "VERIFICAR",
            "motivo": "Puede ser real, pero siempre confirma llamando al hospital antes de responder."
          },
          {
            "caso": "Chatbot IA: Le receto paracetamol 500mg cada 8 horas para su dolor",
            "respuesta": "SOSPECHOSO",
            "motivo": "La IA no debe recetar. Eso es tarea exclusiva de un médico."
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
          {
            "pregunta": "¿Cuál es la señal más clara de una estafa de salud en internet?",
            "opciones": [
              {
                "texto": "Te ofrecen información gratis",
                "correcta": False
              },
              {
                "texto": "El sitio tiene fotos",
                "correcta": False
              },
              {
                "texto": "Te prometen curas milagrosas",
                "correcta": True
              }
            ],
            "feedback": "Las curas milagrosas no existen. Esa promesa es la señal de alerta más clara de una estafa."
          },
          {
            "pregunta": "Recibes un WhatsApp de tu hospital pidiéndote dinero para una cita. ¿Qué haces?",
            "opciones": [
              {
                "texto": "Cuelgo y llamo al hospital al número oficial",
                "correcta": True
              },
              {
                "texto": "Pago de inmediato para no perder la cita",
                "correcta": False
              },
              {
                "texto": "Respondo el WhatsApp pidiendo más datos",
                "correcta": False
              }
            ],
            "feedback": "Los hospitales no cobran citas por WhatsApp. Cuelga y verifica llamando tú mismo al número oficial."
          },
          {
            "pregunta": "Una página dice Dr. González, especialista en TODO. ¿Es buena señal?",
            "opciones": [
              {
                "texto": "Sí, mientras más especialidades mejor",
                "correcta": False
              },
              {
                "texto": "No, los médicos reales se especializan en áreas específicas",
                "correcta": True
              },
              {
                "texto": "Sí, si tiene muchas estrellas",
                "correcta": False
              }
            ],
            "feedback": "Nadie es especialista en todo. Esa exageración es típica de las páginas falsas."
          }
        ],
        "resultado": {
          "umbral_aprobado": 2,
          "titulo_aprobado": "¡Excelente Trabajo!",
          "mensaje_aprobado": "Tienes una buena comprensión de este tema. ¡Sigue así!",
          "titulo_fallido": "¡Casi lo logras!",
          "mensaje_fallido": "No te preocupes, puedes volver a repasar la lección cuando quieras."
        }
      }
    }
  }
]

QUIZZES_DATA = [
  {
    "quiz_final_id": "QF1",
    "modulo_id": 1,
    "minimo_aciertos": 5,
    "bloqueante": True,
    "preguntas": [
      {
        "pregunta": "En palabras simples, ¿qué es la inteligencia artificial?",
        "opciones": [
          {
            "texto": "Un programa que aprende de muchos ejemplos para ayudarte",
            "correcta": True
          },
          {
            "texto": "Una persona del hospital que responde en secreto",
            "correcta": False
          },
          {
            "texto": "Un robot con sentimientos",
            "correcta": False
          }
        ],
        "feedback": "La IA es un programa que encuentra patrones en ejemplos. No es una persona ni siente."
      },
      {
        "pregunta": "¿Para cuál de estas cosas SÍ sirve la IA en salud?",
        "opciones": [
          {
            "texto": "Explicarte una palabra médica que no entendiste",
            "correcta": True
          },
          {
            "texto": "Recetarte un medicamento",
            "correcta": False
          },
          {
            "texto": "Interpretar tus exámenes de sangre",
            "correcta": False
          }
        ],
        "feedback": "La IA orienta y explica. Recetar e interpretar exámenes es tarea exclusiva del médico."
      },
      {
        "pregunta": "Cuando la IA inventa información falsa que parece real, se llama:",
        "opciones": [
          {
            "texto": "Alucinación",
            "correcta": True
          },
          {
            "texto": "Diagnóstico",
            "correcta": False
          },
          {
            "texto": "Consulta",
            "correcta": False
          }
        ],
        "feedback": "Se llama alucinación. Por eso, lo importante de salud siempre se confirma."
      },
      {
        "pregunta": "La IA te responde con mucha seguridad sobre un remedio. ¿Le crees de inmediato?",
        "opciones": [
          {
            "texto": "No, lo confirmo con un profesional",
            "correcta": True
          },
          {
            "texto": "Sí, porque sonó muy segura",
            "correcta": False
          },
          {
            "texto": "Sí, si usó palabras difíciles",
            "correcta": False
          }
        ],
        "feedback": "Sonar segura no es tener la razón. Lo importante se confirma con tu médico o farmacéutico."
      },
      {
        "pregunta": "¿Cuál de estos datos NO debes compartir nunca con una IA?",
        "opciones": [
          {
            "texto": "Tu RUT y tu clave del banco",
            "correcta": True
          },
          {
            "texto": "Una duda general sobre la diabetes",
            "correcta": False
          },
          {
            "texto": "Que tienes dolor de cabeza",
            "correcta": False
          }
        ],
        "feedback": "Nunca compartas datos que te identifican o dan acceso a tu dinero, como el RUT o claves."
      },
      {
        "pregunta": "¿Cuál es la señal más clara de una estafa de salud en internet?",
        "opciones": [
          {
            "texto": "Te prometen una cura milagrosa",
            "correcta": True
          },
          {
            "texto": "Te dan información gratis",
            "correcta": False
          },
          {
            "texto": "La página tiene fotos",
            "correcta": False
          }
        ],
        "feedback": "Las curas milagrosas no existen: son la señal más clara de estafa."
      },
      {
        "pregunta": "Si no entiendes algo en la app, ¿qué puedes hacer?",
        "opciones": [
          {
            "texto": "Volver a leer la lección o preguntar al chatbot",
            "correcta": True
          },
          {
            "texto": "Cerrar la app y no volver",
            "correcta": False
          },
          {
            "texto": "Nada, seguir aunque no entiendas",
            "correcta": False
          }
        ],
        "feedback": "Puedes volver atrás a releer cuantas veces quieras y también preguntarle al asistente."
      }
    ]
  }
]


def poblar(db: Session):
    modulos_data = [
        {"nombre": "Conocer la inteligencia artificial", "orden": 1, "requiere_modulo_previo": False},
        {"nombre": "Practicar con la IA",                "orden": 2, "requiere_modulo_previo": True},
        {"nombre": "Asistente de IA",                    "orden": 3, "requiere_modulo_previo": True},
    ]
    modulos = []
    for m in modulos_data:
        modulo = Modulo(**m)
        db.add(modulo)
        modulos.append(modulo)
    db.flush()
    print(f"✓ {len(modulos)} módulos insertados")

    for dato in LECCIONES_DATA:
        modulo_obj = modulos[dato["modulo_id"] - 1]
        leccion = Leccion(
            modulo_id=modulo_obj.id,
            titulo=dato["titulo"],
            orden=dato["orden"],
            contenido=dato["contenido"],
        )
        db.add(leccion)
    db.flush()
    print(f"✓ {len(LECCIONES_DATA)} lecciones insertadas")

    for qdata in QUIZZES_DATA:
        modulo_obj = modulos[qdata["modulo_id"] - 1]
        quiz = QuizFinal(
            modulo_id=modulo_obj.id,
            minimo_aciertos=qdata["minimo_aciertos"],
            bloqueante=qdata["bloqueante"],
        )
        db.add(quiz)
        db.flush()
        for pdata in qdata["preguntas"]:
            pregunta = PreguntaQuiz(
                quiz_final_id=quiz.id,
                enunciado=pdata["pregunta"],
                feedback=pdata["feedback"],
            )
            db.add(pregunta)
            db.flush()
            for odata in pdata["opciones"]:
                db.add(OpcionRespuesta(
                    pregunta_id=pregunta.id,
                    texto=odata["texto"],
                    es_correcta=odata["correcta"],
                ))
    db.flush()
    print(f"✓ {len(QUIZZES_DATA)} quiz final insertado")

    for idata in [
        {"nombre": "Conocedor de la IA",   "descripcion": "Completaste el Módulo 1: Conocer la IA",      "icono_url": "🧠"},
        {"nombre": "Practicante de la IA", "descripcion": "Completaste el Módulo 2: Practicar con la IA", "icono_url": "💪"},
    ]:
        db.add(Insignia(**idata))

    # Patologías pendientes: requiere módulo chatbot implementado
    # for pdata in [...]:
    #     db.add(Patologia(**pdata))

    db.commit()
    print("\n✅ Base de datos poblada exitosamente.")


def reset_datos(db: Session):
    db.query(InsigniaObtenida).delete()
    db.query(Insignia).delete()
    db.query(IntentoQuiz).delete()
    db.query(ProgresoLeccion).delete()
    db.query(OpcionRespuesta).delete()
    db.query(PreguntaQuiz).delete()
    db.query(QuizFinal).delete()
    db.query(Leccion).delete()
    db.query(Modulo).delete()
    # db.query(Patologia).delete()  # pendiente: módulo chatbot sin entity aún
    db.query(Usuario).delete()
    db.commit()
    print("✓ Datos eliminados. Listo para re-poblar.")


if __name__ == "__main__":
    crear_tablas()
    db = SessionLocal()
    try:
        if "--reset" in sys.argv:
            reset_datos(db)
        if db.query(Modulo).count() > 0 and "--reset" not in sys.argv:
            print("⚠️  Ya hay datos. Usa  python seed.py --reset  para re-poblar.")
            sys.exit(0)
        poblar(db)
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        db.close()
