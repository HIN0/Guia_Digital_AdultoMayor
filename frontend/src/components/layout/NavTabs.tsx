"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { House, BookOpenText, MessageCircle, Lock } from "lucide-react"
import type React from "react"

const TABS: { label: string; href: string; matchPaths: string[]; icon: React.ReactNode; requiereDesbloqueo?: boolean }[] = [
  {
    label: "Inicio",
    href: "/inicio",
    matchPaths: ["/inicio"],
    icon: <House size={34} strokeWidth={2} />,
  },
  {
    label: "Aprender",
    href: "/modulos",
    matchPaths: ["/modulos"],
    icon: <BookOpenText size={34} strokeWidth={2} />,
  },
  {
    label: "Chat",
    href: "/chatbot",
    matchPaths: ["/chatbot"],
    icon: <MessageCircle size={34} strokeWidth={2} />,
    requiereDesbloqueo: true,
  },
]

export default function NavTabs() {
  const pathname = usePathname()
  const [chatbotDesbloqueado, setChatbotDesbloqueado] = useState(false)
  const [mostrarAviso, setMostrarAviso] = useState(false)

  useEffect(() => {
    const check = () => {
      const desbloqueado =
        localStorage.getItem("huap_chatbot_desbloqueado") === "true" ||
        localStorage.getItem("huap_mod2_completado") === "true"
      setChatbotDesbloqueado(desbloqueado)
    }
    check()
    window.addEventListener("storage", check)
    const interval = setInterval(check, 2000)
    return () => {
      window.removeEventListener("storage", check)
      clearInterval(interval)
    }
  }, [])

  useEffect(() => {
    if (mostrarAviso) {
      const timer = setTimeout(() => setMostrarAviso(false), 3000)
      return () => clearTimeout(timer)
    }
  }, [mostrarAviso])

  const OCULTAR_EN = ["/", "/login", "/bienvenida"]
  if (OCULTAR_EN.includes(pathname)) return null
  if (pathname.includes("/lecciones/")) return null

  return (
    <>
      {mostrarAviso && (
        <div
          style={{
            position: "fixed",
            bottom: "100px",
            left: "50%",
            transform: "translateX(-50%)",
            backgroundColor: "#1E293B",
            color: "white",
            padding: "12px 20px",
            borderRadius: "12px",
            fontSize: "14px",
            fontWeight: 500,
            zIndex: 100,
            textAlign: "center",
            maxWidth: "320px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
            animation: "fadeIn 0.2s ease",
          }}
        >
          <Lock size={14} style={{ display: "inline", marginRight: "6px", verticalAlign: "middle" }} />
          Completa los módulos para desbloquear el Chat
        </div>
      )}

      <nav
        aria-label="Navegación principal"
        style={{
          position: "fixed",
          bottom: 0,
          left: 0,
          right: 0,
          zIndex: 50,
          display: "flex",
          justifyContent: "center",
          backgroundColor: "white",
          borderTop: "1px solid #E5E7EB",
          padding: "10px 16px 14px",
          gap: "8px",
        }}
      >
        <div
          style={{
            display: "flex",
            gap: "8px",
            backgroundColor: "#F1F3F8",
            borderRadius: "16px",
            padding: "6px",
            width: "100%",
            maxWidth: "480px",
            justifyContent: "space-between",
          }}
        >
          {TABS.map((tab) => {
            const active = tab.matchPaths.some((p) => pathname === p || pathname.startsWith(p + "/"))
            const bloqueado = tab.requiereDesbloqueo && !chatbotDesbloqueado

            if (bloqueado) {
              return (
                <button
                  key={tab.href}
                  onClick={() => setMostrarAviso(true)}
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "4px",
                    flex: 1,
                    padding: "8px 4px",
                    borderRadius: "12px",
                    border: "none",
                    background: "transparent",
                    cursor: "pointer",
                    color: "#C0C0C0",
                    position: "relative",
                  }}
                >
                  <div style={{ position: "relative" }}>
                    {tab.icon}
                    <Lock
                      size={12}
                      strokeWidth={2.5}
                      style={{
                        position: "absolute",
                        bottom: -2,
                        right: -6,
                        color: "#9E9E9E",
                      }}
                    />
                  </div>
                  <span style={{ fontSize: "14px", fontWeight: 400, lineHeight: 1 }}>
                    {tab.label}
                  </span>
                </button>
              )
            }

            return (
              <Link
                key={tab.href}
                href={tab.href}
                aria-current={active ? "page" : undefined}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "4px",
                  flex: 1,
                  padding: "8px 4px",
                  borderRadius: "12px",
                  textDecoration: "none",
                  transition: "background 0.15s, color 0.15s",
                  backgroundColor: active ? "var(--huap-azul)" : "transparent",
                  color: active ? "white" : "#6B7280",
                }}
              >
                {tab.icon}
                <span style={{ fontSize: "14px", fontWeight: active ? 600 : 400, lineHeight: 1 }}>
                  {tab.label}
                </span>
              </Link>
            )
          })}
        </div>
      </nav>
    </>
  )
}
