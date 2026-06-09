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
          "texto": "La IA es una herramienta útil, no un reemplazo de tu médico. Úsala para aprender y preparar preguntas, pero siempre confirma la información importante de salud con un profesional.",
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
                "texto": "Sí, es igual que un médico",
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
          "texto": "Nunca uses la IA para: autodiagnosticarte, cambiar tu medicación, reemplazar la visita al médico, o tomar decisiones urgentes de salud. La IA es para aprender, no para decisiones médicas.",
          "apoyo_visual": "Lista con íconos rojos de \"no\" frente a cada límite."
        },
        {
          "n": 5,
          "tipo": "cierre",
          "titulo": "En resumen",
          "texto": "La IA en salud sirve para entender, informarte y recordar cuidados generales. Nunca para diagnosticar ni reemplazar a tu médico.",
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
            "pregunta": "Tu médico mencionó una palabra que no entendiste. ¿Cómo te ayuda la IA?",
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
          "texto": "La señora Rosa le preguntó a una IA por un dolor y la IA le sugirió un remedio con mucha seguridad. Por suerte, Rosa lo consultó con su médica, quien le explicó que ese remedio le hacía mal por otro medicamento que ya tomaba. Confirmar le evitó un problema serio.",
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
          "texto": "Cuando le hablas a la IA, es como gritar tu mensaje en una plaza llena de gente. Algunas IAs guardan todo lo que escribes. No es como hablar en privado con tu médico en su consulta.",
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
          "texto": "Los datos personales se guardan para ti y tu médico, no para la IA. Si una IA te pide datos personales para ayudarte mejor, desconfía: una IA confiable nunca necesita tu RUT ni tu dirección para responder dudas de salud.",
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
          "texto": "No todo lo que parece un hospital o un médico en internet, lo es. Hay personas que crean páginas y mensajes falsos para engañarte y quitarte tu dinero o tus datos. Aprender a reconocerlos te protege.",
          "apoyo_visual": "Ilustración de un mensaje con disfraz de hospital y una alerta."
        },
        {
          "n": 2,
          "tipo": "concepto",
          "titulo": "Tres señales de alerta",
          "texto": "Desconfía siempre que algo: te promete curas milagrosas, te apura (responde ya o pierdes el cupo), o te pide pagar antes de explicarte nada. Los servicios de salud de verdad no funcionan así.",
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
  },
  {
    "leccion_id": "2.1",
    "modulo_id": 2,
    "orden": 1,
    "titulo": "Hacer mejores preguntas",
    "duracion_min": 4,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "concepto",
          "titulo": "Una buena pregunta da una buena respuesta",
          "texto": "La IA responde según lo que le preguntas. Si preguntas algo muy vago, te responde algo muy vago. Si preguntas con claridad, te ayuda mucho mejor. Aquí aprenderás a preguntar para que la IA te sirva de verdad.",
          "apoyo_visual": "Ilustración: una pregunta clara entra y sale una respuesta clara; una pregunta confusa sale confusa."
        },
        {
          "n": 2,
          "tipo": "concepto",
          "titulo": "Truco 1: sé concreto",
          "texto": "En lugar de \"me siento mal\", di qué te pasa: \"¿Qué puede causar dolor de cabeza por las mañanas?\". Mientras más concreta la pregunta, más útil la respuesta. No tengas miedo de escribir como hablas.",
          "apoyo_visual": "Comparación: \"me siento mal\" (vago) → \"dolor de cabeza en las mañanas\" (concreto)."
        },
        {
          "n": 3,
          "tipo": "concepto",
          "titulo": "Truco 2: pide que te lo explique fácil",
          "texto": "Si la respuesta tiene palabras difíciles, pídele que te lo explique de nuevo en palabras simples: \"explícamelo como si tuviera 70 años y no soy médico\". La IA con gusto lo repite más fácil.",
          "apoyo_visual": "Ejemplo de pedir \"explícamelo simple\" y la respuesta simplificada."
        },
        {
          "n": 4,
          "tipo": "concepto",
          "titulo": "Truco 3: nunca pongas datos personales",
          "texto": "Recuerda lo aprendido: una buena pregunta NO necesita tu RUT, tu dirección ni tus claves. Puedes preguntar por tu enfermedad sin decir quién eres. \"¿Qué cuidados necesita una persona con presión alta?\" funciona perfecto.",
          "apoyo_visual": "Recordatorio con candado: pregunta sí, datos personales no."
        },
        {
          "n": 5,
          "tipo": "cierre",
          "titulo": "En resumen",
          "texto": "Para preguntar bien: sé concreto, pide explicaciones simples y nunca incluyas datos personales. Con estos tres trucos, la IA pasa de ser confusa a ser una buena aliada.",
          "apoyo_visual": "Resumen con los tres trucos y marca de avance."
        }
      ],
      "ejercicio": {
        "tipo": "elegir_mejor_pregunta",
        "instruccion": "¿Cuál es la mejor pregunta para hacerle a la IA? Toca la mejor opción.",
        "descripcion": "Se presentan pares de preguntas y el usuario elige la más clara y segura. Sin penalización.",
        "items": [
          {
            "opciones": [
              "Me siento mal, ¿qué tengo?",
              "¿Qué puede causar dolor de cabeza por las mañanas?"
            ],
            "mejor": "¿Qué puede causar dolor de cabeza por las mañanas?"
          },
          {
            "opciones": [
              "Soy Pedro Soto, RUT 11.222.333-4, ¿qué es la diabetes?",
              "¿Qué es la diabetes tipo 2?"
            ],
            "mejor": "¿Qué es la diabetes tipo 2?"
          },
          {
            "opciones": [
              "Explícame la hipertensión en palabras simples",
              "Dame un informe técnico completo de fisiopatología hipertensiva"
            ],
            "mejor": "Explícame la hipertensión en palabras simples"
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
          {
            "pregunta": "¿Cuál de estas es una mejor pregunta para la IA?",
            "opciones": [
            
              {
                "texto": "Me siento raro, ¿qué será?",
                "correcta": False
              },
              {
                "texto": "Hola",
                "correcta": False
              },
              {
                "texto": "¿Qué cuidados necesita una persona con presión alta?",
                "correcta": True
              }
            ],
            "feedback": "Una pregunta concreta y clara da respuestas mucho más útiles que una vaga."
          },
          {
            "pregunta": "Si la respuesta tiene palabras muy difíciles, ¿qué puedes hacer?",
            "opciones": [
              {
                "texto": "Pedirle que lo explique en palabras simples",
                "correcta": True
              },
              {
                "texto": "Rendirte y cerrar la app",
                "correcta": False
              },
              {
                "texto": "Creer que es tu culpa por no entender",
                "correcta": False
              }
            ],
            "feedback": "Siempre puedes pedir \"explícamelo simple\". La IA lo repetirá de forma más fácil."
          },
          {
            "pregunta": "Para hacer una buena pregunta, ¿necesitas dar tu RUT?",
            "opciones": [
              {
                "texto": "No, nunca hace falta dar datos personales",
                "correcta": True
              },
              {
                "texto": "Sí, siempre",
                "correcta": False
              },
              {
                "texto": "Solo si la pregunta es larga",
                "correcta": False
              }
            ],
            "feedback": "Puedes preguntar por cualquier tema de salud sin decir quién eres. Tus datos son tuyos."
          },
          {
            "pregunta": "¿Es una buena pregunta para la IA: \"Tengo dolor en el pecho. ¿Qué debo hacer?\"?",
            "opciones": [
              
              {
                "texto": "Sí, es una pregunta clara y concreta",
                "correcta": False
              },
              {
                "texto": "No, es una emergencia. Llama al 131 de inmediato.",
                "correcta": True
              },
              {
                "texto": "Sí, la IA puede orientarte sobre cualquier síntoma",
                "correcta": False
              }
            ],
            "feedback": "El dolor en el pecho es una emergencia. La IA no puede ayudar con síntomas urgentes. Una mejor pregunta sería: \"¿Cuáles son las causas comunes del dolor de pecho?\" y solo DESPUÉS de ver al médico."
          }
        ],
        "resultado": {
          "umbral_aprobado": 4,
          "titulo_aprobado": "¡Excelente Trabajo!",
          "mensaje_aprobado": "Tienes una buena comprensión de este tema. ¡Sigue así!",
          "titulo_fallido": "¡Casi lo logras!",
          "mensaje_fallido": "No te preocupes, puedes volver a repasar la lección cuando quieras."
        }
      }
    }
  },
  {
    "leccion_id": "2.2",
    "modulo_id": 2,
    "orden": 2,
    "titulo": "Leer una respuesta",
    "duracion_min": 4,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "concepto",
          "titulo": "La IA siempre responde, aunque no sepa",
          "texto": "La IA siempre responde algo, aunque no sepa la respuesta. Tu trabajo es saber cuándo confiar y cuándo dudar. En esta lección aprenderás a leer las señales que te da la propia respuesta.",
          "apoyo_visual": "Ilustración de una respuesta con \"señales\" resaltadas como pistas."
        },
        {
          "n": 2,
          "tipo": "concepto",
          "titulo": "Señal 1: cuando generaliza",
          "texto": "Si la respuesta dice \"generalmente...\" o \"en la mayoría de los casos...\", la IA está generalizando. Tu caso puede ser distinto. Es una señal de que conviene confirmarlo con tu médico.",
          "apoyo_visual": "Frase \"generalmente...\" resaltada en ámbar."
        },
        {
          "n": 3,
          "tipo": "concepto",
          "titulo": "Señal 2: cuando reconoce su límite",
          "texto": "Si la respuesta dice \"le recomiendo consultar a un médico\", la IA está reconociendo su límite. Hazle caso: esa es una buena IA siendo honesta contigo.",
          "apoyo_visual": "Frase \"consulte a un médico\" resaltada en verde con un visto bueno."
        },
        {
          "n": 4,
          "tipo": "concepto",
          "titulo": "Señal 3: cuando adivina",
          "texto": "Si la respuesta dice \"podría ser X, Y o Z\", la IA está adivinando entre opciones, no diagnosticando. Eso significa que no está segura, y tú tampoco deberías estarlo.",
          "apoyo_visual": "Frase \"podría ser A, B o C\" con un signo de interrogación."
        },
        {
          "n": 5,
          "tipo": "cierre",
          "titulo": "En resumen",
          "texto": "Aprende a leer las señales: \"generalmente\" = generaliza; \"consulte a un médico\" = reconoce su límite; \"podría ser\" = está adivinando. Una IA que duda en temas de salud no es mala: es honesta.",
          "apoyo_visual": "Resumen con las tres señales y marca de avance."
        }
      ],
      "ejercicio": {
        "tipo": "etiquetar_respuestas",
        "instruccion": "Arrastra la etiqueta correcta a cada respuesta de la IA.",
        "descripcion": "Pantalla con respuestas de IA. El usuario arrastra etiquetas: \"información útil\", \"debo consultar al médico\", \"cuidado, la IA está adivinando\".",
        "items": [
          {
            "respuesta_ia": "La hipertensión es cuando la presión arterial está sobre 140/90 de forma constante. Es importante medirla regularmente.",
            "etiquetas": [
              "información útil"
            ]
          },
          {
            "respuesta_ia": "Sus síntomas podrían ser de gastritis, úlcera o reflujo. Es difícil decir sin examinarlo. Le recomiendo ir a urgencias si el dolor es fuerte.",
            "etiquetas": [
              "debo consultar al médico",
              "cuidado, la IA está adivinando"
            ]
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
        {
          "pregunta": "Si la IA te dice \"podría ser indigestión o algo más serio\", ¿qué significa?",
          "opciones": [
          
            {
              "texto": "Que tienes indigestión seguro",
              "correcta": False
            },
              {
              "texto": "La IA no está segura, mejor ve al médico",
              "correcta": True
            },
            {
              "texto": "Que no es nada grave",
              "correcta": False
            }
          ],
          "feedback": "\"Podría ser\" significa que la IA está adivinando entre opciones. Ante la duda, consulta a un profesional."
        },
        {
          "pregunta": "¿La IA tiene que sonar dudosa para ser confiable?",
          "opciones": [
            {
              "texto": "No necesariamente, pero la duda en temas médicos es buena señal",
              "correcta": True
            },
            {
              "texto": "Sí, si no duda es mentira",
              "correcta": False
            },
            {
              "texto": "No, mientras más segura mejor siempre",
              "correcta": False
            }
          ],
          "feedback": "Que la IA reconozca sus límites en salud es señal de honestidad, no de error."
        },
        {
          "pregunta": "Una IA te dice con mucha seguridad \"usted tiene diabetes\". ¿Confías?",
          "opciones": [
           
            {
              "texto": "Sí, porque lo dijo con seguridad",
              "correcta": False
            },
             {
              "texto": "No, un diagnóstico requiere exámenes; la IA no puede diagnosticar",
              "correcta": True
            },
            {
              "texto": "Sí, empiezo el tratamiento de inmediato",
              "correcta": False
            }
          ],
          "feedback": "Ninguna IA puede diagnosticar. Un diagnóstico necesita exámenes y la evaluación de un médico."
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
    "leccion_id": "2.3",
    "modulo_id": 2,
    "orden": 3,
    "titulo": "Verificar la información",
    "duracion_min": 4,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "concepto",
          "titulo": "Confiar, pero verificar",
          "texto": "La IA puede equivocarse, así que antes de actuar sobre algo importante de tu salud, conviene verificarlo. Verificar significa confirmar lo que leíste en otra fuente confiable. Es un hábito que te protege.",
          "apoyo_visual": "Ilustración de una afirmación pasando por un \"filtro de verificación\"."
        },
        {
          "n": 2,
          "tipo": "concepto",
          "titulo": "Cuáles son las fuentes confiables",
          "texto": "Las fuentes confiables en salud son: tu médico o tu equipo del hospital, los sitios oficiales que terminan en gob.cl, y el personal del consultorio o farmacia. Un comentario en redes sociales o una cadena de WhatsApp NO son fuentes confiables.",
          "apoyo_visual": "Dos columnas: confiables (médico, gob.cl, consultorio) vs. no confiables (redes, cadenas de WhatsApp)."
        },
        {
          "n": 3,
          "tipo": "concepto",
          "titulo": "La regla de las dos fuentes",
          "texto": "Una regla fácil de recordar: si la IA te dice algo importante de salud, búscalo en una segunda fuente confiable. Si las dos coinciden, mejor. Si no coinciden, hazle caso al profesional de salud, no a la IA.",
          "apoyo_visual": "Balanza: IA en un lado, fuente confiable en el otro; gana el profesional."
        },
        {
          "n": 4,
          "tipo": "ejemplo_real",
          "titulo": "Verificar en acción",
          "texto": "Carlos leyó en una IA que cierto té reemplazaba su remedio para la presión. Antes de dejar el remedio, le preguntó a su médico en el control. Ella le explicó que de ninguna manera lo reemplazaba. Verificar le evitó un riesgo grave.",
          "apoyo_visual": "Viñeta del caso de Carlos confirmando con su médico."
        },
        {
          "n": 5,
          "tipo": "cierre",
          "titulo": "En resumen",
          "texto": "Antes de actuar sobre tu salud, verifica lo que dice la IA con una fuente confiable. Si hay desacuerdo, manda el profesional. Verificar no es desconfiar: es cuidarte.",
          "apoyo_visual": "Resumen con la regla de las dos fuentes y marca de avance."
        }
      ],
      "ejercicio": {
        "tipo": "clasificar_fuente",
        "instruccion": "¿Es una fuente CONFIABLE o NO confiable para verificar?",
        "descripcion": "El usuario clasifica fuentes de información de salud. Refuerza dónde confirmar lo que dice la IA.",
        "items": [
          {
            "fuente": "Tu médico en el control",
            "respuesta": "CONFIABLE"
          },
          {
            "fuente": "Una cadena de WhatsApp de un grupo familiar",
            "respuesta": "NO CONFIABLE"
          },
          {
            "fuente": "El sitio del hospital que termina en gob.cl",
            "respuesta": "CONFIABLE"
          },
          {
            "fuente": "Un comentario anónimo en redes sociales",
            "respuesta": "NO CONFIABLE"
          },
          {
            "fuente": "El farmacéutico del consultorio",
            "respuesta": "CONFIABLE"
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
        {
          "pregunta": "¿Cuál de estas es una fuente confiable para verificar información de salud?",
          "opciones": [
            {
              "texto": "Tu médico o un sitio oficial gob.cl",
              "correcta": True
            },
            {
              "texto": "Una cadena de WhatsApp",
              "correcta": False
            },
            {
              "texto": "Un comentario en redes sociales",
              "correcta": False
            }
          ],
          "feedback": "Tu médico y los sitios oficiales gob.cl son fuentes confiables. Las cadenas y comentarios no lo son."
        },
        {
          "pregunta": "La IA y tu médico te dicen cosas distintas. ¿A quién le haces caso?",
          "opciones": [
            
            {
              "texto": "A la IA, porque responde más rápido",
              "correcta": False
            },
            {
              "texto": "Al que diga lo que más me gusta",
              "correcta": False
            },
            {
              "texto": "Al médico",
              "correcta": True
            }
          ],
          "feedback": "Si hay desacuerdo, siempre manda el profesional de salud. La IA solo orienta."
        },
        {
          "pregunta": "¿Por qué conviene verificar lo que dice la IA?",
          "opciones": [
            
            {
              "texto": "Porque la IA siempre miente",
              "correcta": False
            },
            {
              "texto": "No conviene, hay que creerle todo",
              "correcta": False
            },
            {
              "texto": "Porque la IA puede equivocarse y mi salud es importante",
              "correcta": True
            }
          ],
          "feedback": "La IA puede equivocarse. Verificar lo importante en una fuente confiable te protege."
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
    "leccion_id": "2.4",
    "modulo_id": 2,
    "orden": 4,
    "titulo": "Casos por patología",
    "duracion_min": 5,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "intro",
          "titulo": "Pongamos todo en práctica",
          "texto": "Ya sabes preguntar bien, leer respuestas y verificar. Ahora veremos casos reales con las cinco enfermedades más comunes en personas mayores. Recuerda: todo esto es orientación, nunca reemplaza a tu médico.",
          "apoyo_visual": "Cinco tarjetas con las patologías base. Aviso visible: \"contenido educativo, no diagnóstico\"."
        },
        {
          "n": 2,
          "tipo": "caso_patologia",
          "titulo": "Hipertensión (presión alta)",
          "texto": "Pregunta útil: \"¿Qué cuidados generales ayudan a mantener la presión controlada?\". La IA puede orientarte sobre hábitos como reducir la sal o caminar. Lo que NO puede: decirte tu dosis de remedio ni si tu presión de hoy es peligrosa. Eso lo ve tu médico.",
          "apoyo_visual": "Ícono de tensiómetro. Pregunta útil vs. lo que es del médico."
        },
        {
          "n": 3,
          "tipo": "caso_patologia",
          "titulo": "Diabetes tipo 2",
          "texto": "Pregunta útil: \"¿Qué alimentos conviene cuidar si tengo azúcar alta?\". La IA orienta sobre alimentación general. Lo que NO puede: ajustar tu insulina ni interpretar tu examen de glicemia. Eso es del equipo de salud.",
          "apoyo_visual": "Ícono de gota/glucómetro. Pregunta útil vs. lo que es del médico."
        },
        {
          "n": 4,
          "tipo": "caso_patologia",
          "titulo": "Artrosis (dolor de articulaciones)",
          "texto": "Pregunta útil: \"¿Qué ejercicios suaves ayudan con el dolor de rodillas?\". La IA orienta sobre cuidados generales. Lo que NO puede: recetarte analgésicos ni decirte si necesitas una operación. Eso lo decide el traumatólogo.",
          "apoyo_visual": "Ícono de articulación. Pregunta útil vs. lo que es del médico."
        },
        {
          "n": 5,
          "tipo": "caso_patologia",
          "titulo": "Colesterol alto",
          "texto": "Pregunta útil: \"¿Qué significa tener el colesterol alto y por qué importa?\". La IA explica el concepto. Lo que NO puede: leer tu perfil lipídico ni indicarte un medicamento. Eso lo evalúa tu médico con tus exámenes.",
          "apoyo_visual": "Ícono de corazón/arteria. Pregunta útil vs. lo que es del médico."
        },
        {
          "n": 6,
          "tipo": "caso_patologia",
          "titulo": "Insuficiencia venosa (várices, piernas hinchadas)",
          "texto": "Pregunta útil: \"¿Qué cuidados ayudan a las piernas hinchadas en el día a día?\". La IA orienta sobre hábitos como elevar las piernas. Lo que NO puede: diagnosticar la gravedad ni indicar tratamiento. Eso lo ve tu médico.",
          "apoyo_visual": "Ícono de pierna. Pregunta útil vs. lo que es del médico."
        },
        {
          "n": 7,
          "tipo": "cierre",
          "titulo": "El patrón es siempre el mismo",
          "texto": "En las cinco enfermedades, el patrón se repite: la IA SÍ orienta y explica; NO diagnostica, NO receta, NO interpreta exámenes. Si tienes claro ese límite, puedes usar la IA con confianza para cada una de tus condiciones.",
          "apoyo_visual": "Resumen del patrón común SÍ/NO con marca de avance."
        }
      ],
      "ejercicio": {
        "tipo": "pregunta_util_o_no",
        "instruccion": "Para cada patología, ¿esta pregunta es ÚTIL para la IA o es algo DEL MÉDICO?",
        "descripcion": "El usuario clasifica preguntas reales por patología. Refuerza el límite orientación/clínica. Sin penalización.",
        "items": [
          {
            "patologia": "Hipertensión",
            "pregunta": "¿Qué hábitos ayudan a cuidar la presión?",
            "respuesta": "ÚTIL"
          },
          {
            "patologia": "Hipertensión",
            "pregunta": "¿Qué dosis de mi remedio debo tomar hoy?",
            "respuesta": "DEL MÉDICO"
          },
          {
            "patologia": "Diabetes tipo 2",
            "pregunta": "¿Qué significa mi examen de glicemia 180?",
            "respuesta": "DEL MÉDICO"
          },
          {
            "patologia": "Diabetes tipo 2",
            "pregunta": "¿Qué alimentos conviene cuidar con el azúcar alta?",
            "respuesta": "ÚTIL"
          },
          {
            "patologia": "Artrosis",
            "pregunta": "¿Qué ejercicios suaves alivian el dolor de rodilla?",
            "respuesta": "ÚTIL"
          },
          {
            "patologia": "Artrosis",
            "pregunta": "¿Necesito una operación de rodilla?",
            "respuesta": "DEL MÉDICO"
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
        {
          "pregunta": "Para la hipertensión, ¿qué pregunta es apropiada para la IA?",
          "opciones": [
            
            {
              "texto": "¿Qué dosis de remedio tomo hoy?",
              "correcta": False
            },
            {
              "texto": "¿Mi presión de ahora es peligrosa?",
              "correcta": False
            },
            {
              "texto": "¿Qué hábitos ayudan a cuidar la presión?",
              "correcta": True
            }
          ],
          "feedback": "La IA orienta sobre hábitos generales. La dosis y la urgencia las evalúa tu médico."
        },
        {
          "pregunta": "Tienes diabetes y quieres entender tu examen de glicemia. ¿Quién debe interpretarlo?",
          "opciones": [
            
            {
              "texto": "La IA, que da el número exacto",
              "correcta": False
            },
            {
              "texto": "Tu equipo de salud",
              "correcta": True
            },
            {
              "texto": "Un familiar por WhatsApp",
              "correcta": False
            }
          ],
          "feedback": "Interpretar exámenes es tarea clínica. La IA puede explicarte qué es la glicemia, pero no leer tu resultado."
        },
        {
          "pregunta": "En las cinco patologías, ¿qué cosa NUNCA hace la IA?",
          "opciones": [
            
            {
              "texto": "Explicar qué es la enfermedad",
              "correcta": False
            },
            {
              "texto": "Diagnosticar, recetar o interpretar tus exámenes",
              "correcta": True
            },
            {
              "texto": "Orientar sobre hábitos generales",
              "correcta": False
            }
          ],
          "feedback": "El patrón es siempre el mismo: la IA orienta y explica, pero nunca diagnostica, receta ni interpreta exámenes."
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
    "leccion_id": "2.5",
    "modulo_id": 2,
    "orden": 5,
    "titulo": "Preparar tu consulta médica",
    "duracion_min": 5,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "concepto",
          "titulo": "La IA te ayuda a llegar mejor preparado",
          "texto": "La IA puede ayudarte a llegar mejor preparado a tu consulta médica. No reemplaza a tu médico: te ayuda a aprovechar mejor el tiempo con él. Esta es, quizás, la forma más valiosa de usarla.",
          "apoyo_visual": "Ilustración de una persona mayor llegando confiada a su consulta con una lista en la mano."
        },
        {
          "n": 2,
          "tipo": "concepto",
          "titulo": "Uso 1: hacer una lista de preguntas",
          "texto": "Antes de tu consulta, puedes pedirle a la IA que te ayude a armar una lista de preguntas para tu médico. Así no se te olvida nada importante cuando estés frente a él.",
          "apoyo_visual": "Lista de preguntas generada para llevar a la consulta."
        },
        {
          "n": 3,
          "tipo": "concepto",
          "titulo": "Uso 2: entender palabras médicas",
          "texto": "Si en un examen o en la consulta escuchaste una palabra que no entendiste, la IA te la explica en simple. Así llegas sabiendo de qué te están hablando.",
          "apoyo_visual": "Ejemplo: \"insuficiencia venosa\" → explicación simple."
        },
        {
          "n": 4,
          "tipo": "concepto",
          "titulo": "Uso 3: ordenar tus síntomas",
          "texto": "La IA te puede ayudar a recordar y ordenar tus síntomas: ¿Cuándo empezó?, ¿Qué sientes?, ¿Qué lo empeora?. Contarle esto ordenado a tu médico le sirve muchísimo para ayudarte mejor.",
          "apoyo_visual": "Guía de tres preguntas: ¿cuándo empezó?, ¿qué siento?, ¿qué lo empeora?"
        },
        {
          "n": 5,
          "tipo": "demostracion",
          "titulo": "Veámoslo paso a paso",
          "texto": "El paciente pregunta: \"voy a ir al cardiólogo, ¿qué preguntas debería hacerle?\". La IA le responde con cinco preguntas útiles. El paciente las anota o las imprime y las lleva a su consulta. Simple y poderoso.",
          "apoyo_visual": "Demostración de la conversación y el paciente anotando las preguntas."
        },
        {
          "n": 6,
          "tipo": "cierre",
          "titulo": "En resumen",
          "texto": "Usa la IA para preparar tu consulta: arma preguntas, entiende palabras difíciles y ordena tus síntomas. Así la IA potencia tu relación con tu médico, en lugar de reemplazarla.",
          "apoyo_visual": "Resumen con los tres usos y marca de avance."
        }
      ],
      "ejercicio": {
        "tipo": "construye_tu_consulta",
        "instruccion": "Elige una situación y marca las TRES preguntas más útiles para llevar al médico.",
        "descripcion": "El usuario elige una situación de tres opciones (voy al cardiólogo por presión alta, tengo cita con el diabetólogo, o me derivaron al traumatólogo por dolor de rodilla). Luego aparecen seis preguntas posibles y debe marcar las tres más útiles.",
        "situacion_ejemplo": "voy al cardiólogo",
        "items": [
          {
            "pregunta": "¿Qué medicamento debo tomar?",
            "util": False,
            "motivo": "Lo decide el cardiólogo."
          },
          {
            "pregunta": "¿Qué actividades físicas son seguras para mí?",
            "util": True,
            "motivo": None
          },
          {
            "pregunta": "¿Cuándo es momento de preocuparme por la presión?",
            "util": True,
            "motivo": None
          },
          {
            "pregunta": "¿Cuál es la cura definitiva?",
            "util": False,
            "motivo": "No existe; pregunta mal formulada."
          },
          {
            "pregunta": "¿Cómo afecta mi presión a otros aspectos de mi salud?",
            "util": True,
            "motivo": None
          },
          {
            "pregunta": "¿La IA puede operarme?",
            "util": False,
            "motivo": "Evalúa si entendiste que la IA no reemplaza al médico."
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
        {
          "pregunta": "¿La IA puede reemplazar a tu cardiólogo?",
          "opciones": [
            
            {
              "texto": "Sí, es igual que un especialista",
              "correcta": False
            },
            {
              "texto": "No, solo te ayuda a prepararte",
              "correcta": True
            },
            {
              "texto": "Sí, si le cuentas todo",
              "correcta": False
            }
          ],
          "feedback": "La IA te ayuda a preparar tu consulta, pero nunca reemplaza a tu médico."
        },
        {
          "pregunta": "Antes de tu consulta médica, la IA puede ayudarte a...",
          "opciones": [
            {
              "texto": "Preparar preguntas que quieres hacer",
              "correcta": True
            },
            {
              "texto": "Elegir tu medicamento",
              "correcta": False
            },
            {
              "texto": "Cancelar la cita",
              "correcta": False
            }
          ],
          "feedback": "La IA es ideal para preparar preguntas y llegar más seguro a tu consulta."
        },
        {
          "pregunta": "Tu médico te dijo \"tiene insuficiencia venosa\". ¿Para qué te sirve la IA?",
          "opciones": [
            
            {
              "texto": "Para cambiar el diagnóstico",
              "correcta": False
            },
            {
              "texto": "Para entender qué significa esa palabra y prepararte",
              "correcta": True
            },
            {
              "texto": "Para recetarte el tratamiento",
              "correcta": False
            }
          ],
          "feedback": "La IA te explica el término en simple, y así llegas más preparado a tu próxima consulta."
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
    "leccion_id": "2.6",
    "modulo_id": 2,
    "orden": 6,
    "titulo": "Cuándo NO usar la IA",
    "duracion_min": 4,
    "contenido": {
      "paginas": [
        {
          "n": 1,
          "tipo": "concepto",
          "titulo": "Cuándo NO usar la IA",
          "texto": "Hay momentos en que perder tiempo con la IA puede ser peligroso. Aprende a reconocerlos. Esta información puede salvar tu vida o la de alguien cercano.",
          "apoyo_visual": "Encabezado en rojo de emergencia. Tono serio, sin alarmar.",
          "fuente_prototipo": True
        },
        {
          "n": 2,
          "tipo": "alerta_emergencia",
          "titulo": "Llama al 131 si tienes:",
          "texto": "Estas son señales de urgencia que NO se le preguntan a la IA. Si presentas alguna, llama de inmediato al 131 o ve a urgencias:",
          "lista_sintomas": [
            "Dolor fuerte en el pecho",
            "Dificultad para respirar",
            "Pérdida de fuerza en un lado del cuerpo",
            "Habla confusa",
            "Desmayos",
            "Sangrado que no para",
            "Caídas con golpe fuerte en la cabeza"
          ],
          "apoyo_visual": "Caja de alerta roja con lista de síntomas (igual que en el prototipo).",
          "fuente_prototipo": True
        },
        {
          "n": 3,
          "tipo": "numeros_emergencia",
          "titulo": "Números de emergencia",
          "texto": "Guarda estos números. En una emergencia, llamar es siempre lo primero, antes que cualquier app:",
          "numeros": [
            {
              "servicio": "SAMU",
              "numero": "131"
            },
            {
              "servicio": "Bomberos",
              "numero": "132"
            },
            {
              "servicio": "Carabineros",
              "numero": "133"
            }
          ],
          "apoyo_visual": "Tarjetas con números grandes (igual que en el prototipo).",
          "fuente_prototipo": True
        },
        {
          "n": 4,
          "tipo": "concepto",
          "titulo": "Y para estos casos, tu médico de cabecera",
          "texto": "No todo es urgencia, pero tampoco todo es para la IA. Cosas como un dolor que dura semanas, sentirte muy triste o sin ánimo por mucho tiempo, o un malestar que no mejora, son para tu médico de cabecera, no para el chatbot.",
          "apoyo_visual": "Tres situaciones para médico de cabecera con ícono de médico."
        },
        {
          "n": 5,
          "tipo": "cierre",
          "titulo": "Ante la duda, consulta a un profesional",
          "texto": "Si dudas, mejor ve al hospital: una consulta de más nunca es un error. Ante la duda, siempre consulta con un profesional de salud. La IA es para aprender y orientarte, no para emergencias.",
          "apoyo_visual": "Mensaje de cierre destacado (disclaimer del prototipo).",
          "fuente_prototipo": True
        }
      ],
      "ejercicio": {
        "tipo": "ia_medico_o_urgencias",
        "instruccion": "Clasifica cada situación: ¿IA, MÉDICO DE CABECERA o URGENCIAS YA?",
        "descripcion": "Aparecen seis situaciones y el usuario clasifica con tres botones. Es el ejercicio más importante de la plataforma.",
        "items": [
          {
            "situacion": "Quiero entender qué es el colesterol alto",
            "respuesta": "IA"
          },
          {
            "situacion": "Hace una hora me empezó un dolor fuerte en el pecho que me llega al brazo",
            "respuesta": "URGENCIAS YA"
          },
          {
            "situacion": "Tengo dolor de espalda desde hace dos semanas",
            "respuesta": "MÉDICO DE CABECERA"
          },
          {
            "situacion": "Acabo de caer y me golpeé la cabeza, me siento mareado",
            "respuesta": "URGENCIAS YA"
          },
          {
            "situacion": "¿Qué alimentos son buenos para la presión?",
            "respuesta": "IA"
          },
          {
            "situacion": "Me siento muy triste hace meses y no tengo ganas de nada",
            "respuesta": "MÉDICO DE CABECERA"
          }
        ]
      },
      "quiz_corto": {
        "preguntas": [
        {
          "pregunta": "Si tienes dolor fuerte en el pecho, ¿qué haces primero?",
          "opciones": [
            
            {
              "texto": "Le preguntas a la IA",
              "correcta": False
            },
            {
              "texto": "Buscas en Google",
              "correcta": False
            },
            {
              "texto": "Llamas al 131 o vas a urgencias",
              "correcta": True
            }
          ],
          "feedback": "El dolor fuerte en el pecho es una urgencia. Llama al 131 de inmediato; no pierdas tiempo con la IA."
        },
        {
          "pregunta": "¿La IA es buena para emergencias?",
          "opciones": [
            {
              "texto": "No, pierdes tiempo valioso",
              "correcta": True
            },
            {
              "texto": "Sí, responde más rápido que el SAMU",
              "correcta": False
            },
            {
              "texto": "Sí, si escribes rápido",
              "correcta": False
            }
          ],
          "feedback": "En una emergencia, cada minuto cuenta. Llamar al 131 es siempre lo primero."
        },
        {
          "pregunta": "Si dudas si algo es urgente, ¿es mejor sobreestimar o subestimar?",
          "opciones": [
            
            {
              "texto": "Subestimar: esperar a ver si pasa",
              "correcta": False
            },
            {
              "texto": "Preguntarle a la IA y esperar",
              "correcta": False
            },
            {
              "texto": "Sobreestimar: mejor una consulta de más",
              "correcta": True
            },
          ],
          "feedback": "Ante la duda, sobreestima. Una consulta de más nunca es un error; una urgencia perdida sí."
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
            "texto": "Una persona del hospital que responde en secreto",
            "correcta": False
          },
          {
            "texto": "Un programa que aprende de muchos ejemplos para ayudarte",
            "correcta": True
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
            "texto": "Sí, porque sonó muy segura",
            "correcta": False
          },
          {
            "texto": "Sí, si usó palabras difíciles",
            "correcta": False
          },
          {
            "texto": "No, lo confirmo con un profesional",
            "correcta": True
          }
        ],
        "feedback": "Sonar segura no es tener la razón. Lo importante se confirma con tu médico o farmacéutico."
      },
      {
        "pregunta": "¿Cuál de estos datos NO debes compartir nunca con una IA?",
        "opciones": [
          
          {
            "texto": "Una duda general sobre la diabetes",
            "correcta": False
          },
          {
            "texto": "Tu RUT y tu clave del banco",
            "correcta": True
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
            "texto": "Te dan información gratis",
            "correcta": False
          },
          {
            "texto": "La página tiene fotos",
            "correcta": False
          },
          {
            "texto": "Te prometen una cura milagrosa",
            "correcta": True
          }
        ],
        "feedback": "Las curas milagrosas no existen: son la señal más clara de estafa."
      },
      {
        "pregunta": "Si no entiendes algo en la app, ¿qué puedes hacer?",
        "opciones": [
          
          {
            "texto": "Cerrar la app y no volver",
            "correcta": False
          },
          {
            "texto": "Nada, seguir aunque no entiendas",
            "correcta": False
          },
          {
            "texto": "Volver a leer la lección o preguntar al chatbot",
            "correcta": True
          }
        ],
        "feedback": "Puedes volver atrás a releer cuantas veces quieras y también preguntarle al asistente."
      }
    ]
  },
  {
    "quiz_final_id": "QF2",
    "modulo_id": 2,
    "titulo": "Quiz final — Practicar con la IA",
    "minimo_aciertos": 5,
    "bloqueante": False,
    "preguntas": [
      {
        "pregunta": "¿Cuál es una mejor pregunta para hacerle a la IA?",
        "opciones": [
          
          {
            "texto": "Me siento raro, ¿qué será?",
            "correcta": False
          },
          {
            "texto": "¿Qué cuidados necesita una persona con presión alta?",
            "correcta": True
          },
          {
            "texto": "Hola, ¿cómo estás?",
            "correcta": False
          }
        ],
        "feedback": "Una pregunta concreta y sin datos personales da las respuestas más útiles.",
        "submodulo": "2.1"
      },
      {
        "pregunta": "Si la IA dice \"podría ser indigestión o algo más serio\", ¿qué significa?",
        "opciones": [
          {
            "texto": "La IA no está segura, mejor ve al médico",
            "correcta": True
          },
          {
            "texto": "Que es indigestión seguro",
            "correcta": False
          },
          {
            "texto": "Que no es nada",
            "correcta": False
          }
        ],
        "feedback": "\"Podría ser\" es la IA adivinando. Ante la duda, consulta a un profesional.",
        "submodulo": "2.2"
      },
      {
        "pregunta": "La IA y tu médico te dicen cosas distintas. ¿A quién le haces caso?",
        "opciones": [
          {
            "texto": "Al médico",
            "correcta": True
          },
          {
            "texto": "A la IA, que es más rápida",
            "correcta": False
          },
          {
            "texto": "Al que más me convenga",
            "correcta": False
          }
        ],
        "feedback": "Si hay desacuerdo, siempre manda el profesional de salud.",
        "submodulo": "2.3"
      },
      {
        "pregunta": "En cualquier patología, ¿qué cosa NUNCA hace la IA?",
        "opciones": [
          
          {
            "texto": "Explicar qué es la enfermedad",
            "correcta": False
          },
          {
            "texto": "Orientar sobre hábitos generales",
            "correcta": False
          },
          {
            "texto": "Diagnosticar, recetar o interpretar tus exámenes",
            "correcta": True
          }
        ],
        "feedback": "La IA orienta y explica; nunca diagnostica, receta ni interpreta exámenes.",
        "submodulo": "2.4"
      },
      {
        "pregunta": "Antes de tu consulta médica, la IA puede ayudarte a...",
        "opciones": [
          
          {
            "texto": "Elegir tu medicamento",
            "correcta": False
          },
          {
            "texto": "Cancelar la cita",
            "correcta": False
          },
          {
            "texto": "Preparar las preguntas que quieres hacerle al doctor",
            "correcta": True
          }
        ],
        "feedback": "La IA es ideal para preparar tu consulta y aprovechar mejor el tiempo con tu médico.",
        "submodulo": "2.5"
      },
      {
        "pregunta": "Si tienes dolor fuerte en el pecho, ¿qué haces primero?",
        "opciones": [
          
          {
            "texto": "Le preguntas a la IA",
            "correcta": False
          },
          {
            "texto": "Llamas al 131 o vas a urgencias",
            "correcta": True
          },
          {
            "texto": "Buscas en internet",
            "correcta": False
          }
        ],
        "feedback": "Es una urgencia. Llama al 131 de inmediato; no pierdas tiempo con la IA.",
        "submodulo": "2.6"
      },
      {
        "pregunta": "Si dudas si algo es urgente, ¿qué es mejor?",
        "opciones": [
          
          {
            "texto": "Esperar a ver si se pasa solo",
            "correcta": False
          },
          {
            "texto": "Sobreestimar: mejor una consulta de más",
            "correcta": True
          },
          {
            "texto": "Preguntarle a la IA y esperar",
            "correcta": False
          }
        ],
        "feedback": "Ante la duda, sobreestima. Una consulta de más nunca es un error.",
        "submodulo": "2.6"
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
