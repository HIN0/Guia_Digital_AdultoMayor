"use client"

import { useSession, signOut } from "next-auth/react"
import Image from "next/image"
import Link from "next/link"

export default function Header() {
  const { data: session } = useSession()

  return (
    <header>
      <div style={{
        backgroundColor: "var(--huap-azul)",
        paddingBottom: "30px",
        position: "relative",
        overflow: "hidden",
      }}>
        {/* Círculo decorativo */}
        <div style={{
          position: "absolute", top: -40, right: -40,
          width: 160, height: 160, borderRadius: "50%",
          backgroundColor: "rgba(255,255,255,0.06)", pointerEvents: "none",
        }} />

        {/* Contenido */}
        <div style={{
          display: "flex", alignItems: "center", justifyContent: "space-between",
          position: "relative", zIndex: 1, padding: "10px 16px 0",
        }}>
          <Link href="/inicio" style={{ display: "flex", alignItems: "center", gap: "10px", textDecoration: "none" }}>
            <Image src="/logo-huap.png" alt="Logo HUAP" width={40} height={40} style={{ borderRadius: "50%" }} />
            <div style={{ lineHeight: 1.2 }}>
              <div style={{ color: "white", fontWeight: 700, fontSize: "16px" }}>IA y Salud</div>
              <div style={{ color: "rgba(255,255,255,0.65)", fontSize: "11px", letterSpacing: "0.1em" }}>HUAP</div>
            </div>
          </Link>

          <button
            onClick={() => { if (window.confirm("¿Cerrar sesión?")) signOut({ callbackUrl: "/" }) }}
            title="Cerrar sesión"
            style={{
              width: 38, height: 38, borderRadius: "50%", flexShrink: 0,
              backgroundColor: "rgba(255,255,255,0.12)",
              border: "none", outline: "none", boxShadow: "none",
              cursor: "pointer", padding: 0, overflow: "hidden",
              display: "flex", alignItems: "center", justifyContent: "center",
              color: "white", fontWeight: 700, fontSize: "15px",
            }}
          >
            {session?.user?.image ? (
              <Image src={session.user.image} alt="Foto de perfil" width={38} height={38} style={{ borderRadius: "50%", display: "block" }} />
            ) : (
              session?.user?.name?.[0]?.toUpperCase() ?? "U"
            )}
          </button>
        </div>
      </div>

      {/* Ola fuera del overflow:hidden — el backgroundColor cubre el overlap de 2px con el azul del header */}
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
    </header>
  )
}
