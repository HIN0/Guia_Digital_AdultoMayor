"use client"

import Image from "next/image"
import Header from "@/components/layout/Header"
import { ShieldCheck } from "lucide-react"

export default function InicioPage() {
  return (
    <div className="min-h-screen flex flex-col pb-28" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />

      <main className="flex-1 px-5 py-6 w-full mx-auto" style={{ maxWidth: "480px" }}>

        {/* Hero */}
        <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", marginBottom: "28px", minHeight: "180px" }}>
          <div style={{ flex: 1, paddingRight: "8px" }}>
            <h1 style={{ color: "var(--huap-texto)", fontSize: "28px", fontWeight: 400, lineHeight: 1.2, marginBottom: "16px" }}>
              Bienvenido a<br />
              <strong style={{ fontWeight: 800, fontSize: "32px" }}>IA y Salud</strong>
            </h1>

            <div style={{
              borderLeft: "3px solid var(--huap-azul)",
              paddingLeft: "10px",
              marginBottom: "16px",
              color: "#4A4A4A",
              fontSize: "18px",
              lineHeight: 1.4,
            }}>
              Hospital de Urgencia<br />Asistencia Pública
            </div>

            <p style={{ color: "#4A4A4A", fontSize: "18px", lineHeight: 1.55 }}>
              Aprende a usar la inteligencia artificial para entender información de salud de forma segura.
            </p>
          </div>

          {/* Imagen médico */}
          <div style={{ flexShrink: 0, width: "48%", maxWidth: "220px", aspectRatio: "1/1", position: "relative" }}>
            <Image
              src="/medico.svg"
              alt="Asistente de salud"
              fill
              sizes="(max-width: 480px) 48vw, 220px"
              style={{ objectFit: "contain", objectPosition: "center" }}
            />
          </div>
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
            <p style={{ fontWeight: 700, fontSize: "18px", marginBottom: "6px", color: "var(--huap-texto)" }}>
              Asistente educativo
            </p>
            <p style={{ fontSize: "18px", color: "#4A4A4A", lineHeight: 1.5 }}>
              Esta aplicación te entrega información educativa.{" "}
              <strong>No reemplaza la consulta con tu médico o médica.</strong>
            </p>
            <p style={{ fontSize: "18px", color: "#6B5A3E", marginTop: "6px" }}>
              Si tienes síntomas graves, acude a tu centro de salud más cercano o llama al 131.
            </p>
          </div>
        </div>

      </main>
    </div>
  )
}
