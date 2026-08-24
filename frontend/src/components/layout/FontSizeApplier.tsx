"use client"

import { useEffect } from "react"

const FONT_MAP: Record<string, string> = {
  pequeño: "16px",
  mediano: "18px",
  grande: "22px",
}

export default function FontSizeApplier() {
  useEffect(() => {
    const saved = localStorage.getItem("fontTamano") ?? "mediano"
    document.documentElement.style.fontSize = FONT_MAP[saved] ?? "18px"
  }, [])
  return null
}
