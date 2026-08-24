"use client"

import Image from "next/image"
import Header from "@/components/layout/Header"
import { Lightbulb, MessageCircle } from "lucide-react"

export default function InicioPage() {
  return (
    <div className="min-h-screen pb-28" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />

      <main className="px-5 py-6 w-full mx-auto" style={{ maxWidth: "480px" }}>

        {/* Hero — texto izquierda, médico derecha */}
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "28px" }}>

          {/* Bloque de texto */}
          <div style={{ flex: 1, minWidth: 0 }}>
            <h1 style={{
              color: "#111827",
              fontSize: "2rem",
              fontWeight: 400,
              lineHeight: 1.15,
              margin: "0 0 2px 0",
            }}>
              Bienvenido a
            </h1>
            <p style={{
              color: "var(--huap-azul)",
              fontSize: "2.4rem",
              fontWeight: 800,
              lineHeight: 1.1,
              margin: "0 0 16px 0",
            }}>
              IA y Salud
            </p>

            {/* Institución con borde rojo */}
            <div style={{ borderLeft: "3px solid #E05555", paddingLeft: "10px", marginBottom: "14px" }}>
              <p style={{ fontSize: "0.9rem", color: "#4A4A4A", lineHeight: 1.4, margin: 0, fontWeight: 500 }}>
                Hospital de Urgencia<br />Asistencia Pública
              </p>
            </div>

            <p style={{ color: "#6B7280", fontSize: "0.95rem", lineHeight: 1.55, margin: 0 }}>
              Aprende a usar la inteligencia artificial para entender información de salud de forma segura.
            </p>
          </div>

          {/* Ilustración médico */}
          <div style={{ position: "relative", width: "155px", height: "175px", flexShrink: 0 }}>
            <Image
              src="/medico.svg"
              alt="Asistente de salud"
              fill
              sizes="155px"
              style={{ objectFit: "contain", objectPosition: "center bottom" }}
            />
          </div>
        </div>

        {/* Tarjeta informativa */}
        <div
          style={{
            width: "100%",
            background: "white",
            borderRadius: "20px",
            overflow: "hidden",
            boxShadow: "0 8px 32px rgba(0,0,0,0.10), 0 2px 8px rgba(0,0,0,0.06)",
          }}
        >
          {/* Sección superior: ámbar */}
          <div style={{ display: "flex" }}>
            <div aria-hidden="true" style={{ width: "6px", backgroundColor: "#F59E0B", flexShrink: 0 }} />
            <div style={{
              flex: 1,
              display: "flex",
              alignItems: "flex-start",
              gap: "14px",
              padding: "18px 16px",
              backgroundColor: "#FFFBEB",
            }}>
              <div style={{
                width: 48, height: 48, borderRadius: "50%", flexShrink: 0,
                backgroundColor: "#F59E0B",
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>
                <Lightbulb size={24} color="white" strokeWidth={2} />
              </div>
              <div style={{ flex: 1 }}>
                <p style={{ fontWeight: 700, fontSize: "1rem", margin: "0 0 5px 0", color: "#78350F" }}>
                  Asistente educativo
                </p>
                <p style={{ fontSize: "0.93rem", color: "#92400E", lineHeight: 1.5, margin: 0 }}>
                  Esta aplicación te entrega información educativa.{" "}
                  <strong>No reemplaza la consulta con tu médico o médica.</strong>
                  {" "}Si tienes síntomas graves, acude a tu centro de salud más cercano o llama al 131.
                </p>
              </div>
            </div>
          </div>

          {/* Separador */}
          <div style={{ height: "0.5px", backgroundColor: "#E5E7EB" }} />

          {/* Sección inferior: azul */}
          <div style={{ display: "flex" }}>
            <div aria-hidden="true" style={{ width: "6px", backgroundColor: "var(--huap-azul)", flexShrink: 0 }} />
            <div style={{
              flex: 1,
              display: "flex",
              alignItems: "center",
              gap: "14px",
              padding: "18px 16px",
              backgroundColor: "#EFF5FF",
            }}>
              <div style={{
                width: 48, height: 48, borderRadius: "50%", flexShrink: 0,
                backgroundColor: "var(--huap-azul)",
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>
                <MessageCircle size={24} color="white" strokeWidth={2} />
              </div>
              <div style={{ flex: 1 }}>
                <p style={{ fontWeight: 700, fontSize: "1rem", margin: "0 0 3px 0", color: "#1e3a5f" }}>
                  Solo temas de salud del HUAP
                </p>
                <p style={{ fontSize: "0.93rem", color: "#374151", lineHeight: 1.4, margin: 0 }}>
                  Responde preguntas sobre enfermedades, síntomas y servicios del hospital validadas por profesionales.
                </p>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>
  )
}
