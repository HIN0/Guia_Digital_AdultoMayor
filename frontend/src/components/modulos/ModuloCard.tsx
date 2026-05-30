"use client"

import type { ReactNode } from "react"
import type { Modulo } from "@/types"
import { Lock, CheckCircle2, Brain, MessageSquare, HeartPulse } from "lucide-react"

interface ModuloCardProps {
  modulo: Modulo
}

const MODULO_ICON: Record<number, ReactNode> = {
  1: <Brain size={32} color="white" strokeWidth={1.8} />,
  2: <MessageSquare size={32} color="white" strokeWidth={1.8} />,
  3: <HeartPulse size={32} color="white" strokeWidth={1.8} />,
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
    numeroBg: "rgba(255,255,255,0.12)",
    progressTrack: "rgba(255,255,255,0.15)",
    progressFill: "rgba(255,255,255,0.5)",
  },
}

export default function ModuloCard({ modulo }: ModuloCardProps) {
  const cfg = ESTADO_CONFIG[modulo.estado]
  const moduleIcon = MODULO_ICON[modulo.numero]

  return (
    <article
      style={{
        background: cfg.gradient,
        borderRadius: "20px",
        boxShadow: modulo.estado !== "bloqueado"
          ? "0 4px 18px rgba(0,0,0,0.2)"
          : "0 2px 8px rgba(0,0,0,0.1)",
        padding: "24px",
        display: "flex",
        flexDirection: "column",
        gap: "18px",
        opacity: modulo.estado === "bloqueado" ? 0.72 : 1,
      }}
      aria-label={`Módulo ${modulo.numero}: ${modulo.titulo} — ${modulo.estado}`}
    >
      {/* Fila superior: ícono + textos + badge */}
      <div style={{ display: "flex", gap: "16px", alignItems: "flex-start" }}>

        {/* Círculo con ícono del módulo */}
        <div
          style={{
            width: "62px",
            height: "62px",
            borderRadius: "50%",
            backgroundColor: cfg.numeroBg,
            border: "2px solid rgba(255,255,255,0.25)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
          }}
          aria-hidden="true"
        >
          {modulo.estado === "bloqueado"
            ? <Lock size={30} color="rgba(255,255,255,0.75)" strokeWidth={2} />
            : (moduleIcon ?? (
                <span style={{ color: "white", fontWeight: 700, fontSize: "22px" }}>
                  {modulo.numero}
                </span>
              ))
          }
        </div>

        {/* Textos */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "5px", flexWrap: "wrap" }}>
            <span style={{
              color: "rgba(255,255,255,0.65)",
              fontSize: "13px",
              fontWeight: 700,
              textTransform: "uppercase",
              letterSpacing: "0.07em",
            }}>
              Módulo {modulo.numero}
            </span>
            {modulo.estado === "completado" && (
              <span style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "4px",
                backgroundColor: "rgba(255,255,255,0.22)",
                borderRadius: "999px",
                padding: "3px 10px",
                color: "white",
                fontSize: "13px",
                fontWeight: 700,
              }}>
                <CheckCircle2 size={14} strokeWidth={2.5} />
                Completado
              </span>
            )}
          </div>

          <h2 style={{
            color: "white",
            fontSize: "21px",
            fontWeight: 700,
            lineHeight: 1.3,
            marginBottom: "6px",
          }}>
            {modulo.titulo}
          </h2>
          <p style={{ color: "rgba(255,255,255,0.82)", fontSize: "17px", lineHeight: 1.5 }}>
            {modulo.descripcion}
          </p>
        </div>
      </div>

      {/* Progreso o mensaje de bloqueo */}
      {modulo.estado !== "bloqueado" ? (
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
            <span style={{ color: "rgba(255,255,255,0.85)", fontSize: "16px" }}>
              {modulo.leccionesCompletadas} de {modulo.leccionesTotales} lecciones
            </span>
            <span style={{ color: "white", fontSize: "16px", fontWeight: 700 }}>
              {modulo.progreso}%
            </span>
          </div>
          <div
            role="progressbar"
            aria-valuenow={modulo.progreso}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={`Progreso: ${modulo.progreso}%`}
            style={{
              width: "100%",
              height: "12px",
              backgroundColor: cfg.progressTrack,
              borderRadius: "6px",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${modulo.progreso}%`,
                height: "100%",
                backgroundColor: cfg.progressFill,
                borderRadius: "6px",
                transition: "width 0.5s ease",
              }}
            />
          </div>
        </div>
      ) : (
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          backgroundColor: "rgba(0,0,0,0.12)",
          borderRadius: "10px",
          padding: "10px 14px",
        }}>
          <Lock size={18} color="rgba(255,255,255,0.6)" strokeWidth={2} />
          <p style={{ color: "rgba(255,255,255,0.75)", fontSize: "17px", margin: 0 }}>
            Completa el Módulo {modulo.numero - 1} para desbloquearlo
          </p>
        </div>
      )}
    </article>
  )
}
