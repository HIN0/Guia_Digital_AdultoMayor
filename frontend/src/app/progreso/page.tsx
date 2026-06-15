"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Lock } from "lucide-react"
import Header from "@/components/layout/Header"
import { getModulos } from "@/lib/api"

const INSIGNIAS_DEF = [
  { orden: 1, nombre: "Conocedor de la IA",   descripcion: "Completaste el Módulo 1", icono: "🧠", flag: "huap_mod1_completado" },
  { orden: 2, nombre: "Practicante de la IA", descripcion: "Completaste el Módulo 2", icono: "💪", flag: "huap_mod2_completado" },
  { orden: 3, nombre: "Asistente de IA",      descripcion: "Completaste el Módulo 3", icono: "🤖", flag: "huap_chatbot_desbloqueado" },
]

const TOTALES_POR_ORDEN: Record<number, number> = { 1: 6, 2: 6, 3: 1 }
const TOTAL_LECCIONES = 13

export default function ProgresoPage() {
  const router = useRouter()
  const [insigniasGanadas, setInsigniasGanadas] = useState<Record<number, boolean>>({})
  const [leccionesCompletadas, setLeccionesCompletadas] = useState(0)

  useEffect(() => {
    const ganadas: Record<number, boolean> = {}
    for (const ins of INSIGNIAS_DEF) {
      ganadas[ins.orden] = localStorage.getItem(ins.flag) === "true"
    }
    setInsigniasGanadas(ganadas)

    getModulos()
      .then((apiModulos) => {
        let completadas = 0
        for (const m of apiModulos) {
          const guardadas: number[] = JSON.parse(
            localStorage.getItem(`huap_mod${m.id}_lecciones_completadas`) ?? "[]"
          )
          completadas += Math.min(guardadas.length, TOTALES_POR_ORDEN[m.orden] ?? 0)
        }
        setLeccionesCompletadas(completadas)
      })
      .catch(() => {
        const fallback = INSIGNIAS_DEF.filter((i) => ganadas[i.orden]).length
        setLeccionesCompletadas(fallback)
      })
  }, [])

  const pct = Math.round((leccionesCompletadas / TOTAL_LECCIONES) * 100)

  return (
    <div className="min-h-screen pb-28" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />

      <main className="px-5 py-6 w-full mx-auto" style={{ maxWidth: "480px" }}>

        <button
          onClick={() => router.back()}
          style={{
            display: "inline-flex", alignItems: "center", gap: "8px",
            background: "none", border: "1.5px solid #ccc", borderRadius: "20px",
            padding: "8px 18px", cursor: "pointer", marginBottom: "28px",
            fontSize: "16px", color: "var(--huap-texto)", fontWeight: 500,
          }}
        >
          ← Volver
        </button>

        <h1 style={{ fontSize: "1.56rem", fontWeight: 700, marginBottom: "4px", color: "var(--huap-azul)" }}>
          Mi Progreso
        </h1>
        <p style={{ color: "#888", marginBottom: "28px", fontSize: "0.89rem" }}>
          Tu avance actual en el curso
        </p>

        {/* Barra de progreso global */}
        <div style={{
          backgroundColor: "white",
          borderRadius: "16px",
          padding: "22px",
          marginBottom: "28px",
          boxShadow: "0 1px 6px rgba(0,0,0,0.06)",
          border: "1px solid #EBEBEB",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "12px" }}>
            <span style={{ fontSize: "0.95rem", color: "#444", fontWeight: 600 }}>
              {leccionesCompletadas} de {TOTAL_LECCIONES} lecciones
            </span>
            <span style={{ fontSize: "1.4rem", fontWeight: 800, color: pct === 100 ? "var(--huap-verde)" : "var(--huap-azul)" }}>
              {pct}%
            </span>
          </div>
          <div style={{ backgroundColor: "#E8EDF2", borderRadius: "999px", height: "12px", overflow: "hidden" }}>
            <div style={{
              backgroundColor: pct === 100 ? "var(--huap-verde)" : "var(--huap-azul)",
              height: "100%",
              borderRadius: "999px",
              width: `${pct}%`,
              transition: "width 0.5s ease",
              minWidth: pct > 0 ? "12px" : "0",
            }} />
          </div>
          {pct === 100 && (
            <p style={{ color: "var(--huap-verde)", fontSize: "0.88rem", fontWeight: 700, marginTop: "12px", textAlign: "center" }}>
              ✓ ¡Curso completado!
            </p>
          )}
        </div>

        {/* Insignias */}
        <p style={{ fontWeight: 700, fontSize: "1rem", marginBottom: "16px", color: "var(--huap-texto)" }}>
          Insignias ganadas
        </p>
        <div style={{ display: "flex", gap: "12px", marginBottom: "12px" }}>
          {INSIGNIAS_DEF.map((ins) => {
            const ganada = !!insigniasGanadas[ins.orden]
            return (
              <div
                key={ins.orden}
                style={{
                  flex: 1,
                  borderRadius: "14px",
                  padding: "18px 8px 14px",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: "8px",
                  border: ganada ? "2px solid #E8A000" : "1.5px solid #E0E0E0",
                  backgroundColor: ganada ? "#FFFBF0" : "#F5F5F5",
                  position: "relative",
                }}
              >
                <div style={{
                  width: "54px",
                  height: "54px",
                  borderRadius: "50%",
                  backgroundColor: ganada ? "#FFF3CD" : "#E4E4E4",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "28px",
                  position: "relative",
                  opacity: ganada ? 1 : 0.5,
                }}>
                  {ins.icono}
                  {!ganada && (
                    <div style={{
                      position: "absolute", bottom: -2, right: -2,
                      backgroundColor: "#9E9E9E", borderRadius: "50%",
                      width: "22px", height: "22px",
                      display: "flex", alignItems: "center", justifyContent: "center",
                    }}>
                      <Lock size={11} color="white" strokeWidth={2.5} />
                    </div>
                  )}
                </div>
                <p style={{
                  fontSize: "0.72rem",
                  fontWeight: ganada ? 700 : 500,
                  color: ganada ? "#B85C00" : "#AAAAAA",
                  textAlign: "center",
                  lineHeight: 1.3,
                  margin: 0,
                }}>
                  {ins.nombre}
                </p>
              </div>
            )
          })}
        </div>

      </main>
    </div>
  )
}
