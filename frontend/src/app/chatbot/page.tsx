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
          backgroundColor: "var(--huap-ambar-claro)",
          borderBottom: "1px solid #f0c07a",
          padding: "10px 16px",
          display: "flex",
          alignItems: "center",
          gap: "10px",
          flexShrink: 0,
        }}
      >
        <AlertTriangle size={18} color="var(--huap-ambar)" strokeWidth={2} style={{ flexShrink: 0 }} />
        <p style={{ fontSize: "0.78rem", color: "#7a4a00", lineHeight: 1.4, margin: 0 }}>
          Información <strong>educativa</strong>, no reemplaza la consulta médica. Emergencias: llama al{" "}
          <strong>131</strong>.
        </p>
      </div>

      {/* Área de mensajes */}
      <div
        ref={listaRef}
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "16px",
          display: "flex",
          flexDirection: "column",
          gap: "14px",
        }}
      >
        {mensajes.map((msg) => (
          <div
            key={msg.id}
            style={{
              display: "flex",
              justifyContent: msg.tipo === "usuario" ? "flex-end" : "flex-start",
              alignItems: "flex-end",
              gap: "8px",
            }}
          >
            {/* Avatar del bot */}
            {msg.tipo !== "usuario" && (
              <div
                style={{
                  width: 34,
                  height: 34,
                  borderRadius: "50%",
                  flexShrink: 0,
                  backgroundColor:
                    msg.tipo === "error" ? "var(--huap-rojo)" : "var(--huap-azul)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <MessageCircle size={17} color="white" strokeWidth={2} />
              </div>
            )}

            {/* Burbuja */}
            <div
              style={{
                maxWidth: "78%",
                padding: "12px 16px",
                borderRadius:
                  msg.tipo === "usuario"
                    ? "18px 18px 4px 18px"
                    : "18px 18px 18px 4px",
                backgroundColor:
                  msg.tipo === "usuario"
                    ? "var(--huap-azul)"
                    : msg.tipo === "error"
                    ? "#FFEBEE"
                    : "white",
                color:
                  msg.tipo === "usuario"
                    ? "white"
                    : msg.tipo === "error"
                    ? "var(--huap-rojo)"
                    : "var(--huap-texto)",
                boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
                fontSize: "1rem",
                lineHeight: 1.6,
                whiteSpace: "pre-wrap",
              }}
            >
              {msg.contenido}
            </div>
          </div>
        ))}

        {/* Indicador "escribiendo..." */}
        {cargando && (
          <div style={{ display: "flex", alignItems: "flex-end", gap: "8px" }}>
            <div
              style={{
                width: 34,
                height: 34,
                borderRadius: "50%",
                flexShrink: 0,
                backgroundColor: "var(--huap-azul)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <MessageCircle size={17} color="white" strokeWidth={2} />
            </div>
            <div
              style={{
                padding: "14px 18px",
                backgroundColor: "white",
                borderRadius: "18px 18px 18px 4px",
                boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
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
                    backgroundColor: "#aaa",
                    animation: `typing-bounce 1.2s ease-in-out ${i * 0.2}s infinite`,
                  }}
                />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Barra de input */}
      <div
        style={{
          backgroundColor: "white",
          borderTop: "1px solid #E5E7EB",
          padding: "12px 16px",
          paddingBottom: "calc(12px + 88px)", // espacio para NavTabs fijo
          flexShrink: 0,
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
              borderRadius: "14px",
              padding: "12px 16px",
              fontSize: "1rem",
              fontFamily: "inherit",
              outline: "none",
              backgroundColor: "var(--huap-fondo)",
              color: "var(--huap-texto)",
              lineHeight: 1.5,
              overflow: "hidden",
              transition: "border-color 0.15s",
            }}
            onFocus={(e) => (e.currentTarget.style.borderColor = "var(--huap-azul)")}
            onBlur={(e) => (e.currentTarget.style.borderColor = "#D1D5DB")}
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
              transition: "background 0.15s",
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
