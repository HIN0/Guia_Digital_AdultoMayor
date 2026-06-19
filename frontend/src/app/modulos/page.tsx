"use client"

import { useEffect, useState } from "react"
import { useSession } from "next-auth/react"
import Link from "next/link"
import Header from "@/components/layout/Header"
import ModuloCard from "@/components/modulos/ModuloCard"
import { getModulos, getProgreso, sincronizarLocalStorage, type ModuloResumen, type ResumenProgreso } from "@/lib/api"
import type { Modulo } from "@/types"

const DISPLAY: Record<number, { titulo: string; descripcion: string; leccionesTotales: number; tieneQuiz?: boolean }> = {
  1: { titulo: "Entender qué es la IA",   descripcion: "Cómo funciona, qué puede y qué no puede hacer", leccionesTotales: 7, tieneQuiz: true },
  2: { titulo: "Practicar con la IA",     descripcion: "Hacer preguntas, leer respuestas, verificar",   leccionesTotales: 7, tieneQuiz: true },
  3: { titulo: "Asistente de IA",         descripcion: "Conversa sobre temas de salud",                 leccionesTotales: 1 },
}

function construirDesdeBackend(apiModulos: ModuloResumen[], progreso: ResumenProgreso): Modulo[] {
  return apiModulos.map((m) => {
    const display = DISPLAY[m.orden] ?? { titulo: m.nombre, descripcion: "", leccionesTotales: 0 }
    const estado = progreso.modulos.find(e => e.modulo_id === m.id)
    const { leccionesTotales, tieneQuiz } = { tieneQuiz: false, ...display }

    if (!estado) {
      return {
        id: m.id, numero: m.orden, ...display,
        estado: "bloqueado" as const, progreso: 0, leccionesCompletadas: 0,
      }
    }

    const leccionesMax = tieneQuiz ? leccionesTotales - 1 : leccionesTotales
    const leccionesCount = Math.min(estado.lecciones_completadas.length, leccionesMax)
    const completadas = leccionesCount + (tieneQuiz && estado.completado ? 1 : 0)
    const pct = estado.completado ? 100 : leccionesTotales > 0 ? Math.round((completadas / leccionesTotales) * 100) : 0

    return {
      id: m.id, numero: m.orden, ...display,
      estado: estado.completado ? "completado" : estado.desbloqueado ? "disponible" : "bloqueado",
      progreso: pct,
      leccionesCompletadas: estado.completado ? leccionesTotales : completadas,
    }
  })
}

function construirDesdeLocalStorage(apiModulos: ModuloResumen[]): Modulo[] {
  const mod1completado = localStorage.getItem("huap_mod1_completado") === "true"
  const mod2completado = localStorage.getItem("huap_mod2_completado") === "true"
  const esDemo = localStorage.getItem("huap_modo_demo") === "true"

  return apiModulos.map((m) => {
    const display = DISPLAY[m.orden] ?? { titulo: m.nombre, descripcion: "", leccionesTotales: 0 }
    const { leccionesTotales, tieneQuiz } = { tieneQuiz: false, ...display }
    const guardadas: number[] = JSON.parse(localStorage.getItem(`huap_mod${m.id}_lecciones_completadas`) ?? "[]")
    const leccionesMax = tieneQuiz ? leccionesTotales - 1 : leccionesTotales
    const leccionesCount = Math.min(guardadas.length, leccionesMax)

    if (m.orden === 1) {
      const completadas = leccionesCount + (mod1completado ? 1 : 0)
      const progreso = leccionesTotales > 0 ? Math.round((completadas / leccionesTotales) * 100) : 0
      return {
        id: m.id, numero: m.orden, ...display,
        estado: mod1completado ? "completado" : "disponible",
        progreso: mod1completado ? 100 : progreso,
        leccionesCompletadas: mod1completado ? leccionesTotales : completadas,
      }
    }
    if (m.orden === 2) {
      const desbloqueado = mod1completado || esDemo
      const completadas = desbloqueado ? leccionesCount + (mod2completado ? 1 : 0) : 0
      const progreso = desbloqueado && leccionesTotales > 0 ? Math.round((completadas / leccionesTotales) * 100) : 0
      return {
        id: m.id, numero: m.orden, ...display,
        estado: mod2completado ? "completado" : desbloqueado ? "disponible" : "bloqueado",
        progreso: mod2completado ? 100 : desbloqueado ? progreso : 0,
        leccionesCompletadas: mod2completado ? leccionesTotales : desbloqueado ? completadas : 0,
      }
    }
    const desbloqueado = mod2completado || esDemo
    const completadas = leccionesCount
    const progreso = leccionesTotales > 0 ? Math.round((completadas / leccionesTotales) * 100) : 0
    const repasoCompletado = completadas >= 1
    return {
      id: m.id, numero: m.orden, ...display,
      estado: repasoCompletado ? "completado" : desbloqueado ? "disponible" : "bloqueado",
      progreso: repasoCompletado ? 100 : desbloqueado ? progreso : 0,
      leccionesCompletadas: repasoCompletado ? 1 : desbloqueado ? completadas : 0,
    }
  })
}

export default function ModulosPage() {
  const { data: session } = useSession()
  const [modulos, setModulos] = useState<Modulo[] | null>(null)

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const token = (session as any)?.accessToken as string | undefined

    const esDemo = localStorage.getItem("huap_modo_demo") === "true"

    getModulos()
      .then(async (apiModulos) => {
        if (token && !esDemo) {
          const progreso = await getProgreso(token)
          if (progreso && progreso.modulos.length > 0) {
            sincronizarLocalStorage(progreso, apiModulos.map(m => m.id))
            setModulos(construirDesdeBackend(apiModulos, progreso))
            return
          }
        }
        setModulos(construirDesdeLocalStorage(apiModulos))
      })
      .catch(() => setModulos([]))
  }, [session])

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />

      <main className="flex-1 px-5 py-8 pb-28 w-full mx-auto" style={{ maxWidth: "680px" }}>
        <div style={{ marginBottom: "36px" }}>
          <h1 style={{ color: "var(--huap-azul)", fontSize: "1.75rem", fontWeight: 800, lineHeight: 1.2 }}>
            Mis módulos
          </h1>
          <p style={{ color: "#555", marginTop: "10px", fontSize: "1rem", lineHeight: 1.6 }}>
            Completa los módulos en orden para aprender sobre inteligencia artificial y salud.
          </p>
        </div>

        {modulos === null ? (
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
                <Link
                  key={modulo.id}
                  href={`/modulos/${modulo.id}`}
                  style={{ textDecoration: "none" }}
                >
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
