"use client"

import type { Modulo } from "@/types"

interface ModuloCardProps {
  modulo: Modulo
}

const ESTADO_CONFIG = {
  disponible: {
    borderColor: "#E8853A",
    numeroBg: "#E8853A",
    progressColor: "#E8853A",
    titleColor: "var(--huap-texto)",
    descColor: "#4A4A4A",
  },
  completado: {
    borderColor: "var(--huap-verde)",
    numeroBg: "var(--huap-verde)",
    progressColor: "var(--huap-verde)",
    titleColor: "var(--huap-texto)",
    descColor: "#4A4A4A",
  },
  bloqueado: {
    borderColor: "#E0E0E0",
    numeroBg: "#AAAAAA",
    progressColor: "#AAAAAA",
    titleColor: "#AAAAAA",
    descColor: "#AAAAAA",
  },
}

export default function ModuloCard({ modulo }: ModuloCardProps) {
  const cfg = ESTADO_CONFIG[modulo.estado]

  function renderStatus() {
    if (modulo.estado === "completado") {
      return (
        <span style={{ color: "var(--huap-verde)", fontSize: "18px", fontWeight: 600 }}>
          ✓ Completado
        </span>
      )
    }
    if (modulo.estado === "bloqueado") {
      return (
        <span style={{ color: "#777777", fontSize: "18px" }}>
          Completa el Módulo {modulo.numero - 1} para desbloquearlo
        </span>
      )
    }
    if (modulo.leccionesCompletadas !== undefined && modulo.leccionesTotales) {
      return (
        <span style={{ color: "#4A4A4A", fontSize: "18px" }}>
          {modulo.leccionesCompletadas} de {modulo.leccionesTotales} lecciones
        </span>
      )
    }
    return null
  }

  return (
    <article
      style={{
        backgroundColor: "white",
        borderRadius: "16px",
        borderLeft: `5px solid ${cfg.borderColor}`,
        boxShadow: "0 1px 6px rgba(0,0,0,0.07)",
        padding: "20px 20px 20px 18px",
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
              color: cfg.titleColor,
              fontSize: "22px",
              fontWeight: 700,
              lineHeight: 1.3,
              marginBottom: "6px",
            }}
          >
            {modulo.titulo}
          </h2>
          <p style={{ color: cfg.descColor, fontSize: "18px", lineHeight: 1.5 }}>
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
            backgroundColor: "#E0E0E0",
            borderRadius: "4px",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${modulo.progreso}%`,
              height: "100%",
              backgroundColor: cfg.progressColor,
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
