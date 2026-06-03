"use client"

import type { Modulo } from "@/types"
import { Lock, CheckCircle2 } from "lucide-react"

interface ModuloCardProps {
  modulo: Modulo
}

const MODULO_COLOR: Record<number, string> = {
  1: "#2E7D46", // verde
  2: "#C45E10", // naranja
  3: "#6B3FA0", // púrpura
}

export default function ModuloCard({ modulo }: ModuloCardProps) {
  const accentColor = MODULO_COLOR[modulo.numero] ?? "#6B7280"

  return (
    <article
      style={{
        background: "#FFFFFF",
        borderRadius: "16px",
        border: "0.5px solid #E5E7EB",
        display: "flex",
        flexDirection: "row",
        overflow: "hidden",
        opacity: modulo.estado === "bloqueado" ? 0.7 : 1,
        cursor: modulo.estado !== "bloqueado" ? "pointer" : "default",
      }}
      aria-label={`Módulo ${modulo.numero}: ${modulo.titulo} — ${modulo.estado}`}
    >
      {/* Franja izquierda pegada al borde */}
      <div
        aria-hidden="true"
        style={{
          width: "6px",
          backgroundColor: accentColor,
          flexShrink: 0,
        }}
      />

      {/* Contenido con padding propio */}
      <div style={{ flex: 1, minWidth: 0, padding: "16px", display: "flex", flexDirection: "column", gap: "12px" }}>

        {/* Fila superior: ícono + textos */}
        <div style={{ display: "flex", alignItems: "flex-start", gap: "14px" }}>

          {/* Ícono circular */}
          <div
            style={{
              width: "48px",
              height: "48px",
              borderRadius: "50%",
              backgroundColor: modulo.estado === "bloqueado" ? "#F3F4F6" : accentColor,
              border: modulo.estado === "bloqueado" ? "0.5px solid #D1D5DB" : "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexShrink: 0,
            }}
            aria-hidden="true"
          >
            {modulo.estado === "bloqueado" ? (
              <Lock size={20} color="#9CA3AF" strokeWidth={2} />
            ) : (
              <span style={{ fontSize: "18px", fontWeight: 500, color: "#FFFFFF" }}>
                {modulo.numero}
              </span>
            )}
          </div>

          {/* Título y descripción */}
          <div style={{ flex: 1, minWidth: 0 }}>
            <h2
              style={{
                fontSize: "16px",
                fontWeight: 500,
                color: modulo.estado === "bloqueado" ? "#9CA3AF" : "#111827",
                margin: "0 0 4px 0",
                lineHeight: 1.3,
              }}
            >
              {modulo.titulo}
            </h2>
            <p style={{ fontSize: "13px", color: "#6B7280", margin: 0, lineHeight: 1.5 }}>
              {modulo.descripcion}
            </p>
          </div>
        </div>

        {/* Progreso o mensaje de bloqueo */}
        {modulo.estado !== "bloqueado" ? (
          <div>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "6px",
              }}
            >
              {modulo.estado === "completado" ? (
                <span
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "4px",
                    fontSize: "13px",
                    color: accentColor,
                  }}
                >
                  <CheckCircle2 size={14} strokeWidth={2.5} />
                  Completado
                </span>
              ) : (
                <span style={{ fontSize: "13px", color: "#6B7280" }}>
                  {modulo.leccionesCompletadas} de {modulo.leccionesTotales} lecciones
                </span>
              )}
              <span style={{ fontSize: "13px", fontWeight: 500, color: accentColor }}>
                {modulo.progreso}%
              </span>
            </div>

            <div
              role="progressbar"
              aria-valuenow={modulo.progreso}
              aria-valuemin={0}
              aria-valuemax={100}
              style={{
                width: "100%",
                height: "5px",
                backgroundColor: "#E5E7EB",
                borderRadius: "999px",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${modulo.progreso}%`,
                  height: "100%",
                  backgroundColor: accentColor,
                  borderRadius: "999px",
                  transition: "width 0.6s ease",
                }}
              />
            </div>
          </div>
        ) : (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              backgroundColor: "#F9FAFB",
              borderRadius: "10px",
              padding: "10px 12px",
            }}
          >
            <Lock size={16} color="#9CA3AF" strokeWidth={2} />
            <p style={{ fontSize: "13px", color: "#6B7280", margin: 0 }}>
              Completa el Módulo {modulo.numero - 1} para desbloquearlo
            </p>
          </div>
        )}
      </div>
    </article>
  )
}