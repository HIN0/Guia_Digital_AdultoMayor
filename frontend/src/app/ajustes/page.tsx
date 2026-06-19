"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Header from "@/components/layout/Header"

const OPCIONES = [
  { id: "pequeño", label: "Pequeño", size: "0.78rem" },
  { id: "mediano", label: "Mediano", size: "1rem" },
  { id: "grande", label: "Grande", size: "1.22rem" },
]

const FONT_MAP: Record<string, string> = {
  pequeño: "16px",
  mediano: "18px",
  grande: "22px",
}

export default function AjustesPage() {
  const router = useRouter()
  const [tamano, setTamano] = useState("mediano")

  // Leer la preferencia guardada solo en el navegador (tras montar),
  // para no romper el prerender del build donde no existe localStorage.
  useEffect(() => {
    setTamano(localStorage.getItem("fontTamano") ?? "mediano")
  }, [])

  useEffect(() => {
    document.documentElement.style.fontSize = FONT_MAP[tamano]
  }, [tamano])

  useEffect(() => {
    function syncDesdeHeader() {
      setTamano(localStorage.getItem("fontTamano") ?? "mediano")
    }
    window.addEventListener("huap-font-change", syncDesdeHeader)
    return () => window.removeEventListener("huap-font-change", syncDesdeHeader)
  }, [])

  function handleSelect(id: string) {
    setTamano(id)
    localStorage.setItem("fontTamano", id)
  }

  return (
    <div className="min-h-screen pb-28" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />

      <main className="px-5 py-6 w-full mx-auto" style={{ maxWidth: "480px" }}>

        <button
          onClick={() => router.back()}
          style={{
            display: "inline-flex", alignItems: "center", gap: "8px",
            background: "none", border: "1.5px solid #ccc", borderRadius: "20px",
            padding: "8px 18px", cursor: "pointer", marginBottom: "24px",
            fontSize: "16px", color: "var(--huap-texto)", fontWeight: 500,
          }}
        >
          ← Volver
        </button>

        <h1 style={{ fontSize: "1.56rem", fontWeight: 700, marginBottom: "4px", color: "var(--huap-texto)" }}>
          Ajustes
        </h1>
        <p style={{ color: "#888", marginBottom: "36px", fontSize: "0.89rem" }}>
          Personaliza la aplicación a tu gusto
        </p>

        <p style={{ fontWeight: 600, fontSize: "1rem", marginBottom: "16px", color: "var(--huap-texto)" }}>
          Tamaño de letra
        </p>
        <div style={{ display: "flex", gap: "12px" }}>
          {OPCIONES.map(op => (
            <button
              key={op.id}
              onClick={() => handleSelect(op.id)}
              style={{
                flex: 1, padding: "18px 8px",
                display: "flex", flexDirection: "column", alignItems: "center", gap: "8px",
                border: tamano === op.id ? "2px solid var(--huap-azul)" : "1.5px solid #ddd",
                borderRadius: "14px", cursor: "pointer",
                backgroundColor: tamano === op.id ? "#EEF4FA" : "white",
                color: "var(--huap-texto)", transition: "all 0.15s",
              }}
            >
              <span style={{ fontSize: op.size, fontWeight: 700, lineHeight: 1, fontFamily: "inherit" }}>A</span>
              <span style={{ fontSize: "0.72rem", fontWeight: tamano === op.id ? 600 : 400 }}>
                {op.label}
              </span>
            </button>
          ))}
        </div>

      </main>
    </div>
  )
}
