"use client"

import { useEffect, useRef, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import Image from "next/image"
import Header from "@/components/layout/Header"
import { Trophy, RefreshCw } from "lucide-react"
import { getLeccion, getModuloDetalle, completarLeccion, type LeccionDetalle, type PreguntaQuizCorto, type InsigniaOtorgada } from "@/lib/api"

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

type Fase = "paginas" | "ejercicio" | "quiz" | "insignia" | "resultado"

interface EstadoQuiz {
  indice: number
  seleccion: number | null
  mostrandoFeedback: boolean
  aciertos: number
}

interface EstadoEjercicio {
  indice: number
  seleccion: string | null
  mostrandoFeedback: boolean
  completado: boolean
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
  const [ejercicio, setEjercicio] = useState<EstadoEjercicio>({
    indice: 0,
    seleccion: null,
    mostrandoFeedback: false,
    completado: false,
  })
  const [aprobado, setAprobado] = useState(false)
  const [moduloOrden, setModuloOrden] = useState(0)
  const [insignia, setInsignia] = useState<InsigniaOtorgada | null>(null)
  const [tocandoAudio, setTocandoAudio] = useState(false)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const feedbackRef = useRef<HTMLDivElement>(null)
  const progresoRef = useRef<HTMLDivElement>(null)
  const instruccionRef = useRef<HTMLDivElement>(null)
  const confirmarRef = useRef<HTMLButtonElement>(null)
  const opcionesEjercicioRef = useRef<HTMLDivElement>(null)

  function scrollAProgreso() {
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  function scrollAInstruccion() {
    setTimeout(() => {
      instruccionRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
    }, 50)
  }

  function detenerAudio() {
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current.currentTime = 0
    }
    window.speechSynthesis?.cancel()
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

  function toggleAudioEjercicio(texto: string) {
    if (tocandoAudio) {
      detenerAudio()
      return
    }
    if (!texto.trim()) return
    detenerAudio()
    const utterance = new SpeechSynthesisUtterance(texto)
    utterance.lang = "es-ES"
    utterance.rate = 0.9
    utterance.onend = () => setTocandoAudio(false)
    utterance.onerror = () => setTocandoAudio(false)
    setTocandoAudio(true)
    window.speechSynthesis.speak(utterance)
  }

  useEffect(() => {
    return () => {
      if (audioRef.current) audioRef.current.pause()
      window.speechSynthesis?.cancel()
    }
  }, [])

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
        feedbackRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
      }, 50)
      return () => clearTimeout(t)
    }
  }, [quiz.mostrandoFeedback])

  useEffect(() => {
    if (ejercicio.mostrandoFeedback && feedbackRef.current) {
      const t = setTimeout(() => {
        feedbackRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
      }, 50)
      return () => clearTimeout(t)
    }
  }, [ejercicio.mostrandoFeedback])

  useEffect(() => {
    if (quiz.seleccion !== null && !quiz.mostrandoFeedback && confirmarRef.current) {
      const t = setTimeout(() => {
        confirmarRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" })
      }, 50)
      return () => clearTimeout(t)
    }
  }, [quiz.seleccion, quiz.mostrandoFeedback])

  function avanzarPagina() {
    if (!leccion) return
    detenerAudio()
    if (paginaActual < leccion.contenido.paginas.length - 1) {
      scrollAProgreso()
      setPaginaActual((p) => p + 1)
    } else if (leccion.contenido.ejercicio) {
      setFase("ejercicio")
      setTimeout(() => {
        opcionesEjercicioRef.current?.scrollIntoView({ behavior: "smooth", block: "end" })
      }, 150)
    } else {
      setFase("quiz")
      setTimeout(() => {
        confirmarRef.current?.scrollIntoView({ behavior: "smooth", block: "end" })
      }, 100)
    }
  }

  function retrocederPagina() {
    detenerAudio()
    scrollAProgreso()
    setPaginaActual((p) => p - 1)
  }

  function seleccionarEjercicio(resp: string) {
    if (ejercicio.mostrandoFeedback) return
    setEjercicio((e) => ({ ...e, seleccion: resp, mostrandoFeedback: true }))
  }

  function siguienteEjercicio() {
    if (!leccion) return
    detenerAudio()
    const items = leccion.contenido.ejercicio?.items ?? []
    const siguiente = ejercicio.indice + 1
    if (siguiente >= items.length) {
      setEjercicio((e) => ({ ...e, completado: true }))
    } else {
      setEjercicio((e) => ({
        ...e,
        indice: siguiente,
        seleccion: null,
        mostrandoFeedback: false,
      }))
      scrollAInstruccion()
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
      if (paso && moduloOrden === 3) {
        guardarProgresoMod3()  // muestra pantalla insignia y setea localStorage+chatbot
      } else {
        if (paso) guardarProgreso()
        setFase("resultado")
      }
    } else {
      setTimeout(() => {
        setQuiz((q) => ({
          ...q,
          indice: siguiente,
          seleccion: null,
          mostrandoFeedback: false,
        }))
      }, 450)
      scrollAInstruccion()
    }
  }

  function guardarLocalStorage() {
    const key = `huap_mod${moduloId}_lecciones_completadas`
    const completadas: number[] = JSON.parse(localStorage.getItem(key) ?? "[]")
    if (!completadas.includes(leccionId)) {
      completadas.push(leccionId)
      localStorage.setItem(key, JSON.stringify(completadas))
    }
  }

  function guardarProgreso() {
    completarLeccion(leccionId).catch(() => {})
    guardarLocalStorage()
  }

  function guardarProgresoMod3() {
    guardarLocalStorage()
    localStorage.setItem("huap_chatbot_desbloqueado", "true")
    completarLeccion(leccionId)
      .then((resp) => {
        setInsignia(resp.insignia_otorgada)
        setFase("insignia")
      })
      .catch(() => {
        setInsignia(null)
        setFase("insignia")
      })
  }

  function reiniciarLeccion() {
    setPaginaActual(0)
    setFase("paginas")
    setQuiz({ indice: 0, seleccion: null, mostrandoFeedback: false, aciertos: 0 })
    setEjercicio({ indice: 0, seleccion: null, mostrandoFeedback: false, completado: false })
    setInsignia(null)
  }

  // ── Carga / error ──────────────────────────────────────────────────────────

  if (error) {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main className="flex-1 flex items-center justify-center px-5">
          <p style={{ color: "var(--huap-rojo)", fontSize: "1rem", textAlign: "center" }}>
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
          <p style={{ color: "#888", fontSize: "1rem" }}>Cargando lección...</p>
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
          className="flex-1 flex flex-col px-5 py-6 w-full mx-auto"
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
              fontSize: "0.95rem",
              fontWeight: 600,
              cursor: "pointer",
              marginBottom: "16px",
            }}
          >
            ← Volver
          </button>

          {/* Progreso — pill style (ModuloCard) */}
          <div ref={progresoRef} style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
              <span style={{ fontSize: "0.8rem", color: "#6B7280" }}>{leccion.titulo}</span>
              <span style={{ fontSize: "0.8rem", color: "#6B7280", fontWeight: 500 }}>
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
                <h2 style={{ color: "#111827", fontSize: "1rem", fontWeight: 500, lineHeight: 1.4, margin: 0, flex: 1 }}>
                  {pagina.titulo}
                </h2>
                <button
                  onClick={() => toggleAudio(paginaActual + 1)}
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
                    fontSize: "0.8rem",
                    fontWeight: 500,
                    cursor: "pointer",
                    whiteSpace: "nowrap",
                  }}
                >
                  <span style={{ fontSize: "1.2rem", lineHeight: 1, display: "block" }}>{tocandoAudio ? "⏹" : "🔊"}</span>
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
                      {antes.trim() && <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{antes.trim()}</p>}
                      <div style={{ backgroundColor: "#F0FDF4", borderLeft: "4px solid var(--huap-verde)", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.1rem", flexShrink: 0, lineHeight: 1.3 }}>💬</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>
                          <strong>Pregunta útil:</strong> &ldquo;{pregunta}&rdquo;
                        </p>
                      </div>
                      {medio.trim() && <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{medio.trim()}</p>}
                      <div style={{ backgroundColor: "#FFF5F5", borderLeft: "4px solid var(--huap-rojo)", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.1rem", flexShrink: 0, lineHeight: 1.3 }}>⚠️</span>
                        <p style={{ color: "#7f1d1d", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>
                          <strong>Lo que NO puede:</strong> {noPuede.trim()}
                        </p>
                      </div>
                    </>
                  )
                }

                // Patrón contraste vago/claridad: "... Si preguntas algo muy vago... Si preguntas con claridad..."
                const matchVagoClaridad = texto.match(/^(.+?)\. (Si preguntas algo muy vago[^.]+)\. (Si preguntas con claridad[^.]+)\. (.+)$/)
                if (matchVagoClaridad) {
                  const [, intro, vago, claridad, cierre] = matchVagoClaridad
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro.trim()}.</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                        <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "13px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                          <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                          <p style={{ color: "#7f1d1d", fontSize: "0.9rem", lineHeight: 1.5, margin: 0 }}>{vago.trim()}</p>
                        </div>
                        <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "13px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                          <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                          <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{claridad.trim()}</p>
                        </div>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre.trim()}</p>
                    </>
                  )
                }

                // Patrón "Para preguntar bien: item1, item2 y item3. [cierre]"
                const matchPreguntar = texto.match(/^(Para preguntar bien:)\s*([^.]+)\.\s*(.+)$/)
                if (matchPreguntar) {
                  const [, intro, itemsStr, cierre] = matchPreguntar
                  const items = itemsStr.split(/,\s+|\s+y\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                            <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre}</p>
                    </>
                  )
                }

                // Patrón "NO necesita tu RUT... "[pregunta]" funciona perfecto"
                const matchNoDatos = texto.match(/^(Recuerda lo aprendido: una buena pregunta NO necesita)\s+([^.]+)\.\s+([^"]+)"([^"]+)"\s+(.+)$/)
                if (matchNoDatos) {
                  const [, intro, itemsStr, medio, pregunta, cierre] = matchNoDatos
                  const items = itemsStr.split(/,\s*|\s+ni\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro.trim()}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "10px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "26px", height: "26px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                            <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.4, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{medio.trim()}</p>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "14px 18px", backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>?</span>
                        <p style={{ color: "#1e3a5f", fontSize: "0.95rem", fontStyle: "italic", lineHeight: 1.6, margin: 0 }}>&ldquo;{pregunta}&rdquo;</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre.trim()}</p>
                    </>
                  )
                }

                // Patrón "...palabras simples: "[frase]". [resto]"
                const matchPalabrasSim = texto.match(/^(.+palabras simples:)\s*"([^"]+)"\.\s*(.+)$/)
                if (matchPalabrasSim) {
                  const [, intro, frase, resto] = matchPalabrasSim
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro.trim()}</p>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "14px 18px", backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>💬</span>
                        <p style={{ color: "#1e3a5f", fontSize: "0.95rem", fontStyle: "italic", lineHeight: 1.6, margin: 0 }}>&ldquo;{frase}&rdquo;</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{resto.trim()}</p>
                    </>
                  )
                }

                // Patrón "En lugar de X, di qué te pasa: "[pregunta]". [resto]"
                const matchEnLugarDe = texto.match(/^(En lugar de[^:]+:)\s*"([^"]+)"\.\s*(.+)$/)
                if (matchEnLugarDe) {
                  const [, intro, pregunta, resto] = matchEnLugarDe
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro.trim()}</p>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "14px 18px", backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>?</span>
                        <p style={{ color: "#1e3a5f", fontSize: "0.95rem", fontStyle: "italic", lineHeight: 1.6, margin: 0 }}>&ldquo;{pregunta}&rdquo;</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{resto.trim()}</p>
                    </>
                  )
                }

                // Patrón "El paciente pregunta: "..."
                const matchPacientePregunta = texto.match(/^(El paciente pregunta):\s*"([^"]+)"\.\s*(.+)$/)
                if (matchPacientePregunta) {
                  const [, intro, pregunta, resto] = matchPacientePregunta
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "14px 18px", backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>?</span>
                        <p style={{ color: "#1e3a5f", fontSize: "0.95rem", fontStyle: "italic", lineHeight: 1.6, margin: 0 }}>&ldquo;{pregunta}&rdquo;</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{resto.trim()}</p>
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
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                            <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre}</p>
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
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro.trim()}</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>?</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>
                              {item.startsWith("¿") ? item : `¿${item.charAt(0).toUpperCase()}${item.slice(1)}?`}
                            </p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre.trim()}</p>
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
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro.trim()}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "6px 0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>+</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{paraMedico.trim().charAt(0).toUpperCase() + paraMedico.trim().slice(1)}</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                        <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{noChat.trim().charAt(0).toUpperCase() + noChat.trim().slice(1)}</p>
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
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro.trim()}.</p>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                        <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>No reemplaza a tu médico</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{beneficio.trim()}.</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre.trim()}</p>
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
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{intro.trim()}</p>
                      {/* SÍ */}
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>la IA SÍ {siItem.trim()}</p>
                      </div>
                      {/* NO items */}
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {noItems.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                            <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre.trim()}</p>
                    </>
                  )
                }

                // Patrón "La IA es una herramienta útil, no un reemplazo de tu médico. Úsala para..."
                const matchHerramientaUtil = texto.match(/^(La IA es una herramienta útil[^.]+)\.\s*Úsala para\s*([^,]+)\s*y\s*([^,]+),\s*pero\s*(.+)\.$/)
                if (matchHerramientaUtil) {
                  const [, intro, item1, item2, advertencia] = matchHerramientaUtil
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}.</p>
                      <p style={{ color: "#374151", fontSize: "0.95rem", fontWeight: 600, lineHeight: 1.7, margin: 0 }}>Úsala para:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {[item1, item2].map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                            <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.trim().charAt(0).toUpperCase() + item.trim().slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{advertencia.charAt(0).toUpperCase() + advertencia.slice(1)}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Los chatbots como ChatGPT... Suenan muy seguros... Siempre verifica..."
                const matchChatbots = texto.match(/^(Los chatbots como ChatGPT[^.]+)\.\s*(Suenan muy seguros[^.]+)\.\s*(Siempre verifica[^.]+)\.$/)
                if (matchChatbots) {
                  const [, intro, advertencia, consejo] = matchChatbots
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}.</p>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{advertencia}.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{consejo}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Es importante recordar: la IA no sabe todo... Es una herramienta útil..."
                const matchNoMagica = texto.match(/^(Es importante recordar):\s*(.+?)\.\s*(.+)\.$/)
                if (matchNoMagica) {
                  const [, intro, itemsStr, cierre] = matchNoMagica
                  const items = itemsStr.split(/,\s*(?:y\s+)?/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                            <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre}.</p>
                    </>
                  )
                }

                // Patrón "La IA en salud sirve para X, Y y Z. Nunca para A ni B."
                const matchIASalud = texto.match(/^(La IA en salud sirve para)\s+(.+?)\.\s*(Nunca para)\s+(.+)\.$/)
                if (matchIASalud) {
                  const [, introVerde, verdesStr, introRojo, rojosStr] = matchIASalud
                  const verdes = verdesStr.split(/,\s*|\s+y\s+/).map((s: string) => s.trim()).filter(Boolean)
                  const rojos = rojosStr.split(/\s+ni\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "0.95rem", fontWeight: 600, lineHeight: 1.7, margin: 0 }}>{introVerde}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {verdes.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                            <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", fontWeight: 600, lineHeight: 1.7, margin: 0 }}>{introRojo}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {rojos.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                            <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                    </>
                  )
                }

                // Patrón "Un médico de verdad nunca... Una página oficial... Un anuncio..."
                const matchCasosReales = texto.match(/^(Un médico de verdad.+?)\. (Una página oficial.+?)\. (Un anuncio.+)\.$/)
                if (matchCasosReales) {
                  const [, rojo1, verde, rojo2] = matchCasosReales
                  return (
                    <>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{rojo1}.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{verde}.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{rojo2}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Para saber si una página o mensaje es real: X, Y, y Z."
                const matchParaSaber = texto.match(/^(Para saber si una página o mensaje es real):\s*(.+)\.$/)
                if (matchParaSaber) {
                  const [, intro, itemsStr] = matchParaSaber
                  const items = itemsStr.split(/,\s*(?:y\s+)?/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>+</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                    </>
                  )
                }

                // Patrón "Las estafas de salud... Ante cualquier duda: X, Y, Z. Más vale confirmar..."
                const matchEstafas = texto.match(/^(Las estafas de salud[^.]+)\.\s*Ante cualquier duda:\s*(.+?)\.\s*(Más vale[^.]+)\.$/)
                if (matchEstafas) {
                  const [, ambar, itemsStr, cierre] = matchEstafas
                  const items = itemsStr.split(/,\s*(?:y\s+)?/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{ambar}.</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", fontWeight: 600, lineHeight: 1.7, margin: 0 }}>Ante cualquier duda:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>+</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{cierre}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Desconfía siempre que algo: X, Y, o Z. Los servicios de salud..."
                const matchDesconfia = texto.match(/^(Desconfía siempre que algo):\s*(.+)\.\s*(Los servicios de salud[^.]+)\.$/)
                if (matchDesconfia) {
                  const [, intro, itemsStr, cierre] = matchDesconfia
                  const items = itemsStr.split(/,\s*o\s+|,\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                            <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre}.</p>
                    </>
                  )
                }

                // Patrón "No todo lo que parece un hospital... Hay personas... Aprender a reconocerlos..."
                const matchNoTodoHospital = texto.match(/^(No todo lo que parece[^.]+)\.\s*(Hay personas[^.]+)\.\s*(Aprender a reconocerlos[^.]+)\.$/)
                if (matchNoTodoHospital) {
                  const [, ambar, normal, verde] = matchNoTodoHospital
                  return (
                    <>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{ambar}.</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{normal}.</p>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{verde}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Los datos personales se guardan para ti... Si una IA te pide... desconfía:..."
                const matchDatosPersonales = texto.match(/^(Los datos personales[^.]+)\.\s*(Si una IA te pide[^:]+),\s*desconfía:\s*(.+)\.$/)
                if (matchDatosPersonales) {
                  const [, verde, ambar, rojo] = matchDatosPersonales
                  return (
                    <>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{verde}.</p>
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{ambar}, desconfía.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                        <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{rojo.charAt(0).toUpperCase() + rojo.slice(1)}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Nunca uses la IA para: X, Y, Z. Cierre."
                const matchNuncaUses = texto.match(/^(Nunca uses la IA para):\s*(.+?)\.\s*(.+)\.$/)
                if (matchNuncaUses) {
                  const [, intro, itemsStr, cierre] = matchNuncaUses
                  const items = itemsStr.split(/,\s*(?:o\s+)?/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                            <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.2rem", flexShrink: 0, lineHeight: 1.3 }}>💡</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{cierre}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón caso real "María le contó..."
                const matchCasoMaria = texto.match(/^(María le contó.+medicamentos)\.\s*(¿Por qué pasó\?.+)\.$/)
                if (matchCasoMaria) {
                  const [, historia, conclusion] = matchCasoMaria
                  return (
                    <>
                      <div style={{ backgroundColor: "#F8FAFC", border: "1px solid #E2E8F0", borderRadius: "12px", padding: "16px 18px", display: "flex", gap: "12px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, fontSize: "1.55rem", lineHeight: 1 }}>👤</span>
                        <p style={{ color: "#374151", fontSize: "0.9rem", lineHeight: 1.7, margin: 0 }}>{historia}.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{conclusion}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón caso real "Don Luis empezó..."
                if (texto.startsWith("Don Luis empezó")) {
                  return (
                    <div style={{ backgroundColor: "#F8FAFC", border: "1px solid #E2E8F0", borderRadius: "12px", padding: "16px 18px", display: "flex", gap: "12px", alignItems: "flex-start" }}>
                      <span style={{ flexShrink: 0, fontSize: "1.55rem", lineHeight: 1 }}>👤</span>
                      <p style={{ color: "#374151", fontSize: "0.9rem", lineHeight: 1.7, margin: 0 }}>{texto}</p>
                    </div>
                  )
                }

                // Patrón "Usa la IA para: X, Y, Z, o W."
                const matchUsaIAPara = texto.match(/^(Usa la IA para):\s*(.+)\.$/)
                if (matchUsaIAPara) {
                  const [, intro, itemsStr] = matchUsaIAPara
                  const items = itemsStr.split(/,\s*(?:o\s+)?/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                            <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                    </>
                  )
                }

                // Patrón "La IA lee millones... Puede escribir respuestas útiles, pero también puede cometer errores..."
                const matchIAPatrones = texto.match(/^(La IA lee millones[^.]+)\.\s*(Puede escribir respuestas útiles),\s*pero también\s*(.+)\.$/)
                if (matchIAPatrones) {
                  const [, intro, positivo, negativo] = matchIAPatrones
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}.</p>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{positivo}.</p>
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>También {negativo}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Probablemente ya conviviste con la IA: cuando X, cuando Y... Todo eso es IA."
                const matchConviviste = texto.match(/^(Probablemente ya conviviste con la IA):\s*(.+)\.\s*(Todo eso es inteligencia artificial)\.$/)
                if (matchConviviste) {
                  const [, intro, itemsStr, cierre] = matchConviviste
                  const items = itemsStr.split(/,\s*(?=cuando)|o\s+(?=cuando)/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", fontWeight: 600, lineHeight: 1.7, margin: 0 }}>{cierre}.</p>
                    </>
                  )
                }

                // Patrón definición IA "La inteligencia artificial, o "IA"..."
                const matchDefIA = texto.match(/^(La inteligencia artificial[^.]+)\.\s*(No piensa[^.]+)\.$/)
                if (matchDefIA) {
                  const [, definicion, aclaracion] = matchDefIA
                  return (
                    <>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "14px 18px", backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>💬</span>
                        <p style={{ color: "#1e3a5f", fontSize: "0.95rem", lineHeight: 1.6, margin: 0 }}>{definicion}.</p>
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{aclaracion}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón caso real "La señora Rosa..."
                const matchCasoRosa = texto.match(/^(La señora Rosa.+tomaba)\.\s*(Confirmar le evitó[^.]+)\.$/)
                if (matchCasoRosa) {
                  const [, historia, conclusion] = matchCasoRosa
                  return (
                    <>
                      <div style={{ backgroundColor: "#F8FAFC", border: "1px solid #E2E8F0", borderRadius: "12px", padding: "16px 18px", display: "flex", gap: "12px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, fontSize: "1.55rem", lineHeight: 1 }}>👤</span>
                        <p style={{ color: "#374151", fontSize: "0.9rem", lineHeight: 1.7, margin: 0 }}>{historia}.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{conclusion}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "La IA da respuestas generales. Pero tú tienes X, Y, Z. Algo que sirve... Tu médico sí..."
                const matchIACasoPersonal = texto.match(/^(La IA da respuestas generales)\.\s*Pero tú tienes\s*(.+?)\.\s*(.+?)\.\s*(.+)\.$/)
                if (matchIACasoPersonal) {
                  const [, intro, itemsStr, advertencia, cierre] = matchIACasoPersonal
                  const items = itemsStr.split(/,\s*/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}. Pero tú tienes:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>+</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{advertencia}.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{cierre}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Nunca compartas datos que te identifican...: X, Y, Z."
                const matchNuncaCompartas = texto.match(/^(Nunca compartas datos[^:]+):\s*(.+)\.$/)
                if (matchNuncaCompartas) {
                  const [, intro, itemsStr] = matchNuncaCompartas
                  const items = itemsStr.split(/,\s*|\s+y\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                            <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                    </>
                  )
                }

                // Patrón "Puedes compartir sin problema...: X, Y y Z."
                const matchPuedesCompartir = texto.match(/^(Puedes compartir sin problema[^:]+):\s*(.+)\.$/)
                if (matchPuedesCompartir) {
                  const [, intro, itemsStr] = matchPuedesCompartir
                  const items = itemsStr.split(/,\s*|\s+y\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                            <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                    </>
                  )
                }

                // Patrón "Cuando le hablas a la IA, es como gritar..."
                const matchPlazaGente = texto.match(/^(Cuando le hablas a la IA[^.]+)\.\s*(.+)$/)
                if (matchPlazaGente) {
                  const [, advertencia, resto] = matchPlazaGente
                  return (
                    <>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{advertencia}.</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{resto}</p>
                    </>
                  )
                }

                // Patrón "La IA puede inventar datos, estar desactualizada y no conocer tu caso. Regla de oro:..."
                const matchResumenRiesgos = texto.match(/^La IA puede\s+(.+?)\.\s*Regla de oro:\s*(.+)\.$/)
                if (matchResumenRiesgos) {
                  const [, itemsStr, regladeoro] = matchResumenRiesgos
                  const items = itemsStr.split(/,\s*|\s+y\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "0.95rem", fontWeight: 600, lineHeight: 1.7, margin: 0 }}>La IA puede:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                            <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.2rem", flexShrink: 0, lineHeight: 1.3 }}>💡</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}><strong>Regla de oro:</strong> {regladeoro}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "La IA aprendió hasta cierta fecha. Puede no saber de X, Y o Z. Cierre."
                const matchIADesactualizada = texto.match(/^(La IA aprendió hasta cierta fecha)\.\s*Puede no saber de\s*(.+?)\.\s*(.+)\.$/)
                if (matchIADesactualizada) {
                  const [, intro, itemsStr, cierre] = matchIADesactualizada
                  const items = itemsStr.split(/,\s*(?:de\s+)?|\s+o\s+(?:de\s+)?/).map((s: string) => s.replace(/^de\s+/, "").trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}. Puede no saber de:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>+</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.2rem", flexShrink: 0, lineHeight: 1.3 }}>💡</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{cierre.charAt(0).toUpperCase() + cierre.slice(1)}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "A veces la IA inventa información... Puede inventar X, Y o Z. Por eso..."
                const matchIAInventa = texto.match(/^(A veces la IA inventa[^.]+)\.\s*(Se le llama alucinación)\.\s*Puede inventar\s*(.+?)\.\s*(.+)\.$/)
                if (matchIAInventa) {
                  const [, intro, definicion, itemsStr, cierre] = matchIAInventa
                  const items = itemsStr.split(/,\s*|\s+o\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}. <strong>{definicion}.</strong></p>
                      <p style={{ color: "#374151", fontSize: "0.95rem", fontWeight: 600, lineHeight: 1.7, margin: 0 }}>Puede inventar:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>+</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.2rem", flexShrink: 0, lineHeight: 1.3 }}>💡</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{cierre.charAt(0).toUpperCase() + cierre.slice(1)}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Lo más importante de esta lección: [advertencia]. [conclusión]."
                const matchLoMasImportante = texto.match(/^(Lo más importante de esta lección):\s*(.+?)\.\s*(.+)\.$/)
                if (matchLoMasImportante) {
                  const [, intro, advertencia, conclusion] = matchLoMasImportante
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{advertencia.charAt(0).toUpperCase() + advertencia.slice(1)}.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                        <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{(conclusion.charAt(0).toUpperCase() + conclusion.slice(1)).replace(/\bno\b/, "NO")}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón bienvenida "Hola, te vamos a enseñar..."
                const matchBienvenida = texto.match(/^(Hola, te vamos a enseñar[^.]+)\.\s*No te preocupes si te equivocas:\s*([^.]+)\.\s*(.+)\.$/)
                if (matchBienvenida) {
                  const [, intro, item1, item2] = matchBienvenida
                  return (
                    <>
                      <div style={{ backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, fontSize: "1.33rem", lineHeight: 1.2 }}>👋</span>
                        <p style={{ color: "#1e3a5f", fontSize: "0.95rem", lineHeight: 1.6, margin: 0 }}>{intro}.</p>
                      </div>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                          <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                          <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item1.charAt(0).toUpperCase() + item1.slice(1)}.</p>
                        </div>
                        <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                          <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                          <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item2.charAt(0).toUpperCase() + item2.slice(1)}.</p>
                        </div>
                      </div>
                    </>
                  )
                }

                // Patrón "Si la respuesta dice "X", explicación. Hazle caso: cierre."
                const matchRespuestaDiceUno = texto.match(/^(Si la respuesta dice)\s+"([^"]+)",\s+(.+?)\.\s+(.+)$/)
                if (matchRespuestaDiceUno) {
                  const [, intro, cita, explicacion, cierre] = matchRespuestaDiceUno
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "14px 18px", backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>🤖</span>
                        <p style={{ color: "#1e3a5f", fontSize: "0.95rem", fontStyle: "italic", lineHeight: 1.6, margin: 0 }}>&ldquo;{cita}&rdquo;</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{explicacion}.</p>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.2rem", flexShrink: 0, lineHeight: 1.3 }}>💡</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{cierre}</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Si la respuesta dice "X" o "Y", explicación. Señal."
                const matchRespuestaDice = texto.match(/^(Si la respuesta dice)\s+"([^"]+)"\s+o\s+"([^"]+)",\s+(.+?)\.\s+(.+)$/)
                if (matchRespuestaDice) {
                  const [, intro, item1, item2, explicacion, senal] = matchRespuestaDice
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {[item1, item2].map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>–</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>"{item}"</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{explicacion}.</p>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.2rem", flexShrink: 0, lineHeight: 1.3 }}>⚠️</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{senal}</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Tu trabajo es saber: X y Y"
                const matchTrabajo = texto.match(/^(.+?)\.\s*(Tu trabajo es saber)\s+(.+?)\.\s*(.+)$/)
                if (matchTrabajo) {
                  const [, intro, encabezado, items, cierre] = matchTrabajo
                  const lista = items.split(/\s+y\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}.</p>
                      <p style={{ color: "#374151", fontSize: "0.95rem", fontWeight: 600, lineHeight: 1.7, margin: 0 }}>{encabezado}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {lista.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>–</span>
                            <p style={{ color: "#1e3a5f", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0, textTransform: "capitalize" }}>{item}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre}</p>
                    </>
                  )
                }

                // Patrón "Antes de actuar sobre tu salud... Si hay desacuerdo... Verificar no es desconfiar."
                const matchEnResumenVerificar = texto.match(/^(Antes de actuar sobre tu salud[^.]+)\.\s*(Si hay desacuerdo[^.]+)\.\s*(Verificar no es desconfiar[^.]+)\.$/)
                if (matchEnResumenVerificar) {
                  const [, intro, desacuerdo, cierre] = matchEnResumenVerificar
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}.</p>
                      <div style={{ backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1e3a5f", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{desacuerdo}.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{cierre}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón caso real "Carlos leyó... Verificar le evitó un riesgo grave."
                const matchCasoCarlos = texto.match(/^(Carlos leyó.+reemplazaba)\.\s+(Verificar le evitó[^.]+)\.$/)
                if (matchCasoCarlos) {
                  const [, historia, conclusion] = matchCasoCarlos
                  return (
                    <>
                      <div style={{ backgroundColor: "#F8FAFC", border: "1px solid #E2E8F0", borderRadius: "12px", padding: "16px 18px", display: "flex", gap: "12px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, fontSize: "1.55rem", lineHeight: 1 }}>👤</span>
                        <p style={{ color: "#374151", fontSize: "0.9rem", lineHeight: 1.7, margin: 0 }}>{historia}.</p>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                        <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 600, lineHeight: 1.5, margin: 0 }}>{conclusion}.</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Una regla fácil de recordar: [regla]. Si coinciden, mejor. Si no coinciden, [consecuencia]."
                const matchReglaDosFuentes = texto.match(/^(Una regla fácil de recordar):\s*(.+?)\.\s*(Si las dos coinciden[^.]+)\.\s*(Si no coinciden[^.]+)\.$/)
                if (matchReglaDosFuentes) {
                  const [, intro, regla, coinciden, noCoinciden] = matchReglaDosFuentes
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "#B85C00", color: "white", fontSize: "0.9rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{regla}.</p>
                      </div>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                          <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                          <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{coinciden}.</p>
                        </div>
                        <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                          <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                          <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{noCoinciden}.</p>
                        </div>
                      </div>
                    </>
                  )
                }

                // Patrón "Las fuentes confiables en salud son: X, Y, Z. A o B NO son fuentes confiables."
                const matchFuentes = texto.match(/^(Las fuentes confiables en salud son):\s*(.+?)\.\s+(.+?)\s+NO son fuentes confiables\.$/)
                if (matchFuentes) {
                  const [, intro, verdesStr, rojosStr] = matchFuentes
                  const verdes = verdesStr.split(/,\s+/).map((s: string) => s.replace(/^y\s+/, "").trim()).filter(Boolean)
                  const rojos = rojosStr.split(/\s+o\s+/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {verdes.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#F0FDF4", borderRadius: "10px", border: "1px solid #BBF7D0" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-verde)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
                            <p style={{ color: "#166534", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", fontWeight: 600, lineHeight: 1.7, margin: 0 }}>NO son fuentes confiables:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {rojos.map((item: string, i: number) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                            <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</span>
                            <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.5, margin: 0 }}>{item.charAt(0).toUpperCase() + item.slice(1)}</p>
                          </div>
                        ))}
                      </div>
                    </>
                  )
                }

                // Patrón "...verificarlo. Verificar significa [definición]. Cierre."
                const matchVerificar = texto.match(/^(.+?verificarlo)\.\s*(Verificar significa [^.]+)\.\s*(.+)$/)
                if (matchVerificar) {
                  const [, intro, definicion, cierre] = matchVerificar
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}.</p>
                      <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", padding: "14px 18px", backgroundColor: "#EFF6FF", borderLeft: "4px solid var(--huap-azul)", borderRadius: "10px" }}>
                        <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.85rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>i</span>
                        <p style={{ color: "#1e3a5f", fontSize: "0.95rem", lineHeight: 1.6, margin: 0 }}>{definicion}.</p>
                      </div>
                      <p style={{ color: "#374151", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{cierre}</p>
                    </>
                  )
                }

                // Patrón "Aprende a leer las señales: "X" = Y; "X" = Y. Cierre."
                const matchSenales = texto.match(/^(Aprende a leer las señales):\s*(.+)\.\s*(.+)$/)
                if (matchSenales) {
                  const [, intro, itemsStr, cierre] = matchSenales
                  const items = itemsStr.split(/;\s*/).map((s: string) => s.trim()).filter(Boolean)
                  return (
                    <>
                      <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{intro}:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {items.map((item: string, i: number) => {
                          const partes = item.match(/^"([^"]+)"\s*=\s*(.+)$/)
                          return (
                            <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px 16px", backgroundColor: "#EFF6FF", borderRadius: "10px", border: "1px solid #BFDBFE" }}>
                              <span style={{ flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%", backgroundColor: "var(--huap-azul)", color: "white", fontSize: "0.9rem", display: "flex", alignItems: "center", justifyContent: "center" }}>🤖</span>
                              <p style={{ color: "#1e3a5f", fontSize: "0.9rem", lineHeight: 1.5, margin: 0 }}>
                                {partes ? <><em>&ldquo;{partes[1]}&rdquo;</em> <span style={{ color: "#374151" }}>= {partes[2]}</span></> : item}
                              </p>
                            </div>
                          )
                        })}
                      </div>
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.2rem", flexShrink: 0, lineHeight: 1.3 }}>💡</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>{cierre}</p>
                      </div>
                    </>
                  )
                }

                // Patrón "Recuerda:" o "Recuerda siempre:"
                const recuerdaKeyword = texto.includes("Recuerda siempre:") ? "Recuerda siempre:" : texto.includes("Recuerda:") ? "Recuerda:" : null
                if (recuerdaKeyword) {
                  const idx = texto.indexOf(recuerdaKeyword)
                  const antes = texto.slice(0, idx).trim()
                  const despues = texto.slice(idx + recuerdaKeyword.length).trim()
                  return (
                    <>
                      {antes && <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{antes}</p>}
                      <div style={{ backgroundColor: "#FFF4E6", borderLeft: "4px solid #B85C00", borderRadius: "10px", padding: "14px 18px", display: "flex", gap: "10px", alignItems: "flex-start" }}>
                        <span style={{ fontSize: "1.2rem", flexShrink: 0, lineHeight: 1.3 }}>💡</span>
                        <p style={{ color: "#1A1A1A", fontSize: "0.9rem", lineHeight: 1.6, margin: 0 }}>
                          <strong>{recuerdaKeyword}</strong> {despues}
                        </p>
                      </div>
                    </>
                  )
                }

                // Default
                return <p style={{ color: "#374151", fontSize: "1rem", lineHeight: 1.7, margin: 0 }}>{texto}</p>
              })()}

              {/* Lista de síntomas de emergencia */}
              {pagina.lista_sintomas && pagina.lista_sintomas.length > 0 && (
                <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                  {pagina.lista_sintomas.map((sintoma: string, i: number) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "11px 16px", backgroundColor: "#FFF5F5", borderRadius: "10px", border: "1px solid #FECACA" }}>
                      <span style={{ flexShrink: 0, width: "26px", height: "26px", borderRadius: "50%", backgroundColor: "var(--huap-rojo)", color: "white", fontSize: "0.8rem", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>!</span>
                      <p style={{ color: "#7f1d1d", fontSize: "0.9rem", fontWeight: 500, lineHeight: 1.4, margin: 0 }}>{sintoma}</p>
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
                      fontSize: "0.85rem",
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
                onClick={retrocederPagina}
                style={{
                  flex: 1,
                  padding: "16px",
                  borderRadius: "12px",
                  border: "1px solid var(--huap-azul)",
                  backgroundColor: "white",
                  color: "var(--huap-azul)",
                  fontSize: "0.95rem",
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
                fontSize: "0.95rem",
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
              {paginaActual < totalPaginas - 1 ? "Siguiente →" : leccion.contenido.ejercicio ? "Ir al ejercicio →" : "Ir al quiz →"}
            </button>
          </div>
        </main>
      </div>
    )
  }

  // ── FASE: EJERCICIO ────────────────────────────────────────────────────────

  if (fase === "ejercicio" && leccion.contenido.ejercicio) {
    const ej = leccion.contenido.ejercicio
    const items = ej.items
    const itemActual = items[ejercicio.indice]
    const respuestaCorrecta = (ej.tipo === "detectar_riesgo" || ej.tipo === "etiquetar_respuestas")
      ? itemActual?.etiqueta
      : ej.tipo === "elegir_mejor_pregunta"
      ? itemActual?.mejor
      : ej.tipo === "construye_tu_consulta"
      ? (itemActual?.util ? "SÍ" : "NO")
      : itemActual?.respuesta
    const esCorrecto = ejercicio.seleccion === respuestaCorrecta

    const textoAudioEjercicio = (() => {
      const textoItem = ej.tipo === "elegir_mejor_pregunta"
        ? (itemActual?.opciones ?? []).join(". ")
        : ej.tipo === "etiquetar_respuestas"
        ? (itemActual?.respuesta_ia ?? "")
        : ej.tipo === "pregunta_util_o_no" || ej.tipo === "construye_tu_consulta"
        ? [itemActual?.patologia, itemActual?.pregunta].filter(Boolean).join(". ")
        : (itemActual?.fuente ?? itemActual?.caso ?? itemActual?.frase ?? itemActual?.situacion ?? "")
      return [ej.instruccion, textoItem].filter(Boolean).join(". ")
    })()


    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main
          className="flex-1 flex flex-col px-5 py-6 w-full mx-auto"
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

          {/* Progreso ejercicio */}
          <div ref={progresoRef} style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
              <span style={{ fontSize: "14px", color: "#6B7280" }}>{leccion.titulo} — Ejercicio</span>
              {!ejercicio.completado && (
                <span style={{ fontSize: "14px", color: "#6B7280", fontWeight: 500 }}>
                  {ejercicio.indice + 1} / {items.length}
                </span>
              )}
            </div>
            {!ejercicio.completado && (
              <div
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
                    width: `${((ejercicio.indice + 1) / items.length) * 100}%`,
                    height: "100%",
                    backgroundColor: "var(--huap-verde)",
                    borderRadius: "999px",
                    transition: "width 0.6s ease",
                  }}
                />
              </div>
            )}
          </div>

          {ejercicio.completado ? (
            /* ── Pantalla de cierre ── */
            <div
              style={{
                background: "#FFFFFF",
                borderRadius: "16px",
                border: "0.5px solid #E5E7EB",
                padding: "32px 24px",
                textAlign: "center",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: "16px",
              }}
            >
              <div style={{ fontSize: "56px" }}>🎉</div>
              <p style={{ fontSize: "22px", fontWeight: 700, color: "var(--huap-azul)" }}>
                ¡Muy bien!
              </p>
              <p style={{ fontSize: "18px", color: "#374151", lineHeight: 1.5 }}>
                Completaste el ejercicio. Ahora responde unas preguntas rápidas.
              </p>
              <button
                onClick={() => setFase("quiz")}
                style={{
                  marginTop: "8px",
                  padding: "16px 32px",
                  borderRadius: "14px",
                  border: "none",
                  backgroundColor: "var(--huap-azul)",
                  color: "white",
                  fontSize: "19px",
                  fontWeight: 700,
                  cursor: "pointer",
                  width: "100%",
                }}
              >
                Continuar al quiz →
              </button>
            </div>
          ) : (
            /* ── Tarjeta de pregunta ── */
            <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
              {/* Instrucción */}
              <div
                ref={instruccionRef}
                className="pr-[44px] md:pr-[130px]"
                style={{
                  background: "#EFF6FF",
                  borderRadius: "14px",
                  paddingTop: "16px",
                  paddingBottom: "16px",
                  paddingLeft: "20px",
                  borderLeft: "4px solid var(--huap-azul)",
                  position: "relative",
                  scrollMarginTop: "12px",
                }}
              >
                <p style={{ fontSize: "17px", color: "var(--huap-azul)", fontWeight: 600, margin: 0 }}>
                  🤖 {ej.instruccion}
                </p>
                <button
                  onClick={() => toggleAudioEjercicio(textoAudioEjercicio)}
                  className="flex items-center justify-center gap-1 p-[6px] md:py-[2px] md:pl-[8px] md:pr-[10px]"
                  style={{
                    position: "absolute",
                    top: "8px",
                    right: "10px",
                    borderRadius: "999px",
                    border: `1px solid ${tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)"}`,
                    backgroundColor: "white",
                    color: tocandoAudio ? "var(--huap-rojo)" : "var(--huap-azul)",
                    fontSize: "0.8rem",
                    fontWeight: 500,
                    cursor: "pointer",
                    whiteSpace: "nowrap",
                  }}
                >
                  <span style={{ fontSize: "1.2rem", lineHeight: 1, display: "block" }}>{tocandoAudio ? "⏹" : "🔊"}</span>
                  <span className="hidden md:inline">{tocandoAudio ? "Detener" : "Escuchar"}</span>
                </button>
              </div>

              {/* Situación (oculta para tipos que muestran respuesta_ia o sus propias opciones) */}
              {ej.tipo !== "elegir_mejor_pregunta" && ej.tipo !== "detectar_riesgo" && ej.tipo !== "etiquetar_respuestas" && ej.tipo !== "pregunta_util_o_no" && ej.tipo !== "construye_tu_consulta" && (
                <div
                  style={{
                    background: "#FFFFFF",
                    borderRadius: "16px",
                    border: "0.5px solid #E5E7EB",
                    padding: "28px 24px",
                    textAlign: "center",
                  }}
                >
                  <p style={{ fontSize: "20px", color: "#1F2937", lineHeight: 1.5, margin: 0, fontWeight: 500 }}>
                    {itemActual?.fuente ?? itemActual?.caso ?? itemActual?.frase ?? itemActual?.situacion}
                  </p>
                </div>
              )}

              {/* Botones según tipo */}
              {!ejercicio.mostrandoFeedback && ej.tipo === "clasificar_es_ia" && (
                <div style={{ display: "flex", gap: "16px" }}>
                  <button
                    onClick={() => seleccionarEjercicio("SÍ")}
                    style={{
                      flex: 1,
                      padding: "20px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-verde)",
                      color: "white",
                      fontSize: "26px",
                      fontWeight: 800,
                      cursor: "pointer",
                    }}
                  >
                    SÍ
                  </button>
                  <button
                    onClick={() => seleccionarEjercicio("NO")}
                    style={{
                      flex: 1,
                      padding: "20px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-rojo)",
                      color: "white",
                      fontSize: "26px",
                      fontWeight: 800,
                      cursor: "pointer",
                    }}
                  >
                    NO
                  </button>
                </div>
              )}

              {!ejercicio.mostrandoFeedback && ej.tipo === "clasificar_uso_apropiado" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  <button
                    onClick={() => seleccionarEjercicio("SÍ PUEDE AYUDAR")}
                    style={{
                      padding: "20px 24px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-verde)",
                      color: "white",
                      fontSize: "20px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    ✓ SÍ PUEDE AYUDAR
                  </button>
                  <button
                    onClick={() => seleccionarEjercicio("ESO ES DEL MÉDICO")}
                    style={{
                      padding: "20px 24px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-azul)",
                      color: "white",
                      fontSize: "20px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    🩺 ESO ES DEL MÉDICO
                  </button>
                </div>
              )}

              {!ejercicio.mostrandoFeedback && ej.tipo === "pregunta_util_o_no" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  {/* Chip de patología + pregunta */}
                  <div
                    style={{
                      background: "#FFFFFF",
                      borderRadius: "16px",
                      border: "0.5px solid #E5E7EB",
                      padding: "24px",
                    }}
                  >
                    {itemActual?.patologia && (
                      <span
                        style={{
                          display: "inline-block",
                          backgroundColor: "#EFF6FF",
                          color: "var(--huap-azul)",
                          borderRadius: "999px",
                          padding: "4px 14px",
                          fontSize: "14px",
                          fontWeight: 700,
                          marginBottom: "12px",
                        }}
                      >
                        {itemActual.patologia}
                      </span>
                    )}
                    <p style={{ fontSize: "20px", color: "#1F2937", lineHeight: 1.5, margin: 0, fontWeight: 500 }}>
                      {itemActual?.pregunta}
                    </p>
                  </div>
                  <button
                    onClick={() => seleccionarEjercicio("ÚTIL")}
                    style={{
                      padding: "20px 24px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-verde)",
                      color: "white",
                      fontSize: "20px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    ✓ ÚTIL PARA LA IA
                  </button>
                  <button
                    onClick={() => seleccionarEjercicio("DEL MÉDICO")}
                    style={{
                      padding: "20px 24px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-azul)",
                      color: "white",
                      fontSize: "20px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    🩺 ESO ES DEL MÉDICO
                  </button>
                </div>
              )}

              {!ejercicio.mostrandoFeedback && ej.tipo === "construye_tu_consulta" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  {/* Contexto de situación */}
                  {ej.situacion_ejemplo && (
                    <div
                      style={{
                        background: "#EFF6FF",
                        borderRadius: "12px",
                        padding: "14px 18px",
                        borderLeft: "4px solid var(--huap-azul)",
                      }}
                    >
                      <p style={{ fontSize: "15px", color: "var(--huap-azul)", fontWeight: 700, margin: 0 }}>
                        📋 Situación: {ej.situacion_ejemplo}
                      </p>
                    </div>
                  )}
                  {/* Pregunta */}
                  <div
                    style={{
                      background: "#FFFFFF",
                      borderRadius: "16px",
                      border: "0.5px solid #E5E7EB",
                      padding: "24px",
                      textAlign: "center",
                    }}
                  >
                    <p style={{ fontSize: "20px", color: "#1F2937", lineHeight: 1.5, margin: 0, fontWeight: 500 }}>
                      {itemActual?.pregunta}
                    </p>
                  </div>
                  <p style={{ fontSize: "16px", color: "#374151", fontWeight: 600, margin: "4px 0 0 0" }}>
                    ¿Vale la pena llevar esta pregunta al médico?
                  </p>
                  <button
                    onClick={() => seleccionarEjercicio("SÍ")}
                    style={{
                      padding: "20px 24px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-verde)",
                      color: "white",
                      fontSize: "20px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    ✓ SÍ, LA LLEVO
                  </button>
                  <button
                    onClick={() => seleccionarEjercicio("NO")}
                    style={{
                      padding: "20px 24px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-rojo)",
                      color: "white",
                      fontSize: "20px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    ✕ NO, LA DESCARTO
                  </button>
                </div>
              )}

              {!ejercicio.mostrandoFeedback && ej.tipo === "semaforo_privacidad" && (
                <div style={{ display: "flex", gap: "16px" }}>
                  <button
                    onClick={() => seleccionarEjercicio("VERDE")}
                    style={{
                      flex: 1,
                      padding: "20px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-verde)",
                      color: "white",
                      fontSize: "18px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    ✓ SÍ
                  </button>
                  <button
                    onClick={() => seleccionarEjercicio("ROJO")}
                    style={{
                      flex: 1,
                      padding: "20px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-rojo)",
                      color: "white",
                      fontSize: "18px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    ✕ NO
                  </button>
                </div>
              )}

              {!ejercicio.mostrandoFeedback && ej.tipo === "clasificar_fuente" && (
                <div style={{ display: "flex", gap: "16px" }}>
                  <button
                    onClick={() => seleccionarEjercicio("CONFIABLE")}
                    style={{
                      flex: 1,
                      padding: "20px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-verde)",
                      color: "white",
                      fontSize: "18px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    ✓ CONFIABLE
                  </button>
                  <button
                    onClick={() => seleccionarEjercicio("NO CONFIABLE")}
                    style={{
                      flex: 1,
                      padding: "20px",
                      borderRadius: "14px",
                      border: "none",
                      backgroundColor: "var(--huap-rojo)",
                      color: "white",
                      fontSize: "18px",
                      fontWeight: 800,
                      cursor: "pointer",
                      textAlign: "center",
                    }}
                  >
                    ✕ NO CONFIABLE
                  </button>
                </div>
              )}

              {!ejercicio.mostrandoFeedback && ej.tipo === "detective_estafas" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  {[
                    { label: "CONFIABLE",         icon: "✓", bg: "var(--huap-verde)" },
                    { label: "VERIFICAR ANTES",   icon: "⚠", bg: "#F59E0B" },
                    { label: "SOSPECHOSO",        icon: "✕", bg: "var(--huap-rojo)" },
                  ].map(({ label, icon, bg }) => (
                    <button
                      key={label}
                      onClick={() => seleccionarEjercicio(label === "VERIFICAR ANTES" ? "VERIFICAR" : label)}
                      style={{
                        padding: "18px 24px",
                        borderRadius: "14px",
                        border: "none",
                        backgroundColor: bg,
                        color: "white",
                        fontSize: "19px",
                        fontWeight: 700,
                        cursor: "pointer",
                        textAlign: "left",
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                      }}
                    >
                      <span style={{ fontSize: "20px" }}>{icon}</span>
                      {label}
                    </button>
                  ))}
                </div>
              )}

              {!ejercicio.mostrandoFeedback && ej.tipo === "elegir_mejor_pregunta" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  <p style={{ fontSize: "16px", color: "#374151", fontWeight: 600, margin: 0 }}>
                    ¿Cuál es la mejor pregunta?
                  </p>
                  {(itemActual?.opciones ?? []).map((opcion: string) => (
                    <button
                      key={opcion}
                      onClick={() => seleccionarEjercicio(opcion)}
                      style={{
                        padding: "20px 24px",
                        borderRadius: "14px",
                        border: "1.5px solid #E5E7EB",
                        backgroundColor: "#FFFFFF",
                        color: "#1F2937",
                        fontSize: "18px",
                        fontWeight: 500,
                        cursor: "pointer",
                        textAlign: "left",
                        lineHeight: 1.4,
                      }}
                    >
                      {opcion}
                    </button>
                  ))}
                </div>
              )}

              {!ejercicio.mostrandoFeedback && ej.tipo === "etiquetar_respuestas" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  {/* Card con la respuesta de la IA */}
                  <div
                    style={{
                      background: "#F8FAFC",
                      borderRadius: "14px",
                      border: "1.5px solid #CBD5E1",
                      padding: "20px 24px",
                    }}
                  >
                    <p style={{ fontSize: "13px", color: "#6B7280", fontWeight: 600, margin: "0 0 8px 0", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                      🤖 La IA respondió:
                    </p>
                    <p style={{ fontSize: "18px", color: "#1F2937", lineHeight: 1.5, margin: 0, fontStyle: "italic" }}>
                      {itemActual?.respuesta_ia}
                    </p>
                  </div>
                  <p style={{ fontSize: "16px", color: "#374151", fontWeight: 600, margin: "4px 0 0 0" }}>
                    ¿Cómo clasificas esta respuesta?
                  </p>
                  {[
                    { label: "información útil",            icon: "💡", bg: "var(--huap-azul)" },
                    { label: "debo consultar al médico",    icon: "🩺", bg: "var(--huap-verde)" },
                    { label: "cuidado, puede estar adivinando", icon: "⚠", bg: "#F59E0B" },
                  ].map(({ label, icon, bg }) => (
                    <button
                      key={label}
                      onClick={() => seleccionarEjercicio(label)}
                      style={{
                        padding: "18px 24px",
                        borderRadius: "14px",
                        border: "none",
                        backgroundColor: bg,
                        color: "white",
                        fontSize: "18px",
                        fontWeight: 700,
                        cursor: "pointer",
                        textAlign: "left",
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                      }}
                    >
                      <span style={{ fontSize: "20px" }}>{icon}</span>
                      {label}
                    </button>
                  ))}
                </div>
              )}

              {!ejercicio.mostrandoFeedback && ej.tipo === "ia_medico_o_urgencias" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  {[
                    { label: "IA",                  icon: "🤖", bg: "var(--huap-azul)" },
                    { label: "MÉDICO DE CABECERA",  icon: "🩺", bg: "var(--huap-verde)" },
                    { label: "URGENCIAS YA",        icon: "🚨", bg: "var(--huap-rojo)" },
                  ].map(({ label, icon, bg }) => (
                    <button
                      key={label}
                      onClick={() => seleccionarEjercicio(label)}
                      style={{
                        padding: label === "URGENCIAS YA" ? "22px 24px" : "18px 24px",
                        borderRadius: "14px",
                        border: "none",
                        backgroundColor: bg,
                        color: "white",
                        fontSize: label === "URGENCIAS YA" ? "21px" : "19px",
                        fontWeight: 800,
                        cursor: "pointer",
                        textAlign: "left",
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                      }}
                    >
                      <span style={{ fontSize: "22px" }}>{icon}</span>
                      {label}
                    </button>
                  ))}
                </div>
              )}

              {/* Botones detectar_riesgo */}
              {!ejercicio.mostrandoFeedback && ej.tipo === "detectar_riesgo" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  {/* Card con la respuesta de la IA */}
                  <div
                    style={{
                      background: "#F8FAFC",
                      borderRadius: "14px",
                      border: "1.5px solid #CBD5E1",
                      padding: "20px 24px",
                    }}
                  >
                    <p style={{ fontSize: "13px", color: "#6B7280", fontWeight: 600, margin: "0 0 8px 0", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                      🤖 La IA respondió:
                    </p>
                    <p style={{ fontSize: "18px", color: "#1F2937", lineHeight: 1.5, margin: 0, fontStyle: "italic" }}>
                      {itemActual?.respuesta_ia}
                    </p>
                  </div>
                  <p style={{ fontSize: "16px", color: "#374151", fontWeight: 600, margin: "4px 0 0 0" }}>
                    ¿Qué riesgo tiene esta respuesta?
                  </p>
                  {[
                    { label: "Puede estar inventando", icon: "🔴" },
                    { label: "Puede estar desactualizada", icon: "🕐" },
                    { label: "No conoce mi caso", icon: "👤" },
                  ].map(({ label, icon }) => (
                    <button
                      key={label}
                      onClick={() => seleccionarEjercicio(label)}
                      style={{
                        padding: "18px 24px",
                        borderRadius: "14px",
                        border: "1.5px solid #E5E7EB",
                        backgroundColor: "#FFFFFF",
                        color: "#1F2937",
                        fontSize: "18px",
                        fontWeight: 600,
                        cursor: "pointer",
                        textAlign: "left",
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                      }}
                    >
                      <span style={{ fontSize: "20px" }}>{icon}</span>
                      {label}
                    </button>
                  ))}
                </div>
              )}

              {/* Anchor para scroll al final de las opciones */}
              <div ref={opcionesEjercicioRef} style={{ scrollMarginBottom: "70px" }} />

              {/* Feedback */}
              {ejercicio.mostrandoFeedback && (
                <div
                  ref={feedbackRef}
                  style={{
                    background: esCorrecto ? "#F0FDF4" : "#FFF7ED",
                    borderRadius: "14px",
                    padding: "20px 24px",
                    borderLeft: `4px solid ${esCorrecto ? "var(--huap-verde)" : "#F59E0B"}`,
                    display: "flex",
                    flexDirection: "column",
                    gap: "12px",
                  }}
                >
                  <p style={{ fontSize: "22px", fontWeight: 700, margin: 0, color: esCorrecto ? "var(--huap-verde)" : "#B45309" }}>
                    {esCorrecto ? "✓ ¡Correcto!" : "Respuesta correcta: " + respuestaCorrecta}
                  </p>
                  <p style={{ fontSize: "17px", color: "#374151", margin: 0 }}>
                    <strong>Respuesta:</strong>{" "}
                    {itemActual?.motivo
                      ? itemActual.motivo
                      : respuestaCorrecta === "IA"
                      ? "La IA puede ayudarte a entender esto."
                      : respuestaCorrecta === "MÉDICO DE CABECERA"
                      ? "Esto requiere una consulta con tu médico de cabecera."
                      : respuestaCorrecta === "URGENCIAS YA"
                      ? "Esta es una emergencia — hay que ir a urgencias de inmediato."
                      : respuestaCorrecta === "ÚTIL"
                      ? "La IA puede orientarte sobre esto."
                      : respuestaCorrecta === "DEL MÉDICO"
                      ? "Esto es mejor consultarlo directamente con tu médico."
                      : respuestaCorrecta === "CONFIABLE"
                      ? "Esta es una fuente confiable para verificar información de salud."
                      : respuestaCorrecta === "NO CONFIABLE"
                      ? "Esta fuente no es confiable para temas de salud."
                      : respuestaCorrecta === "VERDE"
                      ? "Esto se puede compartir con la IA sin problema."
                      : respuestaCorrecta === "ROJO"
                      ? "Esto es dato privado — nunca lo compartas con una IA."
                      : respuestaCorrecta === "SÍ PUEDE AYUDAR"
                      ? "La IA puede ayudar con esto."
                      : respuestaCorrecta === "ESO ES DEL MÉDICO"
                      ? "Esto es tarea del médico, no de la IA."
                      : respuestaCorrecta === "SÍ"
                      ? "Esto usa inteligencia artificial."
                      : respuestaCorrecta === "NO"
                      ? "Esto no usa inteligencia artificial."
                      : respuestaCorrecta ?? ""}
                  </p>
                  <button
                    onClick={siguienteEjercicio}
                    style={{
                      marginTop: "4px",
                      padding: "14px 24px",
                      borderRadius: "12px",
                      border: "none",
                      backgroundColor: "var(--huap-azul)",
                      color: "white",
                      fontSize: "18px",
                      fontWeight: 700,
                      cursor: "pointer",
                    }}
                  >
                    {ejercicio.indice + 1 < items.length ? "Siguiente →" : "Ver resultado →"}
                  </button>
                </div>
              )}
            </div>
          )}
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
          className="flex-1 flex flex-col px-5 py-6 w-full mx-auto"
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
              fontSize: "0.95rem",
              fontWeight: 600,
              cursor: "pointer",
              marginBottom: "16px",
            }}
          >
            ← Volver
          </button>

          {/* Progreso del quiz — pill style (ModuloCard) */}
          <div ref={progresoRef} style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
              <span style={{ fontSize: "0.8rem", color: "#6B7280" }}>Quiz rápido</span>
              <span style={{ fontSize: "0.8rem", color: "#6B7280", fontWeight: 500 }}>
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
            ref={instruccionRef}
            style={{
              background: "#FFFFFF",
              borderRadius: "16px",
              border: "0.5px solid #E5E7EB",
              overflow: "hidden",
              marginBottom: "12px",
              display: "flex",
              flexDirection: "row",
              scrollMarginTop: "12px",
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
                <h2 style={{ color: "#111827", fontSize: "1rem", fontWeight: 500, lineHeight: 1.5, margin: 0, flex: 1 }}>
                  {preguntaActual.pregunta}
                </h2>
                <button
                  onClick={() => toggleAudio(leccion.contenido.paginas.length + quiz.indice + 1)}
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
                    fontSize: "0.8rem",
                    fontWeight: 500,
                    cursor: "pointer",
                    whiteSpace: "nowrap",
                  }}
                >
                  <span style={{ fontSize: "1.2rem", lineHeight: 1, display: "block" }}>{tocandoAudio ? "⏹" : "🔊"}</span>
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
                        fontSize: "0.9rem",
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
                          fontSize: "0.75rem",
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
                fontSize: "0.8rem",
                fontWeight: 600,
                marginBottom: "4px",
              }}>
                {esCorrecta ? "✓ ¡Muy bien!" : "✗ Incorrecto"}
              </p>
              <p style={{ color: esCorrecta ? "#166534" : "#6B7280", fontSize: "0.85rem", lineHeight: 1.5, margin: 0 }}>
                {preguntaActual.feedback}
              </p>
            </div>
          )}

          {/* Botón de acción */}
          {!quiz.mostrandoFeedback ? (
            <button
              ref={confirmarRef}
              onClick={confirmarRespuesta}
              disabled={quiz.seleccion === null}
              style={{
                padding: "16px",
                borderRadius: "12px",
                border: "none",
                backgroundColor: quiz.seleccion !== null ? "var(--huap-azul)" : "#E5E7EB",
                color: quiz.seleccion !== null ? "white" : "#9CA3AF",
                fontSize: "0.95rem",
                fontWeight: 600,
                cursor: quiz.seleccion !== null ? "pointer" : "not-allowed",
                width: "100%",
                transition: "background-color 0.2s ease",
                scrollMarginBottom: "120px",
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
                fontSize: "0.95rem",
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

  // ── FASE: INSIGNIA (Módulo 3) ──────────────────────────────────────────────

  if (fase === "insignia") {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main
          className="flex-1 flex flex-col items-center justify-center px-5 py-8 w-full mx-auto"
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
            {insignia?.icono_url ?? "🤖"}
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
            Completaste el <strong>Módulo 3</strong> y estás listo para usar el Asistente de IA.
          </p>

          {/* Chip de insignia */}
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
              onClick={() => router.push("/chatbot")}
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
              Ir al Asistente de IA →
            </button>
            <button
              onClick={() => router.push("/modulos")}
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
              Volver al inicio
            </button>
          </div>
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
        className="flex-1 flex flex-col items-center justify-center px-5 py-8 w-full mx-auto"
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
              fontSize: "1.33rem",
              marginBottom: "12px",
            }}
          >
            {aprobado ? resultado.titulo_aprobado : resultado.titulo_fallido}
          </h2>
          <p style={{ color: "#555", fontSize: "1rem", lineHeight: 1.6, marginBottom: "12px" }}>
            {aprobado ? resultado.mensaje_aprobado : resultado.mensaje_fallido}
          </p>
          <p style={{ color: "#aaa", fontSize: "0.85rem", marginBottom: "32px" }}>
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
                  fontSize: "0.95rem",
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
                fontSize: "0.95rem",
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
