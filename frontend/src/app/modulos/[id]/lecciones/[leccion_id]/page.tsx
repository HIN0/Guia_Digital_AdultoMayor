"use client"

import { useEffect, useRef, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import Image from "next/image"
import Header from "@/components/layout/Header"
import { Trophy, RefreshCw } from "lucide-react"
import { getLeccion, getModuloDetalle, completarLeccion, type LeccionDetalle, type PreguntaQuizCorto } from "@/lib/api"

const IMAGENES_APOYO: Record<string, string> = {
  // L1 — Bienvenida y navegación
  'Ilustración cálida de una persona mayor sonriendo frente a un teléfono. Botón verde grande "Comenzar".': "/lecciones/modulo1/L1-1.svg",
  "Flechas animadas señalando: ① la flecha ← para Volver, ② el menú principal (Inicio), ③ el botón de Chat, ④ el botón de progreso, ⑤ el ajuste de tamaño de letra (selector de tamaño de letra).": "/lecciones/modulo1/L1-2.svg",
  "Demostración del selector Pequeño / Mediano / Grande cambiando el tamaño del texto en vivo.": "/lecciones/modulo1/L1-3.svg",
  "Guía paso a paso con refuerzo positivo después de cada toque.": "/lecciones/modulo1/L1-4.svg",
  "Mensaje de felicitación con marca de avance del módulo.": "/lecciones/modulo1/L1-5.svg",
  // L2 — ¿Qué es la IA?
  "Ilustración simple: un computador rodeado de ejemplos con una flecha que sale hacia una respuesta.": "/lecciones/modulo1/L2-1.svg",
  "Cuatro tarjetas: 📷 reconocer cara, ✍️ corregir texto, 🗺️ sugerir ruta, 🔊 asistente de voz.": "/lecciones/modulo1/L2-2.svg",
  "Analogía visual del aprendizaje por ejemplos.": "/lecciones/modulo1/L2-3.svg",
  "Comparación: calculadora 🧮 = herramienta útil / IA 🤖 = herramienta útil.": "/lecciones/modulo1/L2-4.svg",
  "Ilustración de un chatbot conversando con un usuario.": "/lecciones/modulo1/L2-5.svg",
  "Resumen con tres viñetas y marca de avance.": "/lecciones/modulo1/L2-6.svg",
  // L3 — La IA en salud
  "Ícono de corazón con un signo de ayuda.": "/lecciones/modulo1/L3-1.svg",
  "Tres tarjetas: 📖 explicar palabras, ℹ️ información general, ⏰ recordatorios.": "/lecciones/modulo1/L3-2.svg",
  "Viñeta ilustrada de don Luis consultando la app en casa.": "/lecciones/modulo1/L3-3.svg",
  'Lista con íconos rojos de "no" frente a cada límite.': "/lecciones/modulo1/L3-4.svg",
  // L5 — Privacidad y datos
  "Ilustración de una plaza con mucha gente escuchando, frente a una consulta médica cerrada.": "/lecciones/modulo1/L5-1.svg",
  "Lista verde: síntomas en general, dudas sobre una enfermedad, preguntas de orientación.": "/lecciones/modulo1/L5-2.svg",
  "Lista roja: RUT, dirección, Fonasa, fotos con nombre, tarjeta bancaria, contraseñas.": "/lecciones/modulo1/L5-3.svg",
  "Viñeta del caso de María recibiendo publicidad no deseada.": "/lecciones/modulo1/L5-4.svg",
  "Mensaje de cierre destacado con candado 🔒.": "/lecciones/modulo1/L5-5.svg",
  // L6 — Reconocer engaños
  "Ilustración de un mensaje con disfraz de hospital y una alerta.": "/lecciones/modulo1/L6-1.svg",
  "Tres tarjetas de alerta: 🪄 cura milagrosa, ⏱️ te apura, 💳 te pide pagar.": "/lecciones/modulo1/L6-2.svg",
  "Pasos ilustrados: buscar en Google, llamar al número oficial, no tocar links de WhatsApp.": "/lecciones/modulo1/L6-3.svg",
  "Capturas comparadas: mensaje falso vs. sitio oficial gob.cl.": "/lecciones/modulo1/L6-4.svg",
  "Resumen con las tres señales y la acción de verificar.": "/lecciones/modulo1/L6-5.svg",
  // L4 — Riesgos y limitaciones
  "Ilustración de un robot hablando con tono seguro mientras un signo de interrogación flota encima.": "/lecciones/modulo1/L4-1.svg",
  "Ejemplo de una respuesta inventada marcada con una lupa y la palabra \"alucinación\".": "/lecciones/modulo1/L4-2.svg",
  "Calendario con una fecha de corte y un reloj indicando \"puede estar atrasada\".": "/lecciones/modulo1/L4-3.svg",
  "Comparación: una multitud (lo general) frente a una sola persona destacada (tu caso).": "/lecciones/modulo1/L4-4.svg",
  "Viñeta del caso con mensaje: \"confirmar la salvó de un error\".": "/lecciones/modulo1/L4-5.svg",
  "Resumen con tres riesgos y la regla de oro destacada.": "/lecciones/modulo1/L4-6.svg",
  // L1 — Hacer mejores preguntas (Módulo 2, lección 2.1)
  "Ilustración: una pregunta clara entra y sale una respuesta clara; una pregunta confusa sale confusa.": "/lecciones/modulo2/L1-1.svg",
  "Comparación: \"me siento mal\" (vago) → \"dolor de cabeza en las mañanas\" (concreto).": "/lecciones/modulo2/L1-2.svg",
  "Ejemplo de pedir \"explícamelo simple\" y la respuesta simplificada.": "/lecciones/modulo2/L1-3.svg",
  "Recordatorio con candado: pregunta sí, datos personales no.": "/lecciones/modulo2/L1-4.svg",
  "Resumen con los tres trucos y marca de avance.": "/lecciones/modulo2/L1-5.svg",
  // L2 — Leer una respuesta (Módulo 2, lección 2.2)
  "Ilustración de una respuesta con \"señales\" resaltadas como pistas.": "/lecciones/modulo2/L2-1.svg",
  "Frase \"generalmente...\" resaltada en ámbar.": "/lecciones/modulo2/L2-2.svg",
  "Frase \"consulte a un médico\" resaltada en verde con un visto bueno.": "/lecciones/modulo2/L2-3.svg",
  "Frase \"podría ser A, B o C\" con un signo de interrogación.": "/lecciones/modulo2/L2-4.svg",
  "Resumen con las tres señales y marca de avance.": "/lecciones/modulo2/L2-5.svg",
  // L3 — Verificar la información (Módulo 2, lección 2.3)
  "Ilustración de una afirmación pasando por un \"filtro de verificación\".": "/lecciones/modulo2/L3-1.svg",
  "Dos columnas: confiables (médico, gob.cl, consultorio) vs. no confiables (redes, cadenas de WhatsApp).": "/lecciones/modulo2/L3-2.svg",
  "Balanza: IA en un lado, fuente confiable en el otro; gana el profesional.": "/lecciones/modulo2/L3-3.svg",
  "Viñeta del caso de Carlos confirmando con su médico.": "/lecciones/modulo2/L3-4.svg",
  "Resumen con la regla de las dos fuentes y marca de avance.": "/lecciones/modulo2/L3-5.svg",
  // L4 — Casos por patología (Módulo 2, lección 2.4)
  "Cinco tarjetas con las patologías base. Aviso visible: \"contenido educativo, no diagnóstico\".": "/lecciones/modulo2/L4-1.svg",
  "Ícono de tensiómetro. Pregunta útil vs. lo que es del médico.": "/lecciones/modulo2/L4-2.svg",
  "Ícono de gota/glucómetro. Pregunta útil vs. lo que es del médico.": "/lecciones/modulo2/L4-3.svg",
  "Ícono de articulación. Pregunta útil vs. lo que es del médico.": "/lecciones/modulo2/L4-4.svg",
  "Ícono de corazón/arteria. Pregunta útil vs. lo que es del médico.": "/lecciones/modulo2/L4-5.svg",
  "Ícono de pierna. Pregunta útil vs. lo que es del médico.": "/lecciones/modulo2/L4-6.svg",
  "Resumen del patrón común SÍ/NO con marca de avance.": "/lecciones/modulo2/L4-7.svg",
  // L5 — Preparar tu consulta médica (Módulo 2, lección 2.5)
  "Ilustración de una persona mayor llegando confiada a su consulta con una lista en la mano.": "/lecciones/modulo2/L5-1.svg",
  "Lista de preguntas generada para llevar a la consulta.": "/lecciones/modulo2/L5-2.svg",
  "Ejemplo: \"insuficiencia venosa\" → explicación simple.": "/lecciones/modulo2/L5-3.svg",
  "Guía de tres preguntas: ¿cuándo empezó?, ¿qué siento?, ¿qué lo empeora?": "/lecciones/modulo2/L5-4.svg",
  "Demostración de la conversación y el paciente anotando las preguntas.": "/lecciones/modulo2/L5-5.svg",
  "Resumen con los tres usos y marca de avance.": "/lecciones/modulo2/L5-6.svg",
  // L6 — Cuándo NO usar la IA (Módulo 2, lección 2.6)
  "Encabezado en rojo de emergencia. Tono serio, sin alarmar.": "/lecciones/modulo2/L6-1.svg",
  "Caja de alerta roja con lista de síntomas (igual que en el prototipo).": "/lecciones/modulo2/L6-2.svg",
  "Tarjetas con números grandes (igual que en el prototipo).": "/lecciones/modulo2/L6-3.svg",
  "Tres situaciones para médico de cabecera con ícono de médico.": "/lecciones/modulo2/L6-4.svg",
  "Mensaje de cierre destacado (disclaimer del prototipo).": "/lecciones/modulo2/L6-5.svg",
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
  const [moduloOrden, setModuloOrden] = useState(0)
  const [tocandoAudio, setTocandoAudio] = useState(false)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const feedbackRef = useRef<HTMLDivElement>(null)

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
    if (!leccion || moduloOrden === 0) return
    detenerAudio()
    const url = `/audio/modulo${moduloOrden}/L${leccion.orden}/L${leccion.orden}-${numero}.mp3`
    const audio = new Audio(url)
    audioRef.current = audio
    audio.play().then(() => setTocandoAudio(true)).catch(() => setTocandoAudio(false))
    audio.onended = () => setTocandoAudio(false)
  }

  useEffect(() => {
    getLeccion(leccionId)
      .then(setLeccion)
      .catch(() => setError(true))
    getModuloDetalle(moduloId)
      .then(m => setModuloOrden(m.orden))
      .catch(() => {})
  }, [leccionId, moduloId])

  useEffect(() => {
    if (quiz.mostrandoFeedback && feedbackRef.current) {
      const t = setTimeout(() => {
        feedbackRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" })
      }, 80)
      return () => clearTimeout(t)
    }
  }, [quiz.mostrandoFeedback])

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

          {/* Progreso — pill style (ModuloCard) */}
          <div style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
              <span style={{ fontSize: "14px", color: "#6B7280" }}>{leccion.titulo}</span>
              <span style={{ fontSize: "14px", color: "#6B7280", fontWeight: 500 }}>
                {paginaActual + 1} / {totalPaginas}
              </span>
            </div>
            <div
              role="progressbar"
              aria-valuenow={paginaActual + 1}
              aria-valuemin={1}
              aria-valuemax={totalPaginas}
              style={{
                width: "100%",
                height: "5px",
                backgroundColor: "#E5E7EB",
                borderRadius: "999px",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${((paginaActual + 1) / totalPaginas) * 100}%`,
                  height: "100%",
                  backgroundColor: "var(--huap-azul)",
                  borderRadius: "999px",
                  transition: "width 0.6s ease",
                }}
              />
            </div>
          </div>

          {/* Tarjeta de contenido — ModuloCard: franja izquierda + border sutil */}
          <div
            style={{
              background: "#FFFFFF",
              borderRadius: "16px",
              border: "0.5px solid #E5E7EB",
              overflow: "hidden",
              flex: 1,
              minHeight: 0,
              marginBottom: "20px",
              display: "flex",
              flexDirection: "row",
            }}
          >
            {/* Franja izquierda azul */}
            <div
              aria-hidden="true"
              style={{ width: "6px", backgroundColor: "var(--huap-azul)", flexShrink: 0 }}
            />

            {/* Contenido */}
            <div
              style={{
                flex: 1,
                padding: "24px",
                display: "flex",
                flexDirection: "column",
                gap: "16px",
                overflowY: "auto",
              }}
            >
              {/* Título + botón audio */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "12px" }}>
                <h2 style={{ color: "#111827", fontSize: "18px", fontWeight: 500, lineHeight: 1.4, margin: 0, flex: 1 }}>
                  {pagina.titulo}
                </h2>
                <button
                  onClick={() => toggleAudio(paginaActual + 1)}
                  style={{
                    flexShrink: 0,
                    alignSelf: "flex-start",
                    marginTop: "-20px",
                    marginRight: "-20px",
                    padding: "2px 10px 2px 8px",
                    borderRadius: "999px",
                    border: `1px solid ${tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)"}`,
                    backgroundColor: "white",
                    color: tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)",
                    fontSize: "14px",
                    fontWeight: 500,
                    cursor: "pointer",
                    whiteSpace: "nowrap",
                    display: "flex",
                    alignItems: "center",
                    gap: "4px",
                  }}
                >
                  <span style={{ fontSize: "22px", lineHeight: 1 }}>🔊</span>
                  <span className="hidden md:inline">{tocandoAudio ? "Detener" : "Escuchar"}</span>
                </button>
              </div>

              {/* Texto */}
              {(() => {
                const texto = pagina.texto

                // Patrón patología: "Pregunta útil: "..." . [medio] Lo que NO puede: [resto]"
                const matchPatologia = texto.match(/^(.*?)Pregunta útil:\s*"([^"]+)"\.\s*(.*?)\s*Lo que NO puede:\s*(.+)$/)
                if (matchPatologia) {
                  const [, antes, pregunta, medio, noPuede] = matchPatologia
                  return (
                    <>
                      {antes.trim() && <p style={{ color: "#374151", fontSize: "18px", lineHeight: 1.7, margin: 0 }}>{antes.trim()}</p>}
                      <div style={{ backgroundColor: "#F0FDF4", borderLeft: "4px solid var(--huap-verde)", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "20px", flexShrink: 0, lineHeight: 1.3 }}>💬</span>
                        <p style={{ color: "#166534", fontSize: "16px", lineHeight: 1.6, margin: 0 }}>
                          <strong>Pregunta útil:</strong> &ldquo;{pregunta}&rdquo;
                        </p>
                      </div>
                      {medio.trim() && <p style={{ color: "#374151", fontSize: "17px", lineHeight: 1.7, margin: 0 }}>{medio.trim()}</p>}
                      <div style={{ backgroundColor: "#FFF5F5", borderLeft: "4px solid var(--huap-rojo)", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "20px", flexShrink: 0, lineHeight: 1.3 }}>⚠️</span>
                        <p style={{ color: "#7f1d1d", fontSize: "16px", lineHeight: 1.6, margin: 0 }}>
                          <strong>Lo que NO puede:</strong> {noPuede.trim()}
                        </p>
                      </div>
                    </>
                  )
                }

                // Patrón "El paciente pregunta: "..."
                const matchPacientePregunta = texto.match(/^(El paciente pregunta):\s*"([^"]+)"\.\s*(.+)$/)
                if (matchPacientePregunta) {
                  const [, intro, pregunta, resto] = matchPacientePregunta
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "18px", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "14px 18px", backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "16px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>?</span>
                        <p style={{ color: "#1e3a5f", fontSize: "17px", fontStyle: "italic", lineHeight: 1.6, margin: 0 }}>&ldquo;{pregunta}&rdquo;</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "17px", lineHeight: 1.7, margin: 0 }}>{resto.trim()}</p>
                    </>
                  )
                }

                // Patrón resumen usos: "Usa la IA para preparar tu consulta: item1, item2 y item3. [cierre]"
                const matchResumenUsos = texto.match(/^(Usa la IA para preparar tu consulta:)\s*([^.]+)\.\s*(.+)$/)
                if (matchResumenUsos) {
                  const [, intro, itemsStr, cierre] = matchResumenUsos
                  const items = itemsStr.split(/,\s+|\s+y\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "18px", lineHeight: 1.7, margin: 0 }}>{intro}</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "15px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                            <p style={{ color: "#166534", fontSize: "16px", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "17px", lineHeight: 1.7, margin: 0 }}>{cierre}</p>
                    </>
                  )
                }

                // Patrón síntomas con ❓: "... síntomas: cuándo empezó, ..."
                const matchSintomas = texto.match(/^(.+?síntomas:)\s*([^.]+)\.\s*(.+)$/)
                if (matchSintomas) {
                  const [, intro, itemsStr, cierre] = matchSintomas
                  const items = itemsStr.split(/,\s*/).map((s: string) => s.trim())
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "18px", lineHeight: 1.7, margin: 0 }}>{intro.trim()}</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "15px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>?</span>
                            <p style={{ color: "#1e3a5f", fontSize: "16px", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>
                              {item.startsWith("¿") ? item : `¿${item.charAt(0).toUpperCase()}${item.slice(1)}?`}
                            </p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "17px", lineHeight: 1.7, margin: 0 }}>{cierre.trim()}</p>
                    </>
                  )
                }

                // Patrón médico de cabecera: "... Cosas como [items], son para tu médico de cabecera, no para el chatbot."
                const matchCabecera = texto.match(/^(.+?Cosas como)\s+(.+),\s*(son para tu médico de cabecera),\s*(no para el chatbot)\.$/)
                if (matchCabecera) {
                  const [, intro, itemsStr, paraMedico, noChat] = matchCabecera
                  const items = itemsStr.split(/,\s*/).map((s: string) => s.replace(/^o\s+/, '').trim())
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "18px", lineHeight: 1.7, margin: 0 }}>{intro.trim()}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "6px 0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "16px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>+</span>
                            <p style={{ color: "#1e3a5f", fontSize: "16px", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "15px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "16px", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{paraMedico.trim().charAt(0).toUpperCase() + paraMedico.trim().slice(1)}</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "15px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                        <p style={{ color: "#7f1d1d", fontSize: "16px", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{noChat.trim().charAt(0).toUpperCase() + noChat.trim().slice(1)}</p>
                      </div>
                    </>
                  )
                }

                // Patrón "No reemplaza / te ayuda": "... No reemplaza a tu médico: [beneficio]. [cierre]."
                const matchNoReemplaza = texto.match(/^(.+?)\.\s*No reemplaza a tu médico:\s*(.+?)\.\s*(.+)$/)
                if (matchNoReemplaza) {
                  const [, intro, beneficio, cierre] = matchNoReemplaza
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "18px", lineHeight: 1.7, margin: 0 }}>{intro.trim()}.</p>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "15px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                        <p style={{ color: "#7f1d1d", fontSize: "16px", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>No reemplaza a tu médico</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "15px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "16px", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{beneficio.trim()}.</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "17px", lineHeight: 1.7, margin: 0 }}>{cierre.trim()}</p>
                    </>
                  )
                }

                // Patrón SÍ/NO: "la IA SÍ ...; NO ..., NO ..."
                const matchSiNo = texto.match(/^(.+?:\s*)la IA SÍ ([^;]+);\s*((?:NO [^.]+))\.\s*(.+)$/)
                if (matchSiNo) {
                  const [, intro, siItem, noItemsStr, cierre] = matchSiNo
                  const noItems = noItemsStr.split(/,\s*/).map((s: string) => s.trim())
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "17px", lineHeight: 1.7, margin: 0 }}>{intro.trim()}</p>
                      {/* SÍ */}
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "15px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "16px", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>la IA SÍ {siItem.trim()}</p>
                      </div>
                      {/* NO items */}
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {noItems.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "15px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                            <p style={{ color: "#7f1d1d", fontSize: "16px", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "17px", lineHeight: 1.7, margin: 0 }}>{cierre.trim()}</p>
                    </>
                  )
                }

                // Patrón "Recuerda:"
                if (texto.includes("Recuerda:")) {
                  const idx = texto.indexOf("Recuerda:")
                  const antes = texto.slice(0, idx).trim()
                  const despues = texto.slice(idx + "Recuerda:".length).trim()
                  return (
                    <>
                      {antes && <p style={{ color: "#374151", fontSize: "18px", lineHeight: 1.7, margin: 0 }}>{antes}</p>}
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "22px", flexShrink: 0, lineHeight: 1.3 }}>💡</span>
                        <p style={{ color: "#1A1A1A", fontSize: "16px", lineHeight: 1.6, margin: 0 }}>
                          <strong>Recuerda:</strong> {despues}
                        </p>
                      </div>
                    </>
                  )
                }

                // Default
                return <p style={{ color: "#374151", fontSize: "18px", lineHeight: 1.7, margin: 0 }}>{texto}</p>
              })()}

              {/* Lista de síntomas de emergencia */}
              {pagina.lista_sintomas && pagina.lista_sintomas.length > 0 && (
                <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                  {pagina.lista_sintomas.map((sintoma: string, i: number) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "11px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                      <span style={{ flexShrink: 0, width: "26px", height: "26px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "14px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                      <p style={{ color: "#7f1d1d", fontSize: "16px", fontWeight: 500, lineHeight: 1.4, margin: 0 }}>{sintoma}</p>
                    </div>
                  ))}
                </div>
              )}

              {/* Imagen o descripción visual */}
              {pagina.apoyo_visual && !pagina.texto.includes("la IA SÍ") && !pagina.texto.includes("síntomas:") && !pagina.texto.includes("preparar tu consulta:") && !pagina.lista_sintomas?.length && !pagina.texto.includes("Cosas como") && (
                IMAGENES_APOYO[pagina.apoyo_visual] ? (
                  (() => {
                    const src = IMAGENES_APOYO[pagina.apoyo_visual]
                    const grande = src === "/lecciones/modulo2/L6-1.svg" || src === "/lecciones/modulo2/L6-5.svg"
                    return (
                      <div style={{ display: "flex", justifyContent: grande ? "stretch" : "center", width: "100%" }}>
                        <Image
                          src={src}
                          alt="Ilustración de la lección"
                          width={grande ? 620 : 340}
                          height={grande ? 620 : 340}
                          style={{ objectFit: "contain", width: grande ? "100%" : undefined, height: grande ? "auto" : undefined, maxWidth: "100%", maxHeight: grande ? "min(80vh, 700px)" : "min(55vh, 420px)" }}
                        />
                      </div>
                    )
                  })()
                ) : (
                  <p
                    style={{
                      padding: "12px 16px",
                      backgroundColor: "#F9FAFB",
                      border: "0.5px solid #E5E7EB",
                      borderRadius: "10px",
                      color: "#6B7280",
                      fontSize: "15px",
                      fontStyle: "italic",
                      lineHeight: 1.5,
                      margin: 0,
                    }}
                  >
                    {pagina.apoyo_visual}
                  </p>
                )
              )}
            </div>
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
                  border: "1px solid var(--huap-azul)",
                  backgroundColor: "white",
                  color: "var(--huap-azul)",
                  fontSize: "17px",
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
                fontSize: "17px",
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

          {/* Progreso del quiz — pill style (ModuloCard) */}
          <div style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
              <span style={{ fontSize: "14px", color: "#6B7280" }}>Quiz rápido</span>
              <span style={{ fontSize: "14px", color: "#6B7280", fontWeight: 500 }}>
                {quiz.indice + 1} / {preguntas.length}
              </span>
            </div>
            <div
              role="progressbar"
              aria-valuenow={quiz.indice + 1}
              aria-valuemin={1}
              aria-valuemax={preguntas.length}
              style={{
                width: "100%",
                height: "5px",
                backgroundColor: "#E5E7EB",
                borderRadius: "999px",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${((quiz.indice + 1) / preguntas.length) * 100}%`,
                  height: "100%",
                  backgroundColor: "var(--huap-verde)",
                  borderRadius: "999px",
                  transition: "width 0.6s ease",
                }}
              />
            </div>
          </div>

          {/* Tarjeta de pregunta — ModuloCard: franja izquierda + border sutil */}
          <div
            style={{
              background: "#FFFFFF",
              borderRadius: "16px",
              border: "0.5px solid #E5E7EB",
              overflow: "hidden",
              marginBottom: "12px",
              display: "flex",
              flexDirection: "row",
            }}
          >
            {/* Franja izquierda verde (ModuloCard signature) */}
            <div
              aria-hidden="true"
              style={{ width: "6px", backgroundColor: "var(--huap-verde)", flexShrink: 0 }}
            />

            {/* Contenido */}
            <div style={{ flex: 1, padding: "24px", display: "flex", flexDirection: "column", gap: "20px" }}>

              {/* Pregunta + botón audio */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "12px" }}>
                <h2 style={{ color: "#111827", fontSize: "18px", fontWeight: 500, lineHeight: 1.5, margin: 0, flex: 1 }}>
                  {preguntaActual.pregunta}
                </h2>
                <button
                  onClick={() => toggleAudio(leccion.contenido.paginas.length + quiz.indice + 1)}
                  style={{
                    flexShrink: 0,
                    alignSelf: "flex-start",
                    marginTop: "-20px",
                    marginRight: "-20px",
                    padding: "2px 10px 2px 8px",
                    borderRadius: "999px",
                    border: `1px solid ${tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)"}`,
                    backgroundColor: "white",
                    color: tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)",
                    fontSize: "14px",
                    fontWeight: 500,
                    cursor: "pointer",
                    whiteSpace: "nowrap",
                    display: "flex",
                    alignItems: "center",
                    gap: "4px",
                  }}
                >
                  <span style={{ fontSize: "22px", lineHeight: 1 }}>🔊</span>
                  <span className="hidden md:inline">{tocandoAudio ? "Detener" : "Escuchar"}</span>
                </button>
              </div>

              {/* Opciones con letra + franja izquierda al seleccionar */}
              <div className="flex flex-col gap-3">
                {preguntaActual.opciones.map((opcion, idx) => {
                  const letra = String.fromCharCode(65 + idx)
                  let bgColor = "white"
                  let boxShadow = "none"
                  let textColor = "#374151"
                  let letraColor = "#6B7280"
                  let letraBg = "#F3F4F6"

                  if (!quiz.mostrandoFeedback && quiz.seleccion === idx) {
                    bgColor = "#F0FDF4"
                    boxShadow = "inset 4px 0 0 var(--huap-verde)"
                    letraColor = "#166534"
                    letraBg = "#DCFCE7"
                  }
                  if (quiz.mostrandoFeedback) {
                    if (opcion.correcta) {
                      bgColor = "#F0FDF4"
                      boxShadow = "inset 4px 0 0 var(--huap-verde)"
                      textColor = "#166534"
                      letraColor = "#166534"
                      letraBg = "#DCFCE7"
                    } else if (quiz.seleccion === idx) {
                      bgColor = "#FFF5F5"
                      boxShadow = "inset 4px 0 0 var(--huap-rojo)"
                      textColor = "#991B1B"
                      letraColor = "#991B1B"
                      letraBg = "#FEE2E2"
                    }
                  }

                  return (
                    <button
                      key={idx}
                      onClick={() => seleccionarOpcion(idx)}
                      disabled={quiz.mostrandoFeedback}
                      style={{
                        padding: "13px 16px",
                        borderRadius: "12px",
                        border: "0.5px solid #E5E7EB",
                        backgroundColor: bgColor,
                        boxShadow,
                        fontSize: "16px",
                        textAlign: "left",
                        cursor: quiz.mostrandoFeedback ? "default" : "pointer",
                        color: textColor,
                        lineHeight: 1.5,
                        fontWeight: 400,
                        transition: "background-color 0.2s ease, box-shadow 0.2s ease",
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                      }}
                    >
                      <span
                        style={{
                          flexShrink: 0,
                          width: "28px",
                          height: "28px",
                          borderRadius: "50%",
                          backgroundColor: letraBg,
                          color: letraColor,
                          fontSize: "13px",
                          fontWeight: 600,
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          transition: "background-color 0.2s ease, color 0.2s ease",
                        }}
                      >
                        {quiz.mostrandoFeedback && opcion.correcta ? "✓" : letra}
                      </span>
                      {opcion.texto}
                    </button>
                  )
                })}
              </div>
            </div>
          </div>

          {/* Animación de entrada para el feedback */}
          <style>{`
            @keyframes feedbackSlideIn {
              from { opacity: 0; transform: translateY(10px); }
              to   { opacity: 1; transform: translateY(0); }
            }
          `}</style>

          {/* Feedback — fuera de la tarjeta, aparece suave y arrastra la vista */}
          {quiz.mostrandoFeedback && (
            <div
              ref={feedbackRef}
              style={{
                padding: "14px 16px",
                backgroundColor: esCorrecta ? "#F0FDF4" : "#FFF5F5",
                border: `0.5px solid ${esCorrecta ? "#BBF7D0" : "#FECACA"}`,
                borderRadius: "12px",
                marginBottom: "12px",
                animation: "feedbackSlideIn 0.35s ease forwards",
              }}
            >
              <p style={{
                color: esCorrecta ? "#166534" : "#a92020",
                fontSize: "14px",
                fontWeight: 600,
                marginBottom: "4px",
              }}>
                {esCorrecta ? "✓ ¡Muy bien!" : "✗ Incorrecto"}
              </p>
              <p style={{ color: esCorrecta ? "#166534" : "#6B7280", fontSize: "15px", lineHeight: 1.5, margin: 0 }}>
                {preguntaActual.feedback}
              </p>
            </div>
          )}

          {/* Botón de acción */}
          {!quiz.mostrandoFeedback ? (
            <button
              onClick={confirmarRespuesta}
              disabled={quiz.seleccion === null}
              style={{
                padding: "16px",
                borderRadius: "12px",
                border: "none",
                backgroundColor: quiz.seleccion !== null ? "var(--huap-azul)" : "#E5E7EB",
                color: quiz.seleccion !== null ? "white" : "#9CA3AF",
                fontSize: "17px",
                fontWeight: 600,
                cursor: quiz.seleccion !== null ? "pointer" : "not-allowed",
                width: "100%",
                transition: "background-color 0.2s ease",
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
                fontSize: "17px",
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
