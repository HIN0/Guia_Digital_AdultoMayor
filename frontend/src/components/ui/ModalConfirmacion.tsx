"use client"

import { useEffect, useRef, type ReactNode } from "react"
import { createPortal } from "react-dom"

interface Props {
  abierto: boolean
  titulo: string
  mensaje?: string
  textoConfirmar?: string
  textoCancelar?: string
  /** "peligro" pinta la acción principal en rojo (cerrar sesión, eliminar). */
  tono?: "peligro" | "normal"
  icono?: ReactNode
  onConfirmar: () => void
  onCancelar: () => void
}

/**
 * Diálogo de confirmación con el diseño de la plataforma, en reemplazo de
 * window.confirm(), que aparece como una caja gris del navegador con el texto
 * "localhost:3000 dice" y letra chica.
 *
 * Pensado para adultos mayores: texto grande, botones altos y separados, y la
 * acción destructiva NO es la que queda enfocada al abrir.
 */
export default function ModalConfirmacion({
  abierto,
  titulo,
  mensaje,
  textoConfirmar = "Sí, continuar",
  textoCancelar = "Cancelar",
  tono = "normal",
  icono,
  onConfirmar,
  onCancelar,
}: Props) {
  const cancelarRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (!abierto) return

    // Escape cancela: es la salida que el usuario espera de cualquier diálogo.
    function alPresionarTecla(e: KeyboardEvent) {
      if (e.key === "Escape") onCancelar()
    }
    document.addEventListener("keydown", alPresionarTecla)

    // Se bloquea el scroll del fondo para que el diálogo no se pueda perder.
    const overflowPrevio = document.body.style.overflow
    document.body.style.overflow = "hidden"

    // El foco parte en Cancelar, no en la acción destructiva.
    cancelarRef.current?.focus()

    return () => {
      document.removeEventListener("keydown", alPresionarTecla)
      document.body.style.overflow = overflowPrevio
    }
  }, [abierto, onCancelar])

  // createPortal necesita document, que no existe al renderizar en el servidor.
  // El diálogo siempre se abre por un clic, así que en el servidor nunca llega
  // hasta aquí con abierto=true.
  if (!abierto || typeof document === "undefined") return null

  const colorAccion = tono === "peligro" ? "var(--huap-rojo)" : "var(--huap-azul)"

  return createPortal(
    <div
      onClick={onCancelar}
      style={{
        position: "fixed",
        inset: 0,
        // Por encima del header y de NavTabs, ambos en z-index 100.
        zIndex: 1000,
        backgroundColor: "rgba(26, 26, 26, 0.55)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
      }}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-confirmacion-titulo"
        aria-describedby={mensaje ? "modal-confirmacion-mensaje" : undefined}
        // Un clic dentro del cuadro no debe cerrarlo.
        onClick={(e) => e.stopPropagation()}
        style={{
          backgroundColor: "white",
          borderRadius: "18px",
          padding: "28px 24px 22px",
          width: "100%",
          maxWidth: "420px",
          boxShadow: "0 12px 40px rgba(0, 0, 0, 0.28)",
          textAlign: "center",
        }}
      >
        {icono && (
          <div
            aria-hidden="true"
            style={{
              width: 64,
              height: 64,
              borderRadius: "50%",
              margin: "0 auto 18px",
              backgroundColor: tono === "peligro" ? "#FDECEC" : "#EFF5FF",
              color: colorAccion,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {icono}
          </div>
        )}

        <h2
          id="modal-confirmacion-titulo"
          style={{
            fontSize: "1.4rem",
            fontWeight: 700,
            color: "var(--huap-texto)",
            margin: 0,
            lineHeight: 1.3,
          }}
        >
          {titulo}
        </h2>

        {mensaje && (
          <p
            id="modal-confirmacion-mensaje"
            style={{
              fontSize: "1.05rem",
              color: "#555",
              lineHeight: 1.55,
              margin: "12px 0 0",
            }}
          >
            {mensaje}
          </p>
        )}

        <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginTop: "26px" }}>
          <button
            onClick={onConfirmar}
            style={{
              width: "100%",
              // 56px de alto: objetivo táctil holgado.
              padding: "16px 20px",
              borderRadius: "12px",
              border: "none",
              backgroundColor: colorAccion,
              color: "white",
              fontSize: "1.1rem",
              fontWeight: 700,
              cursor: "pointer",
            }}
          >
            {textoConfirmar}
          </button>

          <button
            ref={cancelarRef}
            onClick={onCancelar}
            style={{
              width: "100%",
              padding: "16px 20px",
              borderRadius: "12px",
              border: "2px solid #D8D8D2",
              backgroundColor: "white",
              color: "var(--huap-texto)",
              fontSize: "1.1rem",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            {textoCancelar}
          </button>
        </div>
      </div>
    </div>,
    document.body,
  )
}
