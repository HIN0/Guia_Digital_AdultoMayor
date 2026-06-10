"use client"

import { useState, useEffect, useRef } from "react"
import { useSession } from "next-auth/react"
import Header from "@/components/layout/Header"
import { MessageCircle, Send, AlertTriangle } from "lucide-react"
import { preguntarChatbot } from "@/lib/api"

type TipoMensaje = "usuario" | "bot" | "error"

interface Mensaje {
  id: number
  tipo: TipoMensaje
  contenido: string
}

const SALUDO: Mensaje = {
  id: 0,
  tipo: "bot",
  contenido:
    "Hola, soy el asistente de salud del HUAP. Puedo responder preguntas sobre diabetes, síntomas, causas y cómo cuidar tu salud. ¿En qué te puedo ayudar hoy?",
}

export default function ChatbotPage() {
  const { data: session } = useSession()
  const [mensajes, setMensajes] = useState<Mensaje[]>([SALUDO])
  const [input, setInput] = useState("")
  const [cargando, setCargando] = useState(false)
  const [conversacionId, setConversacionId] = useState<number | null>(null)
  const listaRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (listaRef.current) {
      listaRef.current.scrollTop = listaRef.current.scrollHeight
    }
  }, [mensajes, cargando])

  async function enviar() {
    const texto = input.trim()
    if (!texto || cargando) return

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const token = (session as any)?.accessToken as string | undefined
    if (!token) {
      setMensajes((prev) => [
        ...prev,
        { id: Date.now(), tipo: "error", contenido: "Sin sesión activa. Recarga la página." },
      ])
      return
    }

    setMensajes((prev) => [...prev, { id: Date.now(), tipo: "usuario", contenido: texto }])
    setInput("")

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
    }

    setCargando(true)
    try {
      const data = await preguntarChatbot(texto, conversacionId, token)
      setConversacionId(data.conversacion_id)
      setMensajes((prev) => [
        ...prev,
        { id: Date.now() + 1, tipo: "bot", contenido: data.respuesta },
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

  return (
    <div
      style={{
        height: "100dvh",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "var(--huap-fondo)",
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <Header />

      {/* Aviso educativo */}
      <div
        style={{
          backgroundColor: "#FFFBF0",
          borderBottom: "1px solid #F0C97A",
          padding: "9px 16px",
          flexShrink: 0,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            maxWidth: "680px",
            margin: "0 auto",
          }}
        >
          <AlertTriangle size={16} color="#C47A00" strokeWidth={2.5} style={{ flexShrink: 0 }} />
          <p style={{ fontSize: "0.82rem", color: "#7a4a00", lineHeight: 1.4, margin: 0, flex: 1 }}>
            Solo información <strong>educativa</strong>, no reemplaza al médico.
          </p>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "5px",
              backgroundColor: "#FEE2E2",
              border: "1px solid #FCA5A5",
              borderRadius: "20px",
              padding: "3px 10px",
              flexShrink: 0,
            }}
          >
            <span style={{ fontSize: "0.75rem", color: "#B91C1C", fontWeight: 700, whiteSpace: "nowrap" }}>
              🚨 131
            </span>
          </div>
        </div>
      </div>

      {/* Área de mensajes */}
      <div
        ref={listaRef}
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "20px 16px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "16px",
            width: "100%",
            maxWidth: "680px",
          }}
        >
        {mensajes.map((msg) => (
          <div
            key={msg.id}
            style={{
              display: "flex",
              justifyContent: msg.tipo === "usuario" ? "flex-end" : "flex-start",
              alignItems: msg.tipo === "usuario" ? "flex-end" : "flex-start",
              gap: "8px",
            }}
          >
            {/* Avatar del bot */}
            {msg.tipo !== "usuario" && (
              <div
                style={{
                  width: 36,
                  height: 36,
                  borderRadius: "50%",
                  flexShrink: 0,
                  background:
                    msg.tipo === "error"
                      ? "var(--huap-rojo)"
                      : "linear-gradient(135deg, var(--huap-azul), #3b6fd4)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: "0 2px 6px rgba(26,82,160,0.25)",
                }}
              >
                <MessageCircle size={18} color="white" strokeWidth={2} />
              </div>
            )}

            {/* Burbuja */}
            <div
              style={{
                maxWidth: "78%",
                padding: "13px 17px",
                borderRadius:
                  msg.tipo === "usuario"
                    ? "20px 20px 5px 20px"
                    : "20px 20px 20px 5px",
                background:
                  msg.tipo === "usuario"
                    ? "linear-gradient(135deg, var(--huap-azul), #3b6fd4)"
                    : msg.tipo === "error"
                    ? "#FFF0F0"
                    : "white",
                color:
                  msg.tipo === "usuario"
                    ? "white"
                    : msg.tipo === "error"
                    ? "var(--huap-rojo)"
                    : "var(--huap-texto)",
                boxShadow:
                  msg.tipo === "usuario"
                    ? "0 2px 8px rgba(26,82,160,0.25)"
                    : "0 1px 6px rgba(0,0,0,0.07)",
                fontSize: "1rem",
                lineHeight: 1.65,
                whiteSpace: "pre-wrap",
                border: msg.tipo === "bot" ? "1px solid rgba(0,0,0,0.05)" : "none",
              }}
            >
              {msg.contenido}
            </div>
          </div>
        ))}

        {/* Indicador "escribiendo..." */}
        {cargando && (
          <div style={{ display: "flex", alignItems: "flex-start", gap: "8px" }}>
            <div
              style={{
                width: 36,
                height: 36,
                borderRadius: "50%",
                flexShrink: 0,
                background: "linear-gradient(135deg, var(--huap-azul), #3b6fd4)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 2px 6px rgba(26,82,160,0.25)",
              }}
            >
              <MessageCircle size={18} color="white" strokeWidth={2} />
            </div>
            <div
              style={{
                padding: "14px 18px",
                backgroundColor: "white",
                borderRadius: "20px 20px 20px 5px",
                boxShadow: "0 1px 6px rgba(0,0,0,0.07)",
                border: "1px solid rgba(0,0,0,0.05)",
                display: "flex",
                gap: "5px",
                alignItems: "center",
              }}
            >
              {[0, 1, 2].map((i) => (
                <span
                  key={i}
                  style={{
                    display: "block",
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    backgroundColor: "#bbb",
                    animation: `typing-bounce 1.2s ease-in-out ${i * 0.2}s infinite`,
                  }}
                />
              ))}
            </div>
          </div>
        )}
        </div>
      </div>

      {/* Barra de input */}
      <div
        style={{
          backgroundColor: "white",
          borderTop: "1px solid #E5E7EB",
          padding: "12px 16px",
          paddingBottom: "calc(12px + 104px)",
          flexShrink: 0,
          boxShadow: "0 -2px 12px rgba(0,0,0,0.06)",
        }}
      >
        <div
          style={{
            display: "flex",
            gap: "10px",
            alignItems: "flex-end",
            maxWidth: "680px",
            margin: "0 auto",
          }}
        >
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onInput={autoResize}
            placeholder="Escribe tu pregunta…"
            rows={1}
            style={{
              flex: 1,
              resize: "none",
              border: "1.5px solid #D1D5DB",
              borderRadius: "16px",
              padding: "12px 16px",
              fontSize: "1rem",
              fontFamily: "inherit",
              outline: "none",
              backgroundColor: "#F8F9FB",
              color: "var(--huap-texto)",
              lineHeight: 1.5,
              overflow: "hidden",
              transition: "border-color 0.15s, box-shadow 0.15s",
            }}
            onFocus={(e) => {
              e.currentTarget.style.borderColor = "var(--huap-azul)"
              e.currentTarget.style.boxShadow = "0 0 0 3px rgba(26,82,160,0.1)"
            }}
            onBlur={(e) => {
              e.currentTarget.style.borderColor = "#D1D5DB"
              e.currentTarget.style.boxShadow = "none"
            }}
          />
          <button
            onClick={enviar}
            disabled={!puedeEnviar}
            aria-label="Enviar pregunta"
            style={{
              width: 48,
              height: 48,
              borderRadius: "50%",
              flexShrink: 0,
              backgroundColor: puedeEnviar ? "var(--huap-azul)" : "#D1D5DB",
              border: "none",
              cursor: puedeEnviar ? "pointer" : "not-allowed",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              transition: "background 0.15s, transform 0.1s",
              boxShadow: puedeEnviar ? "0 2px 8px rgba(26,82,160,0.3)" : "none",
            }}
          >
            <Send size={20} color="white" strokeWidth={2} />
          </button>
        </div>
      </div>

      <style>{`
        @keyframes typing-bounce {
          0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
          40% { transform: translateY(-6px); opacity: 1; }
        }
      `}</style>
    </div>
  )
}
