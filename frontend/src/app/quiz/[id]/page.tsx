"use client"

import { useEffect, useRef, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { useSession } from "next-auth/react"
import { Trophy, RefreshCw, CheckCircle, XCircle } from "lucide-react"
import Header from "@/components/layout/Header"
import {
  getModuloDetalle,
  submitQuizFinal,
  type ModuloDetalle,
  type PreguntaQuizFinal,
  type RespuestaItem,
  type ResultadoQuiz,
  type FeedbackPregunta,
  type InsigniaOtorgada,
} from "@/lib/api"

type Fase = "quiz" | "insignia" | "resultado"

function guardarFlags(moduloOrden: number) {
  if (moduloOrden === 1) {
    localStorage.setItem("huap_mod1_completado", "true")
    localStorage.setItem("huap_quiz1_aprobado", "true")
  } else if (moduloOrden === 2) {
    localStorage.setItem("huap_mod2_completado", "true")
  }
}

export default function QuizFinalPage() {
  const params = useParams()
  const router = useRouter()
  const { data: session } = useSession()
  const quizId = Number(params.id as string)

  const [modulo, setModulo] = useState<ModuloDetalle | null>(null)
  const [error, setError] = useState(() => !Number(sessionStorage.getItem("huap_quiz_modulo_id") ?? "0"))
  const [enviando, setEnviando] = useState(false)
  const [fase, setFase] = useState<Fase>("quiz")

  // Estado del quiz: índice de pregunta actual y selecciones acumuladas
  const [indice, setIndice] = useState(0)
  const [selecciones, setSelecciones] = useState<Record<number, number>>({}) // preguntaId → opcionId
  const [seleccionActual, setSeleccionActual] = useState<number | null>(null)

  // Resultado del backend
  const [resultado, setResultado] = useState<ResultadoQuiz | null>(null)
  const [feedbackMap, setFeedbackMap] = useState<Record<number, FeedbackPregunta>>({})
  const [insignia, setInsignia] = useState<InsigniaOtorgada | null>(null)

  // Audio
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const [tocandoAudio, setTocandoAudio] = useState(false)

  const siguienteRef = useRef<HTMLButtonElement>(null)
  const progresoRef = useRef<HTMLDivElement>(null)
  const preguntaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const moduloIdGuardado = Number(sessionStorage.getItem("huap_quiz_modulo_id") ?? "0")
    if (!moduloIdGuardado) return
    getModuloDetalle(moduloIdGuardado)
      .then(setModulo)
      .catch(() => setError(true))
  }, [])

  useEffect(() => {
    return () => {
      if (audioRef.current) audioRef.current.pause()
    }
  }, [])

  useEffect(() => {
    const t = setTimeout(() => {
      siguienteRef.current?.scrollIntoView({ behavior: "smooth", block: "end" })
    }, 150)
    return () => clearTimeout(t)
  }, [])

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
    const audio = new Audio(`/audio/quiz-final-${modulo?.orden}/Q${numero}.mp3`)
    audioRef.current = audio
    audio.play().then(() => setTocandoAudio(true)).catch(() => setTocandoAudio(false))
    audio.onended = () => setTocandoAudio(false)
  }

  function seleccionar(opcionId: number) {
    setSeleccionActual(opcionId)
    setTimeout(() => {
      siguienteRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" })
    }, 50)
  }

  function confirmarYSiguiente() {
    if (!modulo || seleccionActual === null) return
    const pregunta = preguntas[indice]
    const nuevas = { ...selecciones, [pregunta.id]: seleccionActual }
    setSelecciones(nuevas)
    setSeleccionActual(null)
    detenerAudio()

    if (indice + 1 < preguntas.length) {
      setTimeout(() => {
        setIndice((i) => i + 1)
        setTimeout(() => siguienteRef.current?.scrollIntoView({ behavior: "smooth", block: "end" }), 80)
      }, 50)
    } else {
      // Última pregunta: enviar al backend
      enviarRespuestas(nuevas)
    }
  }

  async function enviarRespuestas(sels: Record<number, number>) {
    if (!modulo) return
    setEnviando(true)
    const respuestas: RespuestaItem[] = Object.entries(sels).map(([pregId, opId]) => ({
      pregunta_id: Number(pregId),
      opcion_id: Number(opId),
    }))
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const token = (session as any)?.accessToken as string | undefined
      const res = await submitQuizFinal(quizId, respuestas, token)
      setResultado(res)
      const mapa: Record<number, FeedbackPregunta> = {}
      for (const fb of res.feedbacks) mapa[fb.pregunta_id] = fb
      setFeedbackMap(mapa)
      if (res.aprobado) {
        guardarFlags(modulo.orden)
        setInsignia(res.insignia_otorgada)
        setFase("insignia")
      } else {
        setFase("resultado")
      }
    } catch {
      setError(true)
    } finally {
      setEnviando(false)
    }
  }

  // ── Pantallas de carga / error ──────────────────────────────────────────────

  if (error) {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main className="flex-1 flex flex-col items-center justify-center px-5 gap-6">
          <p style={{ color: "var(--huap-rojo)", fontSize: "18px", textAlign: "center" }}>
            No se pudo cargar el quiz. Vuelve al módulo e inténtalo de nuevo.
          </p>
          <button
            onClick={() => router.back()}
            style={{
              padding: "14px 28px",
              borderRadius: "12px",
              border: "none",
              backgroundColor: "var(--huap-azul)",
              color: "white",
              fontSize: "17px",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            ← Volver
          </button>
        </main>
      </div>
    )
  }

  if (!modulo || enviando) {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <p style={{ color: "#888", fontSize: "18px" }}>
            {enviando ? "Corrigiendo respuestas…" : "Cargando quiz…"}
          </p>
        </main>
      </div>
    )
  }

  if (!modulo.quiz_final) {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main className="flex-1 flex items-center justify-center px-5">
          <p style={{ color: "#888", fontSize: "18px", textAlign: "center" }}>
            Este módulo no tiene quiz final.
          </p>
        </main>
      </div>
    )
  }

  const preguntas: PreguntaQuizFinal[] = modulo.quiz_final.preguntas
  const preguntaActual = preguntas[indice]

  // ── FASE: QUIZ ─────────────────────────────────────────────────────────────

  if (fase === "quiz") {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main
          className="flex-1 flex flex-col px-5 py-6 pb-28 w-full mx-auto"
          style={{ maxWidth: "680px" }}
        >
          {/* Botón volver */}
          <button
            onClick={() => router.back()}
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

          {/* Encabezado */}
          <div style={{ marginBottom: "20px" }}>
            <h1 style={{ color: "var(--huap-azul)", fontSize: "22px", fontWeight: 700, marginBottom: "6px" }}>
              Quiz Final — Módulo {modulo.orden}
            </h1>
            <p style={{ color: "#666", fontSize: "15px" }}>{modulo.nombre}</p>

            {/* Barra de progreso */}
            <div ref={progresoRef} style={{ marginTop: "14px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                <span style={{ fontSize: "14px", color: "#666" }}>Pregunta {indice + 1} de {preguntas.length}</span>
              </div>
              <div style={{ backgroundColor: "#E0E0E0", borderRadius: "4px", height: "8px", overflow: "hidden" }}>
                <div
                  style={{
                    backgroundColor: "var(--huap-azul)",
                    height: "8px",
                    borderRadius: "4px",
                    width: `${((indice + 1) / preguntas.length) * 100}%`,
                    transition: "width 0.3s ease",
                  }}
                />
              </div>
            </div>
          </div>

          {/* Tarjeta de pregunta */}
          <div
            ref={preguntaRef}
            style={{
              backgroundColor: "white",
              borderRadius: "16px",
              padding: "28px",
              flex: 1,
              marginBottom: "20px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
              scrollMarginTop: "12px",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "12px", marginBottom: "24px" }}>
              <h2 style={{ color: "#111827", fontSize: "18px", fontWeight: 500, lineHeight: 1.5, margin: 0, flex: 1 }}>
                {preguntaActual.enunciado}
              </h2>
              <button
                onClick={() => toggleAudio(indice + 1)}
                className="flex items-center justify-center gap-1 p-[6px] md:py-[2px] md:pl-[8px] md:pr-[10px]"
                style={{
                  flexShrink: 0,
                  alignSelf: "flex-start",
                  marginTop: "-20px",
                  marginRight: "-20px",
                  borderRadius: "999px",
                  border: `1px solid ${tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)"}`,
                  backgroundColor: "white",
                  color: tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)",
                  fontSize: "14px",
                  fontWeight: 500,
                  cursor: "pointer",
                  whiteSpace: "nowrap",
                }}
              >
                <span style={{ fontSize: "22px", lineHeight: 1, display: "block" }}>{tocandoAudio ? "⏹" : "🔊"}</span>
                <span className="hidden md:inline">{tocandoAudio ? "Detener" : "Escuchar"}</span>
              </button>
            </div>

            <div className="flex flex-col gap-3">
              {preguntaActual.opciones.map((opcion) => {
                const seleccionada = seleccionActual === opcion.id
                return (
                  <button
                    key={opcion.id}
                    onClick={() => seleccionar(opcion.id)}
                    style={{
                      padding: "16px",
                      borderRadius: "10px",
                      border: `2px solid ${seleccionada ? "var(--huap-azul)" : "#E0E0E0"}`,
                      backgroundColor: seleccionada ? "#E3F2FD" : "white",
                      fontSize: "17px",
                      textAlign: "left",
                      cursor: "pointer",
                      color: seleccionada ? "var(--huap-azul)" : "#333",
                      lineHeight: 1.4,
                      fontWeight: seleccionada ? 600 : 400,
                    }}
                  >
                    {opcion.texto}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Botón siguiente */}
          <button
            ref={siguienteRef}
            onClick={confirmarYSiguiente}
            disabled={seleccionActual === null}
            style={{
              padding: "16px",
              borderRadius: "12px",
              border: "none",
              backgroundColor: seleccionActual !== null ? "var(--huap-azul)" : "#D0D0D0",
              color: seleccionActual !== null ? "white" : "#999",
              fontSize: "18px",
              fontWeight: 600,
              cursor: seleccionActual !== null ? "pointer" : "not-allowed",
              width: "100%",
              scrollMarginBottom: "120px",
            }}
          >
            {indice + 1 < preguntas.length ? "Siguiente pregunta →" : "Ver resultado →"}
          </button>
        </main>
      </div>
    )
  }

  // ── FASE: INSIGNIA ─────────────────────────────────────────────────────────

  if (fase === "insignia") {
    const descripcionPorModulo: Record<number, string> = {
      1: "ahora sabes qué es la inteligencia artificial.",
      2: "sabes cómo usar la IA de manera segura.",
    }
    const desc = descripcionPorModulo[modulo.orden] ?? "completaste el módulo."
    const siguienteLabel = modulo.orden < 3
      ? `Continuar al Módulo ${modulo.orden + 1} →`
      : "Ver mis módulos →"

    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main
          className="flex-1 flex flex-col items-center justify-center px-5 py-8 pb-28 w-full mx-auto"
          style={{ maxWidth: "480px" }}
        >
          {/* Medalla */}
          <div style={{
            width: "150px",
            height: "150px",
            borderRadius: "50%",
            background: "radial-gradient(circle at 35% 35%, #FFD95C, #F5A623)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "68px",
            marginBottom: "32px",
            border: "4px dashed #E8A000",
            boxShadow: "0 10px 40px rgba(245, 166, 35, 0.35)",
            flexShrink: 0,
          }}>
            {insignia?.icono_url ?? "🏅"}
          </div>

          {/* Título */}
          <h2 style={{
            color: "var(--huap-verde)",
            fontSize: "2rem",
            fontWeight: 800,
            textAlign: "center",
            marginBottom: "14px",
            lineHeight: 1.2,
          }}>
            ¡Felicitaciones!
          </h2>

          {/* Descripción */}
          <p style={{
            color: "#444",
            fontSize: "1.05rem",
            textAlign: "center",
            lineHeight: 1.65,
            marginBottom: "24px",
          }}>
            Completaste el <strong>Módulo {modulo.orden}</strong> y {desc}
          </p>

          {/* Chip de insignia — estilo ámbar como en el prototipo */}
          {insignia && (
            <div style={{
              border: "2px solid #E8A000",
              borderRadius: "12px",
              padding: "12px 28px",
              marginBottom: "36px",
              backgroundColor: "#FFFBF0",
            }}>
              <p style={{ color: "#B85C00", fontSize: "1rem", fontWeight: 700, textAlign: "center", margin: 0 }}>
                Insignia: {insignia.nombre}
              </p>
            </div>
          )}

          {/* Botones */}
          <div className="flex flex-col gap-3" style={{ width: "100%" }}>
            <button
              onClick={() => router.push("/modulos")}
              style={{
                padding: "18px",
                borderRadius: "14px",
                border: "none",
                backgroundColor: "var(--huap-verde)",
                color: "white",
                fontSize: "1.1rem",
                fontWeight: 700,
                cursor: "pointer",
                width: "100%",
              }}
            >
              {siguienteLabel}
            </button>
            <button
              onClick={() => setFase("resultado")}
              style={{
                padding: "16px",
                borderRadius: "14px",
                border: "2px solid #D0D0D0",
                backgroundColor: "white",
                color: "#555",
                fontSize: "0.95rem",
                fontWeight: 600,
                cursor: "pointer",
                width: "100%",
              }}
            >
              Ver revisión de respuestas
            </button>
          </div>
        </main>
      </div>
    )
  }

  // ── FASE: RESULTADO ────────────────────────────────────────────────────────

  if (fase === "resultado" && resultado) {
    const aprobado = resultado.aprobado

    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main
          className="flex-1 flex flex-col px-5 py-8 pb-28 w-full mx-auto"
          style={{ maxWidth: "680px" }}
        >
          {/* Tarjeta de resultado */}
          <div
            style={{
              backgroundColor: "white",
              borderRadius: "16px",
              padding: "36px 28px",
              textAlign: "center",
              boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
              marginBottom: "24px",
            }}
          >
            <div style={{ marginBottom: "16px", display: "flex", justifyContent: "center" }}>
              {aprobado
                ? <Trophy size={72} color="var(--huap-verde)" strokeWidth={1.5} />
                : <RefreshCw size={72} color="var(--huap-azul)" strokeWidth={1.5} />
              }
            </div>
            <h2 style={{ color: aprobado ? "var(--huap-verde)" : "var(--huap-azul)", fontSize: "26px", marginBottom: "12px", fontWeight: 700 }}>
              {aprobado ? "¡Módulo completado!" : "¡Casi lo logras!"}
            </h2>
            <p style={{ color: "#555", fontSize: "19px", lineHeight: 1.6, marginBottom: "10px" }}>
              {aprobado
                ? `Respondiste ${resultado.puntaje} de ${preguntas.length} correctamente. ¡Muy bien hecho!`
                : `Respondiste ${resultado.puntaje} de ${preguntas.length} correctamente. Necesitas ${resultado.minimo_aciertos} para aprobar.`
              }
            </p>
            {aprobado && modulo.orden < 3 && (
              <p style={{ color: "var(--huap-verde)", fontSize: "17px", fontWeight: 600 }}>
                ✓ Módulo {modulo.orden + 1} desbloqueado
              </p>
            )}
          </div>

          {/* Revisión de respuestas */}
          <div style={{ marginBottom: "24px" }}>
            <h3 style={{ color: "var(--huap-azul)", fontSize: "18px", fontWeight: 700, marginBottom: "16px" }}>
              Revisión de respuestas
            </h3>
            <div className="flex flex-col gap-4">
              {preguntas.map((pregunta, i) => {
                const fb = feedbackMap[pregunta.id]
                if (!fb) return null
                const opcionSeleccionada = pregunta.opciones.find((o) => o.id === fb.opcion_seleccionada_id)
                const opcionCorrecta = pregunta.opciones.find((o) => o.id === fb.opcion_correcta_id)
                return (
                  <div
                    key={pregunta.id}
                    style={{
                      backgroundColor: "white",
                      borderRadius: "12px",
                      padding: "20px",
                      boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
                      borderLeft: `4px solid ${fb.es_correcta ? "var(--huap-verde)" : "var(--huap-rojo)"}`,
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "flex-start", gap: "10px", marginBottom: "10px" }}>
                      {fb.es_correcta
                        ? <CheckCircle size={22} color="var(--huap-verde)" style={{ flexShrink: 0, marginTop: "2px" }} />
                        : <XCircle size={22} color="var(--huap-rojo)" style={{ flexShrink: 0, marginTop: "2px" }} />
                      }
                      <p style={{ fontSize: "17px", color: "#333", fontWeight: 600, lineHeight: 1.4 }}>
                        {i + 1}. {pregunta.enunciado}
                      </p>
                    </div>

                    {!fb.es_correcta && (
                      <div style={{ marginLeft: "32px", marginBottom: "8px" }}>
                        <p style={{ fontSize: "14px", color: "var(--huap-rojo)", marginBottom: "2px" }}>
                          Tu respuesta: {opcionSeleccionada?.texto ?? "—"}
                        </p>
                        <p style={{ fontSize: "14px", color: "var(--huap-verde)", marginBottom: "0" }}>
                          Correcta: {opcionCorrecta?.texto ?? "—"}
                        </p>
                      </div>
                    )}

                    <div
                      style={{
                        marginLeft: "32px",
                        marginTop: "8px",
                        padding: "10px 14px",
                        backgroundColor: fb.es_correcta ? "#E8F5E9" : "#FFF3E0",
                        borderRadius: "8px",
                      }}
                    >
                      <p style={{ fontSize: "15px", color: "#444", lineHeight: 1.5 }}>
                        {fb.feedback}
                      </p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Botones de acción */}
          <div className="flex flex-col gap-3">
            {!aprobado && (
              <button
                onClick={() => {
                  setFase("quiz")
                  setIndice(0)
                  setSelecciones({})
                  setSeleccionActual(null)
                  setResultado(null)
                }}
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
                Reintentar quiz
              </button>
            )}
            <button
              onClick={() => router.push("/modulos")}
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
              {aprobado ? "Ver mis módulos →" : "Volver a módulos"}
            </button>
          </div>
        </main>
      </div>
    )
  }

  return null
}
