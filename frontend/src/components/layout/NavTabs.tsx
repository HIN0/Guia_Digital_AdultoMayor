"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { House, BookOpenText, MessageCircle } from "lucide-react"
import type React from "react"

const TABS: { label: string; href: string; matchPaths: string[]; icon: React.ReactNode }[] = [
  {
    label: "Inicio",
    href: "/inicio",
    matchPaths: ["/inicio"],
    icon: <House size={26} strokeWidth={2} />,
  },
  {
    label: "Aprender",
    href: "/modulos",
    matchPaths: ["/modulos"],
    icon: <BookOpenText size={26} strokeWidth={2} />,
  },
  {
    label: "Chat",
    href: "/chatbot",
    matchPaths: ["/chatbot"],
    icon: <MessageCircle size={26} strokeWidth={2} />,
  },
]

export default function NavTabs() {
  const pathname = usePathname()

  const OCULTAR_EN = ["/", "/login", "/bienvenida"]
  if (OCULTAR_EN.includes(pathname)) return null

  return (
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
          return (
            <Link
              key={tab.href}
              href={tab.href}
              aria-current={active ? "page" : undefined}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "7px",
                flex: 1,
                padding: "9px 12px",
                borderRadius: "12px",
                fontWeight: active ? 600 : 400,
                fontSize: "18px",
                textDecoration: "none",
                transition: "background 0.15s, color 0.15s",
                backgroundColor: active ? "var(--huap-azul)" : "transparent",
                color: active ? "white" : "#6B7280",
              }}
            >
              {tab.icon}
              {tab.label}
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
