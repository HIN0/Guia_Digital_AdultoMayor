"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { CheckCircle, ChevronRight, ArrowLeft, ClipboardCheck } from "lucide-react"
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
            {/* Cabecera */}
            <div style={{ marginBottom: "28px" }}>
              <button
                onClick={() => router.push("/modulos")}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "12px 20px",
                  borderRadius: "12px",
                  border: "none",
                  backgroundColor: "var(--huap-azul)",
                  color: "white",
                  fontSize: "17px",
                  fontWeight: 600,
                  cursor: "pointer",
                  marginBottom: "20px",
                }}
              >
                <ArrowLeft size={20} />
                Volver a módulos
              </button>

              <h1 style={{ color: "var(--huap-azul)", fontSize: "28px", fontWeight: 700 }}>
                Módulo {modulo.orden}
              </h1>
              <p style={{ color: "#4A4A4A", fontSize: "19px", marginTop: "6px", fontWeight: 500 }}>
                {modulo.nombre}
              </p>

              {/* Barra de progreso */}
              {modulo.lecciones.length > 0 && (
                <div style={{ marginTop: "16px" }}>
                  <p style={{ color: "#666", fontSize: "15px", marginBottom: "8px" }}>
                    {leccionesCompletadas.size} de {modulo.lecciones.length} lecciones completadas
                  </p>
                  <div style={{
                    backgroundColor: "#E8EDF2",
                    borderRadius: "999px",
                    height: "10px",
                    overflow: "hidden",
                  }}>
                    <div style={{
                      backgroundColor: "var(--huap-verde)",
                      height: "100%",
                      borderRadius: "999px",
                      width: `${(leccionesCompletadas.size / modulo.lecciones.length) * 100}%`,
                      transition: "width 0.4s ease",
                    }} />
                  </div>
                </div>
              )}
            </div>

            {/* Botón quiz final — aparece cuando todas las lecciones están completadas */}
            {modulo.quiz_final &&
              modulo.lecciones.length > 0 &&
              leccionesCompletadas.size >= modulo.lecciones.length && (
              <button
                onClick={() => {
                  sessionStorage.setItem("huap_quiz_modulo_id", String(moduloId))
                  router.push(`/quiz/${modulo.quiz_final!.id}`)
                }}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "16px",
                  padding: "22px 20px",
                  borderRadius: "16px",
                  border: "2px solid var(--huap-verde)",
                  backgroundColor: "#F0FAF4",
                  cursor: "pointer",
                  width: "100%",
                  textAlign: "left",
                  marginBottom: "8px",
                  boxShadow: "0 2px 8px rgba(76,175,80,0.15)",
                }}
              >
                <div style={{
                  width: "52px",
                  height: "52px",
                  borderRadius: "50%",
                  backgroundColor: "var(--huap-verde)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                }}>
                  <ClipboardCheck size={28} color="white" strokeWidth={2} />
                </div>
                <div style={{ flex: 1 }}>
                  <p style={{ fontSize: "13px", color: "var(--huap-verde)", marginBottom: "3px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.04em" }}>
                    ¡Listo para el examen!
                  </p>
                  <p style={{ fontSize: "19px", color: "#1a1a1a", fontWeight: 700, lineHeight: 1.3 }}>
                    Iniciar Quiz Final del Módulo
                  </p>
                  <p style={{ fontSize: "14px", color: "#666", marginTop: "2px" }}>
                    Mínimo {modulo.quiz_final.minimo_aciertos} de {modulo.quiz_final.preguntas.length} correctas para aprobar
                  </p>
                </div>
                <ChevronRight size={26} color="var(--huap-verde)" strokeWidth={2} />
              </button>
            )}

            {/* Lista de lecciones */}
            <div className="flex flex-col gap-3">
              {modulo.lecciones.map((leccion) => {
                const completada = leccionesCompletadas.has(leccion.id)
                return (
                  <button
                    key={leccion.id}
                    onClick={() =>
                      router.push(`/modulos/${moduloId}/lecciones/${leccion.id}`)
                    }
                    style={{
                      backgroundColor: completada ? "#F0FAF4" : "white",
                      border: `2px solid ${completada ? "var(--huap-verde)" : "#E0E0E0"}`,
                      borderRadius: "16px",
                      padding: "20px 20px",
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: "16px",
                      textAlign: "left",
                      width: "100%",
                      transition: "box-shadow 0.15s ease",
                      boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
                    }}
                  >
                    {/* Círculo numerado */}
                    <div style={{
                      width: "48px",
                      height: "48px",
                      borderRadius: "50%",
                      backgroundColor: completada ? "var(--huap-verde)" : "#F0F0F0",
                      border: `2px solid ${completada ? "var(--huap-verde)" : "#D0D0D0"}`,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                    }}>
                      {completada
                        ? <CheckCircle size={26} color="white" strokeWidth={2.5} />
                        : <span style={{ fontSize: "17px", fontWeight: 700, color: "#999" }}>
                            {leccion.orden}
                          </span>
                      }
                    </div>

                    {/* Texto */}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ fontSize: "13px", color: completada ? "var(--huap-verde)" : "#999", marginBottom: "3px", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.04em" }}>
                        Lección {leccion.orden}
                      </p>
                      <p style={{ fontSize: "18px", color: completada ? "#1a1a1a" : "#333", fontWeight: 600, lineHeight: 1.3 }}>
                        {leccion.titulo}
                      </p>
                    </div>

                    <ChevronRight size={26} color={completada ? "var(--huap-verde)" : "#C0C0C0"} strokeWidth={2} />
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
