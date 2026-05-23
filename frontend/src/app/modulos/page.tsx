"use client"

import { useEffect, useState } from "react"
import Header from "@/components/layout/Header"
import ModuloCard from "@/components/modulos/ModuloCard"
import type { Modulo } from "@/types"

const MODULOS_ESTATICOS = [
  {
    id: 1,
    numero: 1,
    titulo: "Entender qué es la IA",
    descripcion: "Cómo funciona, qué puede y qué no puede hacer",
    leccionesTotales: 6,
  },
  {
    id: 2,
    numero: 2,
    titulo: "Practicar con la IA",
    descripcion: "Hacer preguntas, leer respuestas, verificar",
    leccionesTotales: 6,
  },
  {
    id: 3,
    numero: 3,
    titulo: "Asistente de IA",
    descripcion: "Conversa sobre temas de salud",
    leccionesTotales: 0,
  },
]

function cargarModulos(): Modulo[] {
  const mod1completado = localStorage.getItem("huap_mod1_completado") === "true"
  const quiz1aprobado = localStorage.getItem("huap_quiz1_aprobado") === "true"
  const mod1progreso = Math.min(
    100,
    parseInt(localStorage.getItem("huap_mod1_progreso") ?? "0", 10)
  )
  const mod2progreso = Math.min(
    100,
    parseInt(localStorage.getItem("huap_mod2_progreso") ?? "0", 10)
  )

  const mod1Lecciones = Math.round((mod1progreso / 100) * MODULOS_ESTATICOS[0].leccionesTotales)
  const mod2Lecciones = Math.round((mod2progreso / 100) * MODULOS_ESTATICOS[1].leccionesTotales)

  return [
    {
      ...MODULOS_ESTATICOS[0],
      estado: mod1completado ? "completado" : "disponible",
      progreso: mod1completado ? 100 : mod1progreso,
      leccionesCompletadas: mod1completado ? MODULOS_ESTATICOS[0].leccionesTotales : mod1Lecciones,
    },
    {
      ...MODULOS_ESTATICOS[1],
      estado: mod1completado ? "disponible" : "bloqueado",
      progreso: mod1completado ? mod2progreso : 0,
      leccionesCompletadas: mod1completado ? mod2Lecciones : 0,
    },
    {
      ...MODULOS_ESTATICOS[2],
      estado: quiz1aprobado ? "disponible" : "bloqueado",
      progreso: 0,
      leccionesCompletadas: 0,
    },
  ]
}

export default function ModulosPage() {
  const [modulos, setModulos] = useState<Modulo[] | null>(null)

  useEffect(() => {
    setModulos(cargarModulos())
  }, [])

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />

      <main className="flex-1 px-5 py-8 pb-28 w-full mx-auto" style={{ maxWidth: "680px" }}>
        <div style={{ marginBottom: "32px" }}>
          <h1 style={{ color: "var(--huap-azul)" }}>Mis módulos</h1>
          <p style={{ color: "#4A4A4A", marginTop: "8px", fontSize: "18px" }}>
            Completa los módulos en orden para aprender sobre inteligencia artificial y salud.
          </p>
        </div>

        {modulos === null ? (
          // Esqueleto de carga para evitar parpadeo
          <div className="flex flex-col gap-5" aria-busy="true" aria-label="Cargando módulos">
            {[1, 2, 3].map((n) => (
              <div
                key={n}
                style={{
                  backgroundColor: "white",
                  border: "2px solid #E0E0E0",
                  borderRadius: "16px",
                  padding: "24px",
                  height: "220px",
                  opacity: 0.5,
                }}
              />
            ))}
          </div>
        ) : (
          <div className="flex flex-col gap-5">
            {modulos.map((modulo) => (
              <ModuloCard key={modulo.id} modulo={modulo} />
            ))}
          </div>
        )}
      </main>

    </div>
  )
}
