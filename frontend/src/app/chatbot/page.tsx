"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Lock } from "lucide-react"
import Header from "@/components/layout/Header"

export default function ChatbotPage() {
  const router = useRouter()
  const [montado, setMontado] = useState(false)
  const [desbloqueado, setDesbloqueado] = useState(false)

  useEffect(() => {
    setMontado(true)
    const completadas: number[] = JSON.parse(
      localStorage.getItem("huap_mod2_lecciones_completadas") ?? "[]"
    )
    setDesbloqueado(completadas.length > 0)
  }, [])

  const bloqueado = !montado || !desbloqueado

  return (
    <div style={{ position: "relative", minHeight: "100vh", backgroundColor: "var(--huap-fondo)" }}>
      <Header />

      {/* Mock de la UI — se difumina cuando está bloqueado */}
      <div
        style={{
          filter: bloqueado ? "blur(5px)" : "none",
          pointerEvents: "none",
          userSelect: "none",
          transition: "filter 0.3s ease",
        }}
      >
        <main style={{ maxWidth: "680px", margin: "0 auto", padding: "24px 20px 100px" }}>
          <h1 style={{ fontSize: "26px", fontWeight: 700, color: "var(--huap-azul)", marginBottom: "20px" }}>
            Asistente de salud
          </h1>

          {/* Aviso educativo */}
          <div
            style={{
              padding: "14px 16px",
              backgroundColor: "#FFFBEB",
              border: "0.5px solid #FCD34D",
              borderLeft: "4px solid #F59E0B",
              borderRadius: "12px",
              marginBottom: "16px",
            }}
          >
            <p style={{ fontSize: "15px", color: "#92400E", lineHeight: 1.6, margin: 0 }}>
              💡 <strong>Este asistente es educativo.</strong> No reemplaza la consulta con tu
              médico o médica. Si tienes síntomas graves, acude a tu centro de salud más cercano
              o llama al 131.
            </p>
          </div>

          {/* Pista */}
          <div
            style={{
              padding: "14px 16px",
              backgroundColor: "#F0FDF4",
              border: "0.5px solid #BBF7D0",
              borderLeft: "4px solid var(--huap-verde)",
              borderRadius: "12px",
              marginBottom: "24px",
            }}
          >
            <p style={{ fontSize: "15px", color: "#166534", margin: 0 }}>
              Toca una pregunta sugerida o escribe la tuya abajo
            </p>
          </div>

          {/* Burbuja del asistente */}
          <div
            style={{
              background: "#FFFFFF",
              border: "0.5px solid #E5E7EB",
              borderRadius: "16px",
              padding: "16px 20px",
              marginBottom: "24px",
            }}
          >
            <p style={{ fontSize: "16px", color: "#374151", lineHeight: 1.6, margin: 0 }}>
              Hola, estoy aquí para ayudarte a entender información sobre salud.
              ¿En qué puedo ayudarte?
            </p>
          </div>

          {/* Preguntas sugeridas */}
          <p
            style={{
              fontSize: "12px",
              color: "#9CA3AF",
              fontWeight: 600,
              letterSpacing: "0.08em",
              marginBottom: "12px",
            }}
          >
            PREGUNTAS SUGERIDAS
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "24px" }}>
            {["¿Qué es la diabetes?", "¿Cómo controlar la presión alta?"].map((q) => (
              <div
                key={q}
                style={{
                  padding: "16px",
                  borderRadius: "12px",
                  border: "1px solid #E5E7EB",
                  backgroundColor: "white",
                  fontSize: "16px",
                  color: "#374151",
                  textAlign: "center",
                }}
              >
                {q}
              </div>
            ))}
          </div>

          {/* Input falso */}
          <div
            style={{
              padding: "14px 16px",
              borderRadius: "12px",
              border: "1px solid #E5E7EB",
              backgroundColor: "white",
              color: "#9CA3AF",
              fontSize: "16px",
              marginBottom: "12px",
            }}
          >
            Escribe tu pregunta aquí...
          </div>
          <div
            style={{
              padding: "16px",
              borderRadius: "12px",
              backgroundColor: "var(--huap-verde)",
              color: "white",
              fontSize: "17px",
              fontWeight: 600,
              textAlign: "center",
            }}
          >
            Enviar pregunta
          </div>
        </main>
      </div>

      {/* Overlay de bloqueo */}
      {bloqueado && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "24px",
            backgroundColor: "rgba(249, 250, 251, 0.55)",
          }}
        >
          <div
            style={{
              background: "#FFFFFF",
              borderRadius: "16px",
              border: "0.5px solid #E5E7EB",
              overflow: "hidden",
              maxWidth: "360px",
              width: "100%",
              display: "flex",
              flexDirection: "row",
            }}
          >
            {/* Franja gris — bloqueado (igual que ModuloCard bloqueado) */}
            <div
              aria-hidden="true"
              style={{ width: "6px", backgroundColor: "#9CA3AF", flexShrink: 0 }}
            />

            <div
              style={{
                flex: 1,
                padding: "32px 24px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: "20px",
                textAlign: "center",
              }}
            >
              {/* Ícono de candado */}
              <div
                style={{
                  width: "72px",
                  height: "72px",
                  borderRadius: "50%",
                  backgroundColor: "#F3F4F6",
                  border: "0.5px solid #D1D5DB",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Lock size={32} color="#9CA3AF" strokeWidth={2} />
              </div>

              {/* Texto */}
              <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                <h2 style={{ fontSize: "18px", fontWeight: 600, color: "#111827", margin: 0 }}>
                  Contenido bloqueado
                </h2>
                <p style={{ fontSize: "15px", color: "#6B7280", lineHeight: 1.6, margin: 0 }}>
                  Completa el{" "}
                  <strong style={{ color: "#111827" }}>Módulo 2</strong> para desbloquear
                  el Asistente de salud.
                </p>
              </div>

              {/* Botón */}
              <button
                onClick={() => router.push("/modulos")}
                style={{
                  width: "100%",
                  padding: "14px",
                  borderRadius: "12px",
                  border: "none",
                  backgroundColor: "var(--huap-azul)",
                  color: "white",
                  fontSize: "16px",
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                Ir al Módulo 2
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
