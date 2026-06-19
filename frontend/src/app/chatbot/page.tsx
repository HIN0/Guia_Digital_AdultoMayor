"use client"

import { useState, useEffect, useRef, useCallback } from "react"
import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import Header from "@/components/layout/Header"
import { MessageCircle, Send, AlertTriangle, ThumbsUp, ThumbsDown, Volume2, VolumeX, RotateCcw, History, X, ChevronRight } from "lucide-react"
import {
  preguntarChatbot,
  valorarMensaje,
  listarConversaciones,
  obtenerMensajesConversacion,
  getProgreso,
  ConversacionOut,
} from "@/lib/api"

type TipoMensaje = "usuario" | "bot" | "error"
type Valoracion = "positiva" | "negativa" | null

interface Mensaje {
  id: number
  tipo: TipoMensaje
  contenido: string
  mensajeId?: number
  valoracion?: Valoracion
}

const TEMAS = [
  { emoji: "🫁", label: "Neumonía", pregunta: "¿Qué es la neumonía?" },
  { emoji: "🦠", label: "Gastroenteritis", pregunta: "¿Qué es la gastroenteritis?" },
  { emoji: "💧", label: "Inf. Urinaria", pregunta: "¿Qué es la infección urinaria?" },
  { emoji: "🩺", label: "Presión alta", pregunta: "¿Qué es la hipertensión?" },
  { emoji: "🤕", label: "Dolor de cabeza", pregunta: "¿Cuándo es peligroso el dolor de cabeza?" },
  { emoji: "🦴", label: "Lumbago", pregunta: "¿Qué es el lumbago?" },
  { emoji: "🏥", label: "Hospital", pregunta: "¿Cuál es el horario de atención del hospital?" },
  { emoji: "🧍", label: "Caídas", pregunta: "¿Qué hago si me caigo?" },
]

const SUGERENCIAS = [
  { emoji: "🏥", texto: "¿Cuál es el horario de atención del hospital?" },
  { emoji: "⚠️", texto: "¿Cuándo es peligroso el dolor de cabeza?" },
  { emoji: "🫁", texto: "¿Qué es la neumonía?" },
  { emoji: "🦴", texto: "¿Qué es el lumbago?" },
]

const SALUDO_TEXTO =
  "Hola, soy el asistente de salud del HUAP. ¿Sobre qué tema de salud te puedo ayudar hoy?"

const SALUDO: Mensaje = { id: 0, tipo: "bot", contenido: SALUDO_TEXTO }

export default function ChatbotPage() {
  const { data: session } = useSession()
  const router = useRouter()
  const [mensajes, setMensajes] = useState<Mensaje[]>([SALUDO])
  const [input, setInput] = useState("")
  const [cargando, setCargando] = useState(false)
  const [conversacionId, setConversacionId] = useState<number | null>(null)
  const [mostrarSugerencias, setMostrarSugerencias] = useState(false)
  const [mostrarHistorial, setMostrarHistorial] = useState(false)
  const [historial, setHistorial] = useState<ConversacionOut[]>([])
  const [cargandoHistorial, setCargandoHistorial] = useState(false)
  const [leyendoId, setLeyendoId] = useState<number | null>(null)

  const listaRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const speechRef = useRef<SpeechSynthesisUtterance | null>(null)

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const token = (session as any)?.accessToken as string | undefined
    const esDemo = localStorage.getItem("huap_modo_demo") === "true"

    if (token) {
      getProgreso(token).then((progreso) => {
        if (progreso && !progreso.chatbot_desbloqueado && !esDemo) {
          router.replace("/modulos")
        }
      })
    } else {
      const chatbotDesbloqueado = localStorage.getItem("huap_chatbot_desbloqueado") === "true"
      const mod2completado = localStorage.getItem("huap_mod2_completado") === "true"
      if (!chatbotDesbloqueado && !mod2completado && !esDemo) {
        router.replace("/modulos")
        return
      }
      if (!chatbotDesbloqueado && mod2completado) {
        localStorage.setItem("huap_chatbot_desbloqueado", "true")
      }
    }
  }, [router, session])

  useEffect(() => {
    if (listaRef.current) {
      listaRef.current.scrollTop = listaRef.current.scrollHeight
    }
  }, [mensajes, cargando])

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const getToken = () => (session as any)?.accessToken as string | undefined

  const enviar = useCallback(async (textoSugerido?: string) => {
    const texto = (textoSugerido ?? input).trim()
    if (!texto || cargando) return

    const token = getToken()
    if (!token) {
      setMensajes((prev) => [
        ...prev,
        { id: Date.now(), tipo: "error", contenido: "Sin sesión activa. Recarga la página." },
      ])
      return
    }

    setMostrarSugerencias(false)
    setMensajes((prev) => [...prev, { id: Date.now(), tipo: "usuario", contenido: texto }])
    if (!textoSugerido) {
      setInput("")
      if (textareaRef.current) textareaRef.current.style.height = "auto"
    }

    setCargando(true)
    try {
      const data = await preguntarChatbot(texto, conversacionId, token)
      setConversacionId(data.conversacion_id)
      setMensajes((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          tipo: "bot",
          contenido: data.respuesta,
          mensajeId: data.mensaje_id,
          valoracion: null,
        },
      ])
    } catch {
      setMensajes((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          tipo: "error",
          contenido: "No pude conectarme al servidor. Verifica tu conexión e intenta de nuevo.",
        },
      ])
    } finally {
      setCargando(false)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [input, cargando, conversacionId, session])

  function reiniciar() {
    detenerVoz()
    setMensajes([SALUDO])
    setConversacionId(null)
    setInput("")
    setMostrarSugerencias(false)
    if (textareaRef.current) textareaRef.current.style.height = "auto"
  }

  async function calificar(msg: Mensaje, val: "positiva" | "negativa") {
    if (!msg.mensajeId || msg.valoracion) return
    const token = getToken()
    if (!token) return
    setMensajes((prev) =>
      prev.map((m) => (m.id === msg.id ? { ...m, valoracion: val } : m))
    )
    await valorarMensaje(msg.mensajeId, val, token).catch(() => {})
  }

  function leerEnVoz(msg: Mensaje) {
    if (!window.speechSynthesis) return
    if (leyendoId === msg.id) {
      detenerVoz()
      return
    }
    detenerVoz()
    const utt = new SpeechSynthesisUtterance(msg.contenido)
    utt.lang = "es-CL"
    utt.rate = 0.9
    utt.onend = () => setLeyendoId(null)
    utt.onerror = () => setLeyendoId(null)
    speechRef.current = utt
    setLeyendoId(msg.id)
    window.speechSynthesis.speak(utt)
  }

  function detenerVoz() {
    if (window.speechSynthesis) window.speechSynthesis.cancel()
    setLeyendoId(null)
  }

  async function abrirHistorial() {
    const token = getToken()
    if (!token) return
    setMostrarHistorial(true)
    setCargandoHistorial(true)
    try {
      const convs = await listarConversaciones(token)
      setHistorial(convs)
    } catch {
      setHistorial([])
    } finally {
      setCargandoHistorial(false)
    }
  }

  async function cargarConversacion(conv: ConversacionOut) {
    const token = getToken()
    if (!token) return
    try {
      const msgs = await obtenerMensajesConversacion(conv.id, token)
      detenerVoz()
      setMensajes([
        SALUDO,
        ...msgs
          .filter((m) => m.tipo !== "fallback" || m.contenido.length > 0)
          .map((m, i) => ({
            id: i + 1,
            tipo: (m.tipo === "usuario" ? "usuario" : m.tipo === "bot" || m.tipo === "fallback" ? "bot" : "bot") as TipoMensaje,
            contenido: m.contenido,
            mensajeId: m.tipo !== "usuario" ? m.id : undefined,
            valoracion: m.valoracion as Valoracion,
          })),
      ])
      setConversacionId(conv.id)
      setMostrarHistorial(false)
    } catch {
      /* silencioso */
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      enviar()
    }
  }

  function autoResize(e: React.FormEvent<HTMLTextAreaElement>) {
    const t = e.currentTarget
    t.style.height = "auto"
    t.style.height = `${Math.min(t.scrollHeight, 120)}px`
  }

  const puedeEnviar = input.trim().length > 0 && !cargando
  const esPrimerMensaje = mensajes.length === 1

  return (
    <div style={{ height: "100dvh", display: "flex", flexDirection: "column", backgroundColor: "var(--huap-fondo)", overflow: "hidden" }}>
      <Header />

      {/* Aviso educativo */}
      <div style={{ backgroundColor: "#FFFBF0", borderBottom: "1px solid #F0C97A", padding: "9px 16px", flexShrink: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", maxWidth: "680px", margin: "0 auto" }}>
          <AlertTriangle size={16} color="#C47A00" strokeWidth={2.5} style={{ flexShrink: 0 }} />
          <p style={{ fontSize: "0.82rem", color: "#7a4a00", lineHeight: 1.4, margin: 0, flex: 1 }}>
            Solo información <strong>educativa</strong>, no reemplaza al médico.
          </p>
          <div style={{ display: "flex", alignItems: "center", gap: "5px", backgroundColor: "#FEE2E2", border: "1px solid #FCA5A5", borderRadius: "20px", padding: "3px 10px", flexShrink: 0 }}>
            <span style={{ fontSize: "0.75rem", color: "#B91C1C", fontWeight: 700, whiteSpace: "nowrap" }}>🚨 131</span>
          </div>
        </div>
      </div>

      {/* Área de mensajes */}
      <div ref={listaRef} style={{ flex: 1, overflowY: "auto", padding: "20px 16px", display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: "16px", width: "100%", maxWidth: "680px" }}>

          {mensajes.map((msg) => (
            <div key={msg.id}>
              <div style={{ display: "flex", justifyContent: msg.tipo === "usuario" ? "flex-end" : "flex-start", alignItems: msg.tipo === "usuario" ? "flex-end" : "flex-start", gap: "8px" }}>
                {msg.tipo !== "usuario" && (
                  <div style={{ width: 36, height: 36, borderRadius: "50%", flexShrink: 0, background: msg.tipo === "error" ? "var(--huap-rojo)" : "linear-gradient(135deg, var(--huap-azul), #3b6fd4)", display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 2px 6px rgba(26,82,160,0.25)" }}>
                    <MessageCircle size={18} color="white" strokeWidth={2} />
                  </div>
                )}
                <div style={{ maxWidth: "78%", padding: "13px 17px", borderRadius: msg.tipo === "usuario" ? "20px 20px 5px 20px" : "20px 20px 20px 5px", background: msg.tipo === "usuario" ? "linear-gradient(135deg, var(--huap-azul), #3b6fd4)" : msg.tipo === "error" ? "#FFF0F0" : "white", color: msg.tipo === "usuario" ? "white" : msg.tipo === "error" ? "var(--huap-rojo)" : "var(--huap-texto)", boxShadow: msg.tipo === "usuario" ? "0 2px 8px rgba(26,82,160,0.25)" : "0 1px 6px rgba(0,0,0,0.07)", fontSize: "1rem", lineHeight: 1.65, whiteSpace: "pre-wrap", border: msg.tipo === "bot" ? "1px solid rgba(0,0,0,0.05)" : "none" }}>
                  {msg.contenido}
                </div>
              </div>

              {/* Acciones de mensajes bot */}
              {msg.tipo === "bot" && msg.id !== 0 && (
                <div style={{ display: "flex", gap: "6px", marginLeft: "44px", marginTop: "5px", alignItems: "center" }}>
                  {/* TTS */}
                  <button
                    onClick={() => leerEnVoz(msg)}
                    title={leyendoId === msg.id ? "Detener lectura" : "Escuchar respuesta"}
                    style={{ padding: "5px 8px", borderRadius: "8px", border: "1px solid #E5E7EB", background: leyendoId === msg.id ? "#EFF5FF" : "white", cursor: "pointer", display: "flex", alignItems: "center", gap: "4px", color: leyendoId === msg.id ? "var(--huap-azul)" : "#888", fontSize: "0.75rem" }}
                  >
                    {leyendoId === msg.id ? <VolumeX size={14} /> : <Volume2 size={14} />}
                    <span style={{ display: "none" }}>Voz</span>
                  </button>

                  {/* Feedback */}
                  {msg.mensajeId && (
                    <>
                      <button
                        onClick={() => calificar(msg, "positiva")}
                        disabled={!!msg.valoracion}
                        title="Respuesta útil"
                        style={{ padding: "5px 8px", borderRadius: "8px", border: "1px solid #E5E7EB", background: msg.valoracion === "positiva" ? "#F0FDF4" : "white", cursor: msg.valoracion ? "default" : "pointer", color: msg.valoracion === "positiva" ? "#16A34A" : "#888", opacity: msg.valoracion && msg.valoracion !== "positiva" ? 0.35 : 1 }}
                      >
                        <ThumbsUp size={14} />
                      </button>
                      <button
                        onClick={() => calificar(msg, "negativa")}
                        disabled={!!msg.valoracion}
                        title="Respuesta no útil"
                        style={{ padding: "5px 8px", borderRadius: "8px", border: "1px solid #E5E7EB", background: msg.valoracion === "negativa" ? "#FFF0F0" : "white", cursor: msg.valoracion ? "default" : "pointer", color: msg.valoracion === "negativa" ? "var(--huap-rojo)" : "#888", opacity: msg.valoracion && msg.valoracion !== "negativa" ? 0.35 : 1 }}
                      >
                        <ThumbsDown size={14} />
                      </button>
                    </>
                  )}
                </div>
              )}
            </div>
          ))}

          {/* Chips de temas — solo en saludo inicial */}
          {esPrimerMensaje && !cargando && (
            <div style={{ marginLeft: "44px" }}>
              <p style={{ fontSize: "0.78rem", color: "#999", marginBottom: "8px", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.04em" }}>Elige un tema</p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "7px" }}>
                {TEMAS.map((t) => (
                  <button
                    key={t.label}
                    onClick={() => enviar(t.pregunta)}
                    style={{ padding: "7px 12px", borderRadius: "20px", border: "1.5px solid #C7D8F5", backgroundColor: "white", color: "var(--huap-azul)", fontSize: "0.84rem", fontWeight: 500, cursor: "pointer", display: "flex", alignItems: "center", gap: "5px", boxShadow: "0 1px 3px rgba(26,82,160,0.06)" }}
                    onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = "#EFF5FF"; e.currentTarget.style.borderColor = "var(--huap-azul)" }}
                    onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = "white"; e.currentTarget.style.borderColor = "#C7D8F5" }}
                  >
                    <span>{t.emoji}</span>
                    <span>{t.label}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Indicador "escribiendo..." */}
          {cargando && (
            <div style={{ display: "flex", alignItems: "flex-start", gap: "8px" }}>
              <div style={{ width: 36, height: 36, borderRadius: "50%", flexShrink: 0, background: "linear-gradient(135deg, var(--huap-azul), #3b6fd4)", display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 2px 6px rgba(26,82,160,0.25)" }}>
                <MessageCircle size={18} color="white" strokeWidth={2} />
              </div>
              <div style={{ padding: "14px 18px", backgroundColor: "white", borderRadius: "20px 20px 20px 5px", boxShadow: "0 1px 6px rgba(0,0,0,0.07)", border: "1px solid rgba(0,0,0,0.05)", display: "flex", gap: "5px", alignItems: "center" }}>
                {[0, 1, 2].map((i) => (
                  <span key={i} style={{ display: "block", width: 8, height: 8, borderRadius: "50%", backgroundColor: "#bbb", animation: `typing-bounce 1.2s ease-in-out ${i * 0.2}s infinite` }} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Barra de input */}
      <div style={{ backgroundColor: "white", borderTop: "1px solid #E5E7EB", padding: "12px 16px", paddingBottom: "calc(12px + 104px)", flexShrink: 0, boxShadow: "0 -2px 12px rgba(0,0,0,0.06)" }}>

        {/* Sugerencias — desplegables */}
        {mostrarSugerencias && !cargando && (
          <div style={{ maxWidth: "680px", margin: "0 auto 10px" }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "7px" }}>
              {SUGERENCIAS.map((s, i) => (
                <button
                  key={i}
                  onClick={() => { setMostrarSugerencias(false); enviar(s.texto) }}
                  style={{ padding: "10px 12px", borderRadius: "12px", border: "1.5px solid #C7D8F5", backgroundColor: "white", color: "var(--huap-azul)", fontSize: "0.84rem", fontWeight: 500, cursor: "pointer", textAlign: "left", lineHeight: 1.35, boxShadow: "0 1px 3px rgba(26,82,160,0.06)", display: "flex", alignItems: "flex-start", gap: "6px" }}
                  onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = "#EFF5FF"; e.currentTarget.style.borderColor = "var(--huap-azul)" }}
                  onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = "white"; e.currentTarget.style.borderColor = "#C7D8F5" }}
                >
                  <span style={{ fontSize: "0.95rem", flexShrink: 0, marginTop: "1px" }}>{s.emoji}</span>
                  <span>{s.texto}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Fila de acciones con etiquetas (Opción B) */}
        <div style={{ display: "flex", gap: "6px", maxWidth: "680px", margin: "0 auto 8px", flexWrap: "nowrap", overflowX: "auto" }}>
          <button
            onClick={abrirHistorial}
            style={{ display: "flex", alignItems: "center", gap: "5px", padding: "6px 12px", borderRadius: "20px", border: "1.5px solid #D1D5DB", background: "white", cursor: "pointer", color: "#555", fontSize: "0.82rem", fontWeight: 500, whiteSpace: "nowrap", flexShrink: 0 }}
          >
            <History size={14} />
            Historial
          </button>

          <button
            onClick={() => setMostrarSugerencias((v) => !v)}
            style={{ display: "flex", alignItems: "center", gap: "5px", padding: "6px 12px", borderRadius: "20px", border: "1.5px solid", borderColor: mostrarSugerencias ? "var(--huap-azul)" : "#D1D5DB", background: mostrarSugerencias ? "#EFF5FF" : "white", cursor: "pointer", color: mostrarSugerencias ? "var(--huap-azul)" : "#555", fontSize: "0.82rem", fontWeight: 500, whiteSpace: "nowrap", flexShrink: 0 }}
          >
            <ChevronRight size={14} style={{ transform: mostrarSugerencias ? "rotate(90deg)" : "none", transition: "transform 0.15s" }} />
            Sugerencias
          </button>

          {mensajes.length > 1 && (
            <button
              onClick={reiniciar}
              title="Nueva conversación"
              style={{ display: "flex", alignItems: "center", gap: "5px", padding: "6px 12px", borderRadius: "20px", border: "1.5px solid #D1D5DB", background: "white", cursor: "pointer", color: "#555", fontSize: "0.82rem", fontWeight: 500, whiteSpace: "nowrap", flexShrink: 0 }}
            >
              <RotateCcw size={13} />
              Nueva
            </button>
          )}
        </div>

        {/* Fila textarea + enviar */}
        <div style={{ display: "flex", gap: "8px", alignItems: "flex-end", maxWidth: "680px", margin: "0 auto" }}>
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onInput={autoResize}
            placeholder="Escribe tu pregunta…"
            rows={1}
            style={{ flex: 1, minWidth: 0, resize: "none", border: "1.5px solid #D1D5DB", borderRadius: "16px", padding: "11px 16px", fontSize: "1rem", fontFamily: "inherit", outline: "none", backgroundColor: "#F8F9FB", color: "var(--huap-texto)", lineHeight: 1.5, overflow: "hidden", transition: "border-color 0.15s, box-shadow 0.15s" }}
            onFocus={(e) => { e.currentTarget.style.borderColor = "var(--huap-azul)"; e.currentTarget.style.boxShadow = "0 0 0 3px rgba(26,82,160,0.1)" }}
            onBlur={(e) => { e.currentTarget.style.borderColor = "#D1D5DB"; e.currentTarget.style.boxShadow = "none" }}
          />
          <button
            onClick={() => enviar()}
            disabled={!puedeEnviar}
            aria-label="Enviar pregunta"
            style={{ width: 46, height: 46, borderRadius: "50%", flexShrink: 0, backgroundColor: puedeEnviar ? "var(--huap-azul)" : "#D1D5DB", border: "none", cursor: puedeEnviar ? "pointer" : "not-allowed", display: "flex", alignItems: "center", justifyContent: "center", transition: "background 0.15s", boxShadow: puedeEnviar ? "0 2px 8px rgba(26,82,160,0.3)" : "none" }}
          >
            <Send size={19} color="white" strokeWidth={2} />
          </button>
        </div>
      </div>

      {/* Drawer — historial de conversaciones */}
      {mostrarHistorial && (
        <div
          onClick={() => setMostrarHistorial(false)}
          style={{ position: "fixed", inset: 0, backgroundColor: "rgba(0,0,0,0.4)", zIndex: 300, display: "flex", justifyContent: "flex-end" }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{ width: "min(360px, 92vw)", height: "100%", backgroundColor: "white", boxShadow: "-4px 0 24px rgba(0,0,0,0.15)", display: "flex", flexDirection: "column" }}
          >
            {/* Header del drawer */}
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "20px 20px 16px", borderBottom: "1px solid #F0F0F0" }}>
              <div>
                <div style={{ fontWeight: 700, fontSize: "1.1rem", color: "var(--huap-texto)" }}>Mis conversaciones</div>
                <div style={{ fontSize: "0.8rem", color: "#999", marginTop: "2px" }}>Últimas 20</div>
              </div>
              <button onClick={() => setMostrarHistorial(false)} style={{ background: "none", border: "none", cursor: "pointer", color: "#888", padding: "4px" }}>
                <X size={20} />
              </button>
            </div>

            {/* Lista */}
            <div style={{ flex: 1, overflowY: "auto", padding: "12px 0" }}>
              {cargandoHistorial ? (
                <div style={{ padding: "40px 20px", textAlign: "center", color: "#aaa", fontSize: "0.9rem" }}>Cargando...</div>
              ) : historial.length === 0 ? (
                <div style={{ padding: "40px 20px", textAlign: "center", color: "#aaa", fontSize: "0.9rem" }}>No hay conversaciones guardadas.</div>
              ) : (
                historial.map((conv) => (
                  <button
                    key={conv.id}
                    onClick={() => cargarConversacion(conv)}
                    style={{ width: "100%", padding: "14px 20px", background: "none", border: "none", borderBottom: "1px solid #F5F5F5", cursor: "pointer", textAlign: "left", display: "flex", flexDirection: "column", gap: "4px" }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#F8FAFF")}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
                  >
                    <div style={{ fontSize: "0.82rem", color: "#999" }}>
                      {new Date(conv.fecha_inicio).toLocaleDateString("es-CL", { day: "2-digit", month: "long", year: "numeric", hour: "2-digit", minute: "2-digit" })}
                      <span style={{ marginLeft: "8px", color: "#C7D8F5", fontWeight: 600 }}>· {conv.total_mensajes} msgs</span>
                    </div>
                    <div style={{ fontSize: "0.93rem", color: "var(--huap-texto)", fontWeight: 500, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {conv.preview}
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      <style>{`
        @keyframes typing-bounce {
          0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
          40% { transform: translateY(-6px); opacity: 1; }
        }
      `}</style>
    </div>
  )
}
