"use client"

import { useSession, signOut } from "next-auth/react"
import Image from "next/image"
import Link from "next/link"
import { useState, useEffect, useRef } from "react"
import { useRouter } from "next/navigation"

const TAMANOS = ["pequeño", "mediano", "grande"] as const
type Tamano = typeof TAMANOS[number]
const FONT_MAP: Record<Tamano, string> = { pequeño: "16px", mediano: "18px", grande: "22px" }

export default function Header() {
  const { data: session } = useSession()
  const router = useRouter()
  const [open, setOpen] = useState(false)
  const [tamano, setTamano] = useState<Tamano>("mediano")
  const buttonRef = useRef<HTMLDivElement>(null)
  const panelRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const saved = (localStorage.getItem("fontTamano") ?? "mediano") as Tamano
    setTamano(saved)
    document.documentElement.style.fontSize = FONT_MAP[saved]
  }, [])

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      const target = e.target as Node
      if (
        buttonRef.current && !buttonRef.current.contains(target) &&
        panelRef.current && !panelRef.current.contains(target)
      ) {
        setOpen(false)
      }
    }
    if (open) document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [open])

  function cambiarTamano(dir: -1 | 1) {
    const idx = TAMANOS.indexOf(tamano)
    const nuevoIdx = idx + dir
    if (nuevoIdx < 0 || nuevoIdx >= TAMANOS.length) return
    const nuevo = TAMANOS[nuevoIdx]
    setTamano(nuevo)
    localStorage.setItem("fontTamano", nuevo)
    document.documentElement.style.fontSize = FONT_MAP[nuevo]
    window.dispatchEvent(new Event("huap-font-change"))
  }

  return (
    <header style={{ position: "sticky", top: 0, zIndex: 100 }}>
      <div className="header-inner" style={{
        backgroundColor: "var(--huap-azul)",
        paddingBottom: "22px",
        position: "relative",
        overflow: "hidden",
      }}>
        {/* Círculo decorativo */}
        <div style={{
          position: "absolute", top: -40, right: -40,
          width: 160, height: 160, borderRadius: "50%",
          backgroundColor: "rgba(255,255,255,0.06)", pointerEvents: "none",
        }} />

        {/* Contenido — grid 3 cols para centrar el control de fuente */}
        <div style={{
          display: "grid",
          gridTemplateColumns: "1fr auto 1fr",
          alignItems: "center",
          position: "relative", zIndex: 1, padding: "16px 16px 0",
        }}>
          {/* Columna izquierda: logo */}
          <Link href="/inicio" style={{ display: "flex", alignItems: "center", gap: "10px", textDecoration: "none" }}>
            <Image src="/logo-huap.png" alt="Logo HUAP" width={52} height={52} style={{ borderRadius: "50%" }} />
            <div style={{ lineHeight: 1.2 }}>
              <div style={{ color: "white", fontWeight: 700, fontSize: "16px" }}>IA y Salud</div>
              <div style={{ color: "rgba(255,255,255,0.65)", fontSize: "11px", letterSpacing: "0.1em" }}>HUAP</div>
            </div>
          </Link>

          {/* Columna central: control de tamaño de fuente */}
          <div style={{
            display: "flex",
            alignItems: "center",
            backgroundColor: "rgba(255,255,255,0.13)",
            borderRadius: "24px",
            border: "1px solid rgba(255,255,255,0.22)",
            overflow: "hidden",
          }}>
            <button
              onClick={() => cambiarTamano(-1)}
              disabled={tamano === "pequeño"}
              title="Reducir letra"
              style={{
                padding: "8px 13px",
                background: "none", border: "none",
                cursor: tamano === "pequeño" ? "default" : "pointer",
                color: tamano === "pequeño" ? "rgba(255,255,255,0.3)" : "white",
                fontSize: "20px", fontWeight: 700, lineHeight: 1,
                transition: "color 0.15s",
              }}
            >
              −
            </button>
            <div style={{
              width: "32px",
              display: "flex", alignItems: "center", justifyContent: "center",
              borderLeft: "1px solid rgba(255,255,255,0.18)",
              borderRight: "1px solid rgba(255,255,255,0.18)",
              padding: "6px 0",
              userSelect: "none",
            }}>
              <span style={{
                color: "white",
                fontWeight: 700,
                lineHeight: 1,
                fontSize: tamano === "pequeño" ? "13px" : tamano === "grande" ? "21px" : "17px",
                transition: "font-size 0.15s",
              }}>A</span>
            </div>
            <button
              onClick={() => cambiarTamano(1)}
              disabled={tamano === "grande"}
              title="Aumentar letra"
              style={{
                padding: "8px 13px",
                background: "none", border: "none",
                cursor: tamano === "grande" ? "default" : "pointer",
                color: tamano === "grande" ? "rgba(255,255,255,0.3)" : "white",
                fontSize: "20px", fontWeight: 700, lineHeight: 1,
                transition: "color 0.15s",
              }}
            >
              +
            </button>
          </div>

          {/* Columna derecha: botón de perfil */}
          <div style={{ display: "flex", justifyContent: "flex-end" }}>
            <div ref={buttonRef}>
              <button
                onClick={() => setOpen(v => !v)}
                title="Mi perfil"
                style={{
                  width: 46, height: 46, borderRadius: "50%", flexShrink: 0,
                  backgroundColor: "rgba(255,255,255,0.12)",
                  border: "none", outline: "none", boxShadow: "none",
                  cursor: "pointer", padding: 0, overflow: "hidden",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  color: "white", fontWeight: 700, fontSize: "15px",
                }}
              >
                {session?.user?.image ? (
                  <Image src={session.user.image} alt="Foto de perfil" width={46} height={46} style={{ borderRadius: "50%", display: "block" }} />
                ) : (
                  session?.user?.name?.[0]?.toUpperCase() ?? "U"
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Ola */}
      <svg
        viewBox="0 0 1440 40"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="none"
        style={{
          display: "block",
          width: "100%",
          height: "32px",
          marginTop: "-32px",
          backgroundColor: "var(--huap-azul)",
        }}
      >
        <path d="M0,40 Q720,0 1440,40 L1440,50 L0,50 Z" fill="#FAFAF7" />
      </svg>

      {/* Dropdown — fuera del overflow:hidden, anclado al header */}
      {open && (
        <div ref={panelRef} style={{
          position: "absolute", top: "62px", right: "16px",
          backgroundColor: "white", borderRadius: "16px",
          boxShadow: "0 6px 24px rgba(0,0,0,0.18)",
          minWidth: "260px", zIndex: 200, overflow: "hidden",
        }}>
          {/* Info del usuario */}
          <div style={{
            display: "flex", alignItems: "center", gap: "14px",
            padding: "20px",
            borderBottom: "1px solid #f0f0f0",
          }}>
            <div style={{
              width: 50, height: 50, borderRadius: "50%", flexShrink: 0,
              backgroundColor: "var(--huap-azul)",
              display: "flex", alignItems: "center", justifyContent: "center",
              color: "white", fontWeight: 700, fontSize: "20px",
              overflow: "hidden",
            }}>
              {session?.user?.image ? (
                <Image src={session.user.image} alt="Foto de perfil" width={50} height={50} style={{ borderRadius: "50%", display: "block" }} />
              ) : (
                session?.user?.name?.[0]?.toUpperCase() ?? "U"
              )}
            </div>
            <div style={{ overflow: "hidden" }}>
              <div style={{ fontWeight: 700, fontSize: "17px", color: "#1a1a1a", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                {session?.user?.name ?? "Usuario"}
              </div>
              <div style={{ fontSize: "14px", color: "#888", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", marginTop: "2px" }}>
                {session?.user?.email ?? ""}
              </div>
            </div>
          </div>

          {/* Progreso */}
          <button
            onClick={() => { setOpen(false); router.push("/progreso") }}
            style={{
              width: "100%", padding: "18px 20px",
              display: "flex", alignItems: "center", gap: "14px",
              background: "none", border: "none", borderBottom: "1px solid #f0f0f0",
              cursor: "pointer", color: "#333", fontWeight: 500, fontSize: "17px",
              textAlign: "left",
            }}
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
            Progreso
          </button>

          {/* Ajustes */}
          <button
            onClick={() => { setOpen(false); router.push("/ajustes") }}
            style={{
              width: "100%", padding: "18px 20px",
              display: "flex", alignItems: "center", gap: "14px",
              background: "none", border: "none", borderBottom: "1px solid #f0f0f0",
              cursor: "pointer", color: "#333", fontWeight: 500, fontSize: "17px",
              textAlign: "left",
            }}
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
            </svg>
            Ajustes
          </button>

          {/* Cerrar sesión */}
          <button
            onClick={() => { if (window.confirm("¿Cerrar sesión?")) signOut({ callbackUrl: "/" }) }}
            style={{
              width: "100%", padding: "18px 20px",
              display: "flex", alignItems: "center", gap: "14px",
              background: "none", border: "none", cursor: "pointer",
              color: "#e53935", fontWeight: 500, fontSize: "17px",
              textAlign: "left",
            }}
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            Cerrar sesión
          </button>
        </div>
      )}
    </header>
  )
}
