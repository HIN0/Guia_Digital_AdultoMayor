"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import Header from "@/components/layout/Header"
import ModuloCard from "@/components/modulos/ModuloCard"
import { getModulos, type ModuloResumen } from "@/lib/api"
import type { Modulo } from "@/types"

// Datos de display estáticos indexados por orden (1, 2, 3)
const DISPLAY: Record<number, { titulo: string; descripcion: string; leccionesTotales: number }> = {
  1: { titulo: "Entender qué es la IA",   descripcion: "Cómo funciona, qué puede y qué no puede hacer", leccionesTotales: 6 },
  2: { titulo: "Practicar con la IA",     descripcion: "Hacer preguntas, leer respuestas, verificar",   leccionesTotales: 6 },
  3: { titulo: "Asistente de IA",         descripcion: "Conversa sobre temas de salud",                 leccionesTotales: 0 },
}

function construirModulos(apiModulos: ModuloResumen[]): Modulo[] {
  const mod1completado = localStorage.getItem("huap_mod1_completado") === "true"
  const quiz1aprobado  = localStorage.getItem("huap_quiz1_aprobado")  === "true"

  return apiModulos.map((m) => {
    const display = DISPLAY[m.orden] ?? { titulo: m.nombre, descripcion: "", leccionesTotales: 0 }
    const leccionesTotales = display.leccionesTotales
    // Usa el ID real del módulo en BD para leer el progreso guardado por la página de lecciones
    const guardadas: number[] = JSON.parse(localStorage.getItem(`huap_mod${m.id}_lecciones_completadas`) ?? "[]")
    const completadas = guardadas.length
    const progreso = leccionesTotales > 0 ? Math.round((completadas / leccionesTotales) * 100) : 0

    if (m.orden === 1) {
      return {
        id: m.id, numero: m.orden, ...display,
        estado: mod1completado ? "completado" : "disponible",
        progreso: mod1completado ? 100 : progreso,
        leccionesCompletadas: mod1completado ? leccionesTotales : completadas,
      }
    }
    if (m.orden === 2) {
      return {
        id: m.id, numero: m.orden, ...display,
        estado: mod1completado ? "disponible" : "bloqueado",
        progreso: mod1completado ? progreso : 0,
        leccionesCompletadas: mod1completado ? completadas : 0,
      }
    }
    return {
      id: m.id, numero: m.orden, ...display,
      estado: quiz1aprobado ? "disponible" : "bloqueado",
      progreso: 0,
      leccionesCompletadas: 0,
    }
  })
}

export default function ModulosPage() {
  const [modulos, setModulos] = useState<Modulo[] | null>(null)

  useEffect(() => {
    getModulos()
      .then((apiModulos) => setModulos(construirModulos(apiModulos)))
      .catch(() => setModulos([]))  // si el back no responde, muestra lista vacía
  }, [])

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />

      <main className="flex-1 px-5 py-8 pb-28 w-full mx-auto" style={{ maxWidth: "680px" }}>
        <div style={{ marginBottom: "36px" }}>
          <h1 style={{ color: "var(--huap-azul)", fontSize: "32px", fontWeight: 800, lineHeight: 1.2 }}>
            Mis módulos
          </h1>
          <p style={{ color: "#555", marginTop: "10px", fontSize: "18px", lineHeight: 1.6 }}>
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
            {modulos.map((modulo) =>
              modulo.estado !== "bloqueado" ? (
                <Link key={modulo.id} href={`/modulos/${modulo.id}`} style={{ textDecoration: "none" }}>
                  <ModuloCard modulo={modulo} />
                </Link>
              ) : (
                <ModuloCard key={modulo.id} modulo={modulo} />
              )
            )}
          </div>
        )}
      </main>

    </div>
  )
}
