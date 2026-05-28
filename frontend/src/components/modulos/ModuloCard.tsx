"use client"

import type { Modulo } from "@/types"

interface ModuloCardProps {
  modulo: Modulo
}

const ESTADO_CONFIG = {
  disponible: {
    gradient: "linear-gradient(145deg, #1E5C8A 0%, #1B4F7A 100%)",
    numeroBg: "rgba(255,255,255,0.2)",
    progressTrack: "rgba(255,255,255,0.2)",
    progressFill: "rgba(255,255,255,0.85)",
  },
  completado: {
    gradient: "linear-gradient(145deg, #2D7A47 0%, #1E5530 100%)",
    numeroBg: "rgba(255,255,255,0.2)",
    progressTrack: "rgba(255,255,255,0.2)",
    progressFill: "rgba(255,255,255,0.85)",
  },
  bloqueado: {
    gradient: "linear-gradient(145deg, #6B7280 0%, #4B5563 100%)",
    numeroBg: "rgba(255,255,255,0.15)",
    progressTrack: "rgba(255,255,255,0.15)",
    progressFill: "rgba(255,255,255,0.5)",
  },
}

export default function ModuloCard({ modulo }: ModuloCardProps) {
  const cfg = ESTADO_CONFIG[modulo.estado]

  function renderStatus() {
    if (modulo.estado === "completado") {
      return (
        <span style={{ color: "rgba(255,255,255,0.95)", fontSize: "18px", fontWeight: 600 }}>
          ✓ Completado
        </span>
      )
    }
    if (modulo.estado === "bloqueado") {
      return (
        <span style={{ color: "rgba(255,255,255,0.7)", fontSize: "18px" }}>
          Completa el Módulo {modulo.numero - 1} para desbloquearlo
        </span>
      )
    }
    if (modulo.leccionesCompletadas !== undefined && modulo.leccionesTotales) {
      return (
        <span style={{ color: "rgba(255,255,255,0.85)", fontSize: "18px" }}>
          {modulo.leccionesCompletadas} de {modulo.leccionesTotales} lecciones
        </span>
      )
    }
    return null
  }

  return (
    <article
      style={{
        background: cfg.gradient,
        borderRadius: "16px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.15)",
        padding: "20px 20px 20px 20px",
        display: "flex",
        flexDirection: "column",
        gap: "14px",
        opacity: modulo.estado === "bloqueado" ? 0.8 : 1,
      }}
      aria-label={`Módulo ${modulo.numero}: ${modulo.titulo} — ${modulo.estado}`}
    >
      {/* Número + título + descripción en fila */}
      <div style={{ display: "flex", gap: "14px", alignItems: "flex-start" }}>
        <div
          style={{
            width: "48px",
            height: "48px",
            borderRadius: "50%",
            backgroundColor: cfg.numeroBg,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "white",
            fontWeight: 700,
            fontSize: "22px",
            flexShrink: 0,
          }}
          aria-hidden="true"
        >
          {modulo.numero}
        </div>

        <div>
          <h2
            style={{
              color: "white",
              fontSize: "22px",
              fontWeight: 700,
              lineHeight: 1.3,
              marginBottom: "6px",
            }}
          >
            {modulo.titulo}
          </h2>
          <p style={{ color: "rgba(255,255,255,0.85)", fontSize: "18px", lineHeight: 1.5 }}>
            {modulo.descripcion}
          </p>
        </div>
      </div>

      {/* Barra de progreso (solo si no está bloqueado) */}
      {modulo.estado !== "bloqueado" && (
        <div
          role="progressbar"
          aria-valuenow={modulo.progreso}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={`Progreso del módulo: ${modulo.progreso}%`}
          style={{
            width: "100%",
            height: "8px",
            backgroundColor: cfg.progressTrack,
            borderRadius: "4px",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${modulo.progreso}%`,
              height: "100%",
              backgroundColor: cfg.progressFill,
              borderRadius: "4px",
              transition: "width 0.4s ease",
            }}
          />
        </div>
      )}

      {/* Texto de estado */}
      {renderStatus()}
    </article>
  )
}
