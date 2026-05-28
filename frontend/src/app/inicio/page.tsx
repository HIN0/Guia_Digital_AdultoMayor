"use client"

import Image from "next/image"
import Header from "@/components/layout/Header"
import { ShieldCheck } from "lucide-react"

export default function InicioPage() {
  return (
    <div className="min-h-screen pb-28" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />

      <main className="px-5 py-6 w-full mx-auto" style={{ maxWidth: "480px" }}>

        {/* Hero */}
        <div style={{ marginBottom: "24px" }}>
          <p style={{
            color: "#E05555",
            fontSize: "0.72rem",
            fontWeight: 700,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
            marginBottom: "16px",
            lineHeight: 1.4,
            textAlign: "center",
          }}>
            Hospital de Urgencia Asistencia Pública
          </p>

          <h1 style={{ color: "var(--huap-texto)", fontSize: "2rem", fontWeight: 400, lineHeight: 1.2, marginBottom: "4px", textAlign: "left" }}>
            Bienvenido a
          </h1>
          <p style={{ color: "var(--huap-azul)", fontSize: "2.33rem", fontWeight: 800, lineHeight: 1.1, marginBottom: "20px", textAlign: "center" }}>
            IA y Salud
          </p>

          <p style={{ color: "#4A4A4A", fontSize: "1.11rem", lineHeight: 1.55 }}>
            Aprende a usar inteligencia artificial para entender información de salud de forma segura.
          </p>
        </div>

        {/* Tarjeta asistente educativo */}
        <div style={{
          backgroundColor: "var(--huap-ambar-claro)",
          borderRadius: "16px",
          padding: "16px",
          display: "flex",
          alignItems: "flex-start",
          gap: "14px",
          marginBottom: "14px",
          cursor: "default",
        }}>
          <div style={{
            width: 48, height: 48, borderRadius: "50%", flexShrink: 0,
            backgroundColor: "var(--huap-ambar)",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}>
            <ShieldCheck size={24} color="white" strokeWidth={2} />
          </div>
          <div style={{ flex: 1 }}>
            <p style={{ fontWeight: 700, fontSize: "1rem", marginBottom: "6px", color: "var(--huap-texto)" }}>
              Asistente educativo
            </p>
            <p style={{ fontSize: "1rem", color: "#4A4A4A", lineHeight: 1.5 }}>
              Esta aplicación te entrega información educativa.{" "}
              <strong>No reemplaza la consulta con tu médico o médica.</strong>
            </p>
            <p style={{ fontSize: "1rem", color: "#6B5A3E", marginTop: "6px" }}>
              Si tienes síntomas graves, acude a tu centro de salud más cercano o llama al 131.
            </p>
          </div>
        </div>

        {/* Imagen médico */}
        <div style={{ position: "relative", width: "100%", maxWidth: "280px", aspectRatio: "1/1", margin: "0 auto" }}>
          <Image
            src="/medico.svg"
            alt="Asistente de salud"
            fill
            sizes="(max-width: 480px) 60vw, 280px"
            style={{ objectFit: "contain", objectPosition: "center" }}
          />
        </div>

      </main>
    </div>
  )
}
