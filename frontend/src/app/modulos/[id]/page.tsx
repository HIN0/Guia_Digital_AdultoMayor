"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { CheckCircle, Circle, ChevronRight } from "lucide-react"
import Header from "@/components/layout/Header"
import { getModuloDetalle, type ModuloDetalle } from "@/lib/api"

export default function ModuloDetallePage() {
  const params = useParams()
  const router = useRouter()
  const moduloId = Number(params.id as string)

  const [modulo, setModulo] = useState<ModuloDetalle | null>(null)
  const [error, setError] = useState(false)
  const [leccionesCompletadas, setLeccionesCompletadas] = useState<Set<number>>(new Set())

  useEffect(() => {
    const guardadas: number[] = JSON.parse(
      localStorage.getItem(`huap_mod${moduloId}_lecciones_completadas`) ?? "[]"
    )
    setLeccionesCompletadas(new Set(guardadas))

    getModuloDetalle(moduloId)
      .then(setModulo)
      .catch(() => setError(true))
  }, [moduloId])

  if (error) {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main className="flex-1 flex items-center justify-center px-5">
          <p style={{ color: "var(--huap-rojo)", fontSize: "18px", textAlign: "center" }}>
            No se pudo cargar el módulo. Verifica que el servidor esté activo e intenta de nuevo.
          </p>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
      <Header />
      <main className="flex-1 px-5 py-8 pb-28 w-full mx-auto" style={{ maxWidth: "680px" }}>

        {modulo === null ? (
          <div className="flex flex-col gap-4" aria-busy="true" aria-label="Cargando lecciones">
            {[1, 2, 3, 4, 5, 6].map((n) => (
              <div
                key={n}
                style={{
                  backgroundColor: "white",
                  borderRadius: "12px",
                  height: "84px",
                  opacity: 0.4,
                }}
              />
            ))}
          </div>
        ) : (
          <>
            <div style={{ marginBottom: "28px" }}>
              <button
                onClick={() => router.push("/modulos")}
                style={{
                  alignSelf: "flex-start",
                  padding: "12px 20px",
                  borderRadius: "12px",
                  border: "none",
                  backgroundColor: "var(--huap-azul)",
                  color: "white",
                  fontSize: "17px",
                  fontWeight: 600,
                  cursor: "pointer",
                  marginBottom: "16px",
                }}
              >
                ← Volver a módulos
              </button>

              <h1 style={{ color: "var(--huap-azul)" }}>
                Módulo {modulo.orden}
              </h1>
              <p style={{ color: "#4A4A4A", fontSize: "18px", marginTop: "6px" }}>
                {modulo.nombre}
              </p>
              <p style={{ color: "#888", fontSize: "16px", marginTop: "4px" }}>
                {leccionesCompletadas.size} de {modulo.lecciones.length} lecciones completadas
              </p>
            </div>

            <div className="flex flex-col gap-4">
              {modulo.lecciones.map((leccion) => {
                const completada = leccionesCompletadas.has(leccion.id)
                return (
                  <button
                    key={leccion.id}
                    onClick={() =>
                      router.push(`/modulos/${moduloId}/lecciones/${leccion.id}`)
                    }
                    style={{
                      backgroundColor: "white",
                      border: `2px solid ${completada ? "var(--huap-verde)" : "#E0E0E0"}`,
                      borderRadius: "12px",
                      padding: "18px 20px",
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: "16px",
                      textAlign: "left",
                      width: "100%",
                    }}
                  >
                    {completada ? (
                      <CheckCircle size={28} color="var(--huap-verde)" style={{ flexShrink: 0 }} />
                    ) : (
                      <Circle size={28} color="#C0C0C0" style={{ flexShrink: 0 }} />
                    )}
                    <div style={{ flex: 1 }}>
                      <p style={{ fontSize: "13px", color: "#888", marginBottom: "3px" }}>
                        Lección {leccion.orden}
                      </p>
                      <p style={{ fontSize: "18px", color: "#222", fontWeight: 600 }}>
                        {leccion.titulo}
                      </p>
                    </div>
                    <ChevronRight size={22} color="#C0C0C0" />
                  </button>
                )
              })}
            </div>
          </>
        )}
      </main>
    </div>
  )
}
