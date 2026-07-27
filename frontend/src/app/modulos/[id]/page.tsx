"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { CheckCircle, ChevronRight, ArrowLeft, Trophy, Lock } from "lucide-react"
import Header from "@/components/layout/Header"
import { getModuloDetalle, type ModuloDetalle } from "@/lib/api"

export default function ModuloDetallePage() {
  const params = useParams()
  const router = useRouter()
  const moduloId = Number(params.id as string)

  const [modulo, setModulo] = useState<ModuloDetalle | null>(null)
  const [error, setError] = useState(false)
  const [leccionesCompletadas] = useState<Set<number>>(() => {
    const guardadas: number[] = JSON.parse(
      localStorage.getItem(`huap_mod${moduloId}_lecciones_completadas`) ?? "[]"
    )
    return new Set(guardadas)
  })
  const [quizAprobado, setQuizAprobado] = useState(false)
  const [chatbotAccesible] = useState(() => {
    const desbloqueado = localStorage.getItem("huap_chatbot_desbloqueado") === "true"
    const mod2done = localStorage.getItem("huap_mod2_completado") === "true"
    return desbloqueado || mod2done
  })

  useEffect(() => {
    getModuloDetalle(moduloId)
      .then((m) => {
        setModulo(m)
        setQuizAprobado(localStorage.getItem(`huap_mod${m.orden}_completado`) === "true")
      })
      .catch(() => setError(true))
  }, [moduloId])

  if (error) {
    return (
      <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--huap-fondo)" }}>
        <Header />
        <main className="flex-1 flex items-center justify-center px-5">
          <p style={{ color: "var(--huap-rojo)", fontSize: "1rem", textAlign: "center" }}>
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
                  fontSize: "0.95rem",
                  fontWeight: 600,
                  cursor: "pointer",
                  marginBottom: "20px",
                }}
              >
                <ArrowLeft size={20} />
                Volver a módulos
              </button>

              <h1 style={{ color: "var(--huap-azul)", fontSize: "1.55rem", fontWeight: 700 }}>
                Módulo {modulo.orden}
              </h1>
              <p style={{ color: "#4A4A4A", fontSize: "1.05rem", marginTop: "6px", fontWeight: 500 }}>
                {modulo.nombre}
              </p>

              {/* Barra de progreso */}
              {modulo.lecciones.length > 0 && (() => {
                const tieneQuiz = !!modulo.quiz_final
                const total = modulo.lecciones.length + (tieneQuiz ? 1 : 0)
                const completados = leccionesCompletadas.size + (tieneQuiz && quizAprobado ? 1 : 0)
                return (
                  <div style={{ marginTop: "16px" }}>
                    <p style={{ color: "#666", fontSize: "0.85rem", marginBottom: "8px" }}>
                      {completados} de {total} {tieneQuiz ? "pasos completados" : "lecciones completadas"}
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
                        width: `${(completados / total) * 100}%`,
                        transition: "width 0.4s ease",
                      }} />
                    </div>
                  </div>
                )
              })()}
            </div>

            {/* Lista de lecciones + quiz final al final */}
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
                        : <span style={{ fontSize: "0.95rem", fontWeight: 700, color: "#999" }}>
                            {leccion.orden}
                          </span>
                      }
                    </div>

                    {/* Texto */}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ fontSize: "0.75rem", color: completada ? "var(--huap-verde)" : "#999", marginBottom: "3px", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.04em" }}>
                        Lección {leccion.orden}
                      </p>
                      <p style={{ fontSize: "1rem", color: completada ? "#1a1a1a" : "#333", fontWeight: 600, lineHeight: 1.3 }}>
                        {leccion.titulo}
                      </p>
                    </div>

                    <ChevronRight size={26} color={completada ? "var(--huap-verde)" : "#C0C0C0"} strokeWidth={2} />
                  </button>
                )
              })}

              {/* Módulo 3: pestaña de acceso al chatbot */}
              {modulo.orden === 3 && chatbotAccesible && (() => {
                const repasoHecho = modulo.lecciones.length > 0 && leccionesCompletadas.size >= modulo.lecciones.length
                return (
                  <>
                    <div style={{ display: "flex", alignItems: "center", gap: "12px", margin: "4px 0" }}>
                      <div style={{ flex: 1, height: "1px", backgroundColor: "#D0D0D0" }} />
                      <span style={{ fontSize: "0.75rem", color: "#999", fontWeight: 600, whiteSpace: "nowrap" }}>
                        ASISTENTE DE IA
                      </span>
                      <div style={{ flex: 1, height: "1px", backgroundColor: "#D0D0D0" }} />
                    </div>
                    <button
                      onClick={() => {
                        localStorage.setItem("huap_chatbot_desbloqueado", "true")
                        router.push("/chatbot")
                      }}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "16px",
                        padding: "20px",
                        borderRadius: "16px",
                        width: "100%",
                        textAlign: "left",
                        cursor: "pointer",
                        ...(repasoHecho
                          ? {
                              backgroundColor: "#F0FAF4",
                              border: "2px solid var(--huap-verde)",
                              boxShadow: "0 1px 6px rgba(76,175,80,0.12)",
                            }
                          : {
                              backgroundColor: "white",
                              border: "2px dashed var(--huap-azul)",
                              boxShadow: "0 1px 6px rgba(0,80,180,0.10)",
                            }),
                      }}
                    >
                      <div style={{
                        width: "52px",
                        height: "52px",
                        borderRadius: "50%",
                        flexShrink: 0,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        backgroundColor: repasoHecho ? "var(--huap-verde)" : "#EBF3FF",
                        border: repasoHecho ? "none" : "2px solid var(--huap-azul)",
                      }}>
                        {repasoHecho
                          ? <CheckCircle size={28} color="white" strokeWidth={2.5} />
                          : <ChevronRight size={26} color="var(--huap-azul)" strokeWidth={2.5} />
                        }
                      </div>
                      <div style={{ flex: 1 }}>
                        <p style={{
                          fontSize: "0.75rem",
                          fontWeight: 700,
                          textTransform: "uppercase",
                          letterSpacing: "0.05em",
                          marginBottom: "3px",
                          color: repasoHecho ? "var(--huap-verde)" : "var(--huap-azul)",
                        }}>
                          {repasoHecho ? "✓ Test completado" : "Disponible"}
                        </p>
                        <p style={{ fontSize: "1rem", fontWeight: 700, lineHeight: 1.3, color: "#1a1a1a" }}>
                          {repasoHecho
                            ? "¡Haz clic para ir al chatbot!"
                            : "Ir al Asistente de IA"
                          }
                        </p>
                        <p style={{ fontSize: "0.8rem", color: "#555", marginTop: "2px" }}>
                          {repasoHecho
                            ? "Completaste el repaso. El asistente te espera."
                            : "Completa el repaso de arriba para prepararte mejor."
                          }
                        </p>
                      </div>
                      <ChevronRight size={26} color={repasoHecho ? "var(--huap-verde)" : "var(--huap-azul)"} strokeWidth={2} />
                    </button>
                  </>
                )
              })()}

              {/* Quiz final — siempre visible al final de la lista */}
              {modulo.quiz_final && modulo.lecciones.length > 0 && (() => {
                const desbloqueado = leccionesCompletadas.size >= modulo.lecciones.length
                const bloqueado = !desbloqueado

                return (
                  <>
                    {/* Separador */}
                    <div style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "12px",
                      margin: "4px 0",
                    }}>
                      <div style={{ flex: 1, height: "1px", backgroundColor: "#D0D0D0" }} />
                      <span style={{ fontSize: "0.75rem", color: "#999", fontWeight: 600, whiteSpace: "nowrap" }}>
                        CUESTIONARIO FINAL
                      </span>
                      <div style={{ flex: 1, height: "1px", backgroundColor: "#D0D0D0" }} />
                    </div>

                    <button
                      disabled={bloqueado}
                      onClick={() => {
                        if (desbloqueado && !quizAprobado) {
                          sessionStorage.setItem("huap_quiz_modulo_id", String(moduloId))
                          router.push(`/quiz/${modulo.quiz_final!.id}`)
                        }
                      }}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "16px",
                        padding: "20px",
                        borderRadius: "16px",
                        width: "100%",
                        textAlign: "left",
                        // Bloqueado
                        ...(bloqueado && {
                          backgroundColor: "#F5F5F5",
                          border: "2px solid #E0E0E0",
                          cursor: "not-allowed",
                          opacity: 0.7,
                          boxShadow: "none",
                        }),
                        // Desbloqueado y pendiente
                        ...(desbloqueado && !quizAprobado && {
                          backgroundColor: "white",
                          border: "2px dashed var(--huap-azul)",
                          cursor: "pointer",
                          boxShadow: "0 1px 6px rgba(0,80,180,0.10)",
                        }),
                        // Aprobado
                        ...(quizAprobado && {
                          backgroundColor: "#F0FAF4",
                          border: "2px solid var(--huap-verde)",
                          cursor: "default",
                          boxShadow: "0 1px 6px rgba(76,175,80,0.12)",
                        }),
                      }}
                    >
                      {/* Ícono */}
                      <div style={{
                        width: "52px",
                        height: "52px",
                        borderRadius: "50%",
                        flexShrink: 0,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        ...(bloqueado && { backgroundColor: "#E8E8E8" }),
                        ...(desbloqueado && !quizAprobado && { backgroundColor: "#EBF3FF", border: "2px solid var(--huap-azul)" }),
                        ...(quizAprobado && { backgroundColor: "var(--huap-verde)" }),
                      }}>
                        {bloqueado && <Lock size={24} color="#AAAAAA" strokeWidth={2} />}
                        {desbloqueado && !quizAprobado && <Trophy size={26} color="var(--huap-azul)" strokeWidth={2} />}
                        {quizAprobado && <CheckCircle size={28} color="white" strokeWidth={2.5} />}
                      </div>

                      {/* Texto */}
                      <div style={{ flex: 1 }}>
                        <p style={{
                          fontSize: "0.75rem",
                          fontWeight: 700,
                          textTransform: "uppercase",
                          letterSpacing: "0.05em",
                          marginBottom: "3px",
                          ...(bloqueado && { color: "#BBBBBB" }),
                          ...(desbloqueado && !quizAprobado && { color: "var(--huap-azul)" }),
                          ...(quizAprobado && { color: "var(--huap-verde)" }),
                        }}>
                          {bloqueado && "Bloqueado"}
                          {desbloqueado && !quizAprobado && "Pendiente"}
                          {quizAprobado && "✓ Aprobado"}
                        </p>
                        <p style={{
                          fontSize: "1rem",
                          fontWeight: 700,
                          lineHeight: 1.3,
                          color: bloqueado ? "#AAAAAA" : "#1a1a1a",
                        }}>
                          Cuestionario Final del Módulo
                        </p>
                        <p style={{
                          fontSize: "0.8rem",
                          marginTop: "2px",
                          ...(bloqueado && { color: "#BBBBBB" }),
                          ...(desbloqueado && !quizAprobado && { color: "#555" }),
                          ...(quizAprobado && { color: "#666" }),
                        }}>
                          {bloqueado
                            ? `Completa las ${modulo.lecciones.length} lecciones para desbloquearlo`
                            : quizAprobado
                              ? "Has superado el cuestionario de este módulo"
                              : `Mínimo ${modulo.quiz_final.minimo_aciertos} de ${modulo.quiz_final.preguntas.length} correctas para aprobar`
                          }
                        </p>
                      </div>

                      {desbloqueado && !quizAprobado && (
                        <ChevronRight size={26} color="var(--huap-azul)" strokeWidth={2} />
                      )}
                    </button>
                  </>
                )
              })()}
            </div>
          </>
        )}
      </main>
    </div>
  )
}
