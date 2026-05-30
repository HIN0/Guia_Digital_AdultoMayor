"use client"

import { useEffect, useRef, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import Image from "next/image"
import Header from "@/components/layout/Header"
import { Trophy, RefreshCw } from "lucide-react"
import { getLeccion, completarLeccion, type LeccionDetalle, type PreguntaQuizCorto } from "@/lib/api"

const IMAGENES_APOYO: Record<string, string> = {
  // L1 — Bienvenida y navegación
  'Ilustración cálida de una persona mayor sonriendo frente a un teléfono. Botón verde grande "Comenzar".': "/lecciones/L1-1.svg",
  "Flechas animadas señalando: ① la flecha ← para Volver, ② el menú principal (Inicio), ③ el botón de Chat, ④ el botón de progreso, ⑤ el ajuste de tamaño de letra (selector de tamaño de letra).": "/lecciones/L1-2.svg",
  "Demostración del selector Pequeño / Mediano / Grande cambiando el tamaño del texto en vivo.": "/lecciones/L1-3.svg",
  "Guía paso a paso con refuerzo positivo después de cada toque.": "/lecciones/L1-4.svg",
  "Mensaje de felicitación con marca de avance del módulo.": "/lecciones/L1-5.svg",
  // L2 — ¿Qué es la IA?
  "Ilustración simple: un computador rodeado de ejemplos con una flecha que sale hacia una respuesta.": "/lecciones/L2-1.svg",
  "Cuatro tarjetas: 📷 reconocer cara, ✍️ corregir texto, 🗺️ sugerir ruta, 🔊 asistente de voz.": "/lecciones/L2-2.svg",
  "Analogía visual del aprendizaje por ejemplos.": "/lecciones/L2-3.svg",
  "Comparación: calculadora 🧮 = herramienta útil / IA 🤖 = herramienta útil.": "/lecciones/L2-4.svg",
  "Ilustración de un chatbot conversando con un usuario.": "/lecciones/L2-5.svg",
  "Resumen con tres viñetas y marca de avance.": "/lecciones/L2-6.svg",
  // L3 — La IA en salud
  "Ícono de corazón con un signo de ayuda.": "/lecciones/L3-1.svg",
  "Tres tarjetas: 📖 explicar palabras, ℹ️ información general, ⏰ recordatorios.": "/lecciones/L3-2.svg",
  "Viñeta ilustrada de don Luis consultando la app en casa.": "/lecciones/L3-3.svg",
  'Lista con íconos rojos de "no" frente a cada límite.': "/lecciones/L3-4.svg",
  // L5 — Privacidad y datos
  "Ilustración de una plaza con mucha gente escuchando, frente a una consulta médica cerrada.": "/lecciones/L5-1.svg",
  "Lista verde: síntomas en general, dudas sobre una enfermedad, preguntas de orientación.": "/lecciones/L5-2.svg",
  "Lista roja: RUT, dirección, Fonasa, fotos con nombre, tarjeta bancaria, contraseñas.": "/lecciones/L5-3.svg",
  "Viñeta del caso de María recibiendo publicidad no deseada.": "/lecciones/L5-4.svg",
  "Mensaje de cierre destacado con candado 🔒.": "/lecciones/L5-5.svg",
  // L6 — Reconocer engaños
  "Ilustración de un mensaje con disfraz de hospital y una alerta.": "/lecciones/L6-1.svg",
  "Tres tarjetas de alerta: 🪄 cura milagrosa, ⏱️ te apura, 💳 te pide pagar.": "/lecciones/L6-2.svg",
  "Pasos ilustrados: buscar en Google, llamar al número oficial, no tocar links de WhatsApp.": "/lecciones/L6-3.svg",
  "Capturas comparadas: mensaje falso vs. sitio oficial gob.cl.": "/lecciones/L6-4.svg",
  "Resumen con las tres señales y la acción de verificar.": "/lecciones/L6-5.svg",
  // L4 — Riesgos y limitaciones
  "Ilustración de un robot hablando con tono seguro mientras un signo de interrogación flota encima.": "/lecciones/L4-1.svg",
  "Ejemplo de una respuesta inventada marcada con una lupa y la palabra \"alucinación\".": "/lecciones/L4-2.svg",
  "Calendario con una fecha de corte y un reloj indicando \"puede estar atrasada\".": "/lecciones/L4-3.svg",
  "Comparación: una multitud (lo general) frente a una sola persona destacada (tu caso).": "/lecciones/L4-4.svg",
  "Viñeta del caso con mensaje: \"confirmar la salvó de un error\".": "/lecciones/L4-5.svg",
  "Resumen con tres riesgos y la regla de oro destacada.": "/lecciones/L4-6.svg",
}

type Fase = "paginas" | "quiz" | "resultado"

interface EstadoQuiz {
  indice: number
  seleccion: number | null
  mostrandoFeedback: boolean
  aciertos: number
}

export default function LeccionPage() {
  const params = useParams()
  const router = useRouter()
  const moduloId = Number(params.id as string)
  const leccionId = Number(params.leccion_id as string)

  const [leccion, setLeccion] = useState<LeccionDetalle | null>(null)
  const [error, setError] = useState(false)
  const [paginaActual, setPaginaActual] = useState(0)
  const [fase, setFase] = useState<Fase>("paginas")
  const [quiz, setQuiz] = useState<EstadoQuiz>({
    indice: 0,
    seleccion: null,
    mostrandoFeedback: false,
    aciertos: 0,
  })
  const [aprobado, setAprobado] = useState(false)
  const [tocandoAudio, setTocandoAudio] = useState(false)
  const audioRef = useRef<HTMLAudioElement | null>(null)

  function detenerAudio() {
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current.currentTime = 0
    }
    setTocandoAudio(false)
  }

  function toggleAudio(numero: number) {
    if (audioRef.current && !audioRef.current.paused) {
      detenerAudio()
      return
    }
    detenerAudio()
    const url = `/audio/L${leccionId}/L${leccionId}-${numero}.mp3`
    const audio = new Audio(url)
    audioRef.current = audio
    audio.play().then(() => setTocandoAudio(true)).catch(() => setTocandoAudio(false))
    audio.onended = () => setTocandoAudio(false)
  }

  useEffect(() => {
    getLeccion(leccionId)
      .then(setLeccion)
      .catch(() => setError(true))
  }, [leccionId])

  function avanzarPagina() {
    if (!leccion) return
    detenerAudio()
    if (paginaActual < leccion.contenido.paginas.length - 1) {
      setPaginaActual((p) => p + 1)
    } else {
      setFase("quiz")
    }
  }

  function seleccionarOpcion(idx: number) {
    if (quiz.mostrandoFeedback) return
    setQuiz((q) => ({ ...q, seleccion: idx }))
  }

  function confirmarRespuesta() {
    if (!leccion || quiz.seleccion === null) return
    const pregunta: PreguntaQuizCorto =
      leccion.contenido.quiz_corto.preguntas[quiz.indice]
    const esCorrecta = pregunta.opciones[quiz.seleccion].correcta
    setQuiz((q) => ({
      ...q,
      aciertos: esCorrecta ? q.aciertos + 1 : q.aciertos,
      mostrandoFeedback: true,
    }))
  }

  function siguientePregunta() {
    if (!leccion) return
    detenerAudio()
    const siguiente = quiz.indice + 1
    const totalPreguntas = leccion.contenido.quiz_corto.preguntas.length
    if (siguiente >= totalPreguntas) {
      const umbral = leccion.contenido.quiz_corto.resultado.umbral_aprobado
      const paso = quiz.aciertos >= umbral
      setAprobado(paso)
      setFase("resultado")
      if (paso) guardarProgreso()
    } else {
      setQuiz((q) => ({
        ...q,
        indice: siguiente,
        seleccion: null,
        mostrandoFeedback: false,
      }))
    }
  }

  function guardarProgreso() {
    completarLeccion(leccionId).catch(() => {})
    const key = `huap_mod${moduloId}_lecciones_completadas`
    const completadas: number[] = JSON.parse(localStorage.getItem(key) ?? "[]")
    if (!completadas.includes(leccionId)) {
      completadas.push(leccionId)
      localStorage.setItem(key, JSON.stringify(completadas))
    }
  }

  function reiniciarLeccion() {
    setPaginaActual(0)
    setFase("paginas")
    setQuiz({ indice: 0, seleccion: null, mostrandoFeedback: false, aciertos: 0 })
  }

  // ── Carga / error ──────────────────────────────────────────────────────────

  if (error) {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main className="flex-1 flex items-center justify-center px-5">
          <p style={{ color: "var(--huap-rojo)", fontSize: "18px", textAlign: "center" }}>
            No se pudo cargar la lección. Verifica que el servidor esté activo.
          </p>
        </main>
      </div>
    )
  }

  if (!leccion) {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <p style={{ color: "#888", fontSize: "18px" }}>Cargando lección...</p>
        </main>
      </div>
    )
  }

  // ── FASE: PÁGINAS ──────────────────────────────────────────────────────────

  if (fase === "paginas") {
    const pagina = leccion.contenido.paginas[paginaActual]
    const totalPaginas = leccion.contenido.paginas.length

    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main
          className="flex-1 flex flex-col px-5 py-6 pb-28 w-full mx-auto"
          style={{ maxWidth: "680px" }}
        >
          {/* Volver */}
          <button
            onClick={() => router.push(`/modulos/${moduloId}`)}
            style={{
              alignSelf: "flex-start",
              padding: "12px 20px",
              borderRadius: "12px",
              border: "none",
              backgroundColor: "var(--huap-azul)",
              color: "white",
              fontSize: "17px",
              fontWeight: 600,
              cursor: "pointer",
              marginBottom: "16px",
            }}
          >
            ← Volver
          </button>

          {/* Progreso y título */}
          <div style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
              <span style={{ fontSize: "15px", color: "#666" }}>{leccion.titulo}</span>
              <span style={{ fontSize: "15px", color: "#666" }}>
                {paginaActual + 1} / {totalPaginas}
              </span>
            </div>
            <div
              style={{ backgroundColor: "#E0E0E0", borderRadius: "4px", height: "8px", overflow: "hidden" }}
            >
              <div
                style={{
                  backgroundColor: "var(--huap-azul)",
                  height: "8px",
                  borderRadius: "4px",
                  width: `${((paginaActual + 1) / totalPaginas) * 100}%`,
                  transition: "width 0.3s ease",
                }}
              />
            </div>
          </div>

          {/* Tarjeta de contenido */}
          <div
            style={{
              backgroundColor: "white",
              borderRadius: "16px",
              padding: "28px",
              flex: 1,
              minHeight: 0,
              marginBottom: "20px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
              overflowY: "auto",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "16px" }}>
              <h2 style={{ color: "var(--huap-azul)", flex: 1, marginRight: "12px" }}>
                {pagina.titulo}
              </h2>
              <button
                onClick={() => toggleAudio(paginaActual + 1)}
                style={{
                  flexShrink: 0,
                  padding: "8px 14px",
                  borderRadius: "10px",
                  border: `2px solid ${tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)"}`,
                  backgroundColor: tocandoAudio ? "#FFEBEE" : "#E3F2FD",
                  color: tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)",
                  fontSize: "15px",
                  fontWeight: 600,
                  cursor: "pointer",
                  whiteSpace: "nowrap",
                }}
              >
                {tocandoAudio ? "⏹ Detener" : "🔊 Escuchar"}
              </button>
            </div>
            <p style={{ color: "#333", fontSize: "18px", lineHeight: 1.7 }}>
              {pagina.texto}
            </p>
            {pagina.apoyo_visual && (
              IMAGENES_APOYO[pagina.apoyo_visual] ? (
                <div style={{ marginTop: "20px", display: "flex", justifyContent: "center" }}>
                  <Image
                    src={IMAGENES_APOYO[pagina.apoyo_visual]}
                    alt="Ilustración de la lección"
                    width={340}
                    height={340}
                    style={{ objectFit: "contain", maxWidth: "100%", maxHeight: "min(55vh, 420px)" }}
                  />
                </div>
              ) : (
                <p
                  style={{
                    marginTop: "20px",
                    padding: "12px 16px",
                    backgroundColor: "var(--huap-gris-suave)",
                    borderRadius: "8px",
                    color: "#555",
                    fontSize: "15px",
                    fontStyle: "italic",
                    lineHeight: 1.5,
                  }}
                >
                  {pagina.apoyo_visual}
                </p>
              )
            )}
          </div>

          {/* Botones de navegación */}
          <div style={{ display: "flex", gap: "12px" }}>
            {paginaActual > 0 && (
              <button
                onClick={() => setPaginaActual((p) => p - 1)}
                style={{
                  flex: 1,
                  padding: "16px",
                  borderRadius: "12px",
                  border: "2px solid var(--huap-azul)",
                  backgroundColor: "white",
                  color: "var(--huap-azul)",
                  fontSize: "18px",
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                ← Anterior
              </button>
            )}
            <button
              onClick={avanzarPagina}
              style={{
                flex: 2,
                padding: "16px",
                borderRadius: "12px",
                border: "none",
                backgroundColor: "var(--huap-azul)",
                color: "white",
                fontSize: "18px",
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
              {paginaActual < totalPaginas - 1 ? "Siguiente →" : "Ir al quiz →"}
            </button>
          </div>
        </main>
      </div>
    )
  }

  // ── FASE: QUIZ ─────────────────────────────────────────────────────────────

  if (fase === "quiz") {
    const preguntas = leccion.contenido.quiz_corto.preguntas
    const preguntaActual: PreguntaQuizCorto = preguntas[quiz.indice]
    const esCorrecta = quiz.seleccion !== null && preguntaActual.opciones[quiz.seleccion].correcta

    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main
          className="flex-1 flex flex-col px-5 py-6 pb-28 w-full mx-auto"
          style={{ maxWidth: "680px" }}
        >
          {/* Volver */}
          <button
            onClick={() => router.push(`/modulos/${moduloId}`)}
            style={{
              alignSelf: "flex-start",
              padding: "12px 20px",
              borderRadius: "12px",
              border: "none",
              backgroundColor: "var(--huap-azul)",
              color: "white",
              fontSize: "17px",
              fontWeight: 600,
              cursor: "pointer",
              marginBottom: "16px",
            }}
          >
            ← Volver
          </button>

          {/* Progreso del quiz */}
          <div style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
              <span style={{ fontSize: "15px", color: "#666" }}>Quiz rápido</span>
              <span style={{ fontSize: "15px", color: "#666" }}>
                {quiz.indice + 1} / {preguntas.length}
              </span>
            </div>
            <div
              style={{ backgroundColor: "#E0E0E0", borderRadius: "4px", height: "8px", overflow: "hidden" }}
            >
              <div
                style={{
                  backgroundColor: "var(--huap-verde)",
                  height: "8px",
                  borderRadius: "4px",
                  width: `${((quiz.indice + 1) / preguntas.length) * 100}%`,
                  transition: "width 0.3s ease",
                }}
              />
            </div>
          </div>

          {/* Tarjeta de pregunta */}
          <div
            style={{
              backgroundColor: "white",
              borderRadius: "16px",
              padding: "28px",
              flex: 1,
              marginBottom: "20px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "24px" }}>
              <h2 style={{ color: "#333", fontSize: "20px", lineHeight: 1.5, flex: 1, marginRight: "12px" }}>
                {preguntaActual.pregunta}
              </h2>
              <button
                onClick={() => toggleAudio(leccion.contenido.paginas.length + quiz.indice + 1)}
                style={{
                  flexShrink: 0,
                  padding: "8px 14px",
                  borderRadius: "10px",
                  border: `2px solid ${tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)"}`,
                  backgroundColor: tocandoAudio ? "#FFEBEE" : "#E3F2FD",
                  color: tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)",
                  fontSize: "15px",
                  fontWeight: 600,
                  cursor: "pointer",
                  whiteSpace: "nowrap",
                }}
              >
                {tocandoAudio ? "⏹ Detener" : "🔊 Escuchar"}
              </button>
            </div>

            <div className="flex flex-col gap-3">
              {preguntaActual.opciones.map((opcion, idx) => {
                let bgColor = "white"
                let borderColor = "#E0E0E0"
                let textColor = "#333"

                if (!quiz.mostrandoFeedback && quiz.seleccion === idx) {
                  bgColor = "#E3F2FD"
                  borderColor = "var(--huap-azul)"
                }
                if (quiz.mostrandoFeedback) {
                  if (opcion.correcta) {
                    bgColor = "#E8F5E9"
                    borderColor = "var(--huap-verde)"
                    textColor = "#1B5E20"
                  } else if (quiz.seleccion === idx) {
                    bgColor = "#FFEBEE"
                    borderColor = "var(--huap-rojo)"
                    textColor = "#7F0000"
                  }
                }

                return (
                  <button
                    key={idx}
                    onClick={() => seleccionarOpcion(idx)}
                    disabled={quiz.mostrandoFeedback}
                    style={{
                      padding: "16px",
                      borderRadius: "10px",
                      border: `2px solid ${borderColor}`,
                      backgroundColor: bgColor,
                      fontSize: "17px",
                      textAlign: "left",
                      cursor: quiz.mostrandoFeedback ? "default" : "pointer",
                      color: textColor,
                      lineHeight: 1.4,
                    }}
                  >
                    {opcion.texto}
                  </button>
                )
              })}
            </div>

            {quiz.mostrandoFeedback && (
              <div
                style={{
                  marginTop: "20px",
                  padding: "14px 16px",
                  backgroundColor: esCorrecta ? "#E8F5E9" : "#FFEBEE",
                  border: `1.5px solid ${esCorrecta ? "var(--huap-verde)" : "var(--huap-rojo)"}`,
                  borderRadius: "8px",
                }}
              >
                <p style={{
                  color: esCorrecta ? "#1B5E20" : "#7F0000",
                  fontSize: "15px",
                  fontWeight: 700,
                  marginBottom: "6px",
                }}>
                  {esCorrecta ? "✓ ¡Muy bien!" : "✗ Incorrecto"}
                </p>
                <p style={{ color: esCorrecta ? "#2E7D32" : "#B71C1C", fontSize: "16px", lineHeight: 1.5 }}>
                  {preguntaActual.feedback}
                </p>
              </div>
            )}
          </div>

          {/* Botón de acción */}
          {!quiz.mostrandoFeedback ? (
            <button
              onClick={confirmarRespuesta}
              disabled={quiz.seleccion === null}
              style={{
                padding: "16px",
                borderRadius: "12px",
                border: "none",
                backgroundColor: quiz.seleccion !== null ? "var(--huap-azul)" : "#D0D0D0",
                color: quiz.seleccion !== null ? "white" : "#999",
                fontSize: "18px",
                fontWeight: 600,
                cursor: quiz.seleccion !== null ? "pointer" : "not-allowed",
                width: "100%",
              }}
            >
              Confirmar respuesta
            </button>
          ) : (
            <button
              onClick={siguientePregunta}
              style={{
                padding: "16px",
                borderRadius: "12px",
                border: "none",
                backgroundColor: "var(--huap-azul)",
                color: "white",
                fontSize: "18px",
                fontWeight: 600,
                cursor: "pointer",
                width: "100%",
              }}
            >
              {quiz.indice + 1 < preguntas.length
                ? "Siguiente pregunta →"
                : "Ver resultado →"}
            </button>
          )}
        </main>
      </div>
    )
  }

  // ── FASE: RESULTADO ────────────────────────────────────────────────────────

  const resultado = leccion.contenido.quiz_corto.resultado

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />
      <main
        className="flex-1 flex flex-col items-center justify-center px-5 py-8 pb-28 w-full mx-auto"
        style={{ maxWidth: "680px" }}
      >
        <div
          style={{
            backgroundColor: "white",
            borderRadius: "16px",
            padding: "36px 28px",
            textAlign: "center",
            boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
            width: "100%",
          }}
        >
          <div style={{ marginBottom: "16px", display: "flex", justifyContent: "center" }}>
            {aprobado
              ? <Trophy size={72} color="var(--huap-verde)" strokeWidth={1.5} />
              : <RefreshCw size={72} color="var(--huap-azul)" strokeWidth={1.5} />
            }
          </div>
          <h2
            style={{
              color: aprobado ? "var(--huap-verde)" : "var(--huap-azul)",
              fontSize: "24px",
              marginBottom: "12px",
            }}
          >
            {aprobado ? resultado.titulo_aprobado : resultado.titulo_fallido}
          </h2>
          <p style={{ color: "#555", fontSize: "18px", lineHeight: 1.6, marginBottom: "12px" }}>
            {aprobado ? resultado.mensaje_aprobado : resultado.mensaje_fallido}
          </p>
          <p style={{ color: "#aaa", fontSize: "15px", marginBottom: "32px" }}>
            {quiz.aciertos} de {leccion.contenido.quiz_corto.preguntas.length} respuestas correctas
          </p>

          <div className="flex flex-col gap-3">
            {!aprobado && (
              <button
                onClick={reiniciarLeccion}
                style={{
                  padding: "16px",
                  borderRadius: "12px",
                  border: "2px solid var(--huap-azul)",
                  backgroundColor: "white",
                  color: "var(--huap-azul)",
                  fontSize: "17px",
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                Repasar la lección
              </button>
            )}
            <button
              onClick={() => router.push(`/modulos/${moduloId}`)}
              style={{
                padding: "16px",
                borderRadius: "12px",
                border: "none",
                backgroundColor: "var(--huap-azul)",
                color: "white",
                fontSize: "17px",
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
              Volver al módulo
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}
