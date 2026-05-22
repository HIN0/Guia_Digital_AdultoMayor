"use client"

import { signIn } from "next-auth/react"
import Image from "next/image"

export default function LoginPage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4"
      style={{ backgroundColor: "var(--huap-fondo)" }}>

      <div className="w-full max-w-sm flex flex-col items-center gap-6">

        <Image
          src="/logo-huap.png"
          alt="Logo HUAP"
          width={90}
          height={90}
          priority
        />

        <div className="text-center">
          <h1 style={{ color: "var(--huap-azul)", fontSize: "26px", fontWeight: 600 }}>
            IA y Salud
          </h1>
          <p style={{ color: "var(--huap-texto)", fontSize: "16px", marginTop: "8px" }}>
            Hospital de Urgencia Asistencia Pública
          </p>
        </div>

        <div className="w-full p-4 rounded-lg text-center"
          style={{ backgroundColor: "var(--huap-ambar-claro)", border: "1px solid var(--huap-ambar)" }}>
          <p style={{ color: "var(--huap-texto)", fontSize: "15px" }}>
            Inicia sesión para acceder a la plataforma
          </p>
        </div>

        <button
          onClick={() => signIn("google", { callbackUrl: "/bienvenida" })}
          className="w-full py-3 px-6 rounded-lg font-medium text-white flex items-center justify-center gap-3"
          style={{
            backgroundColor: "var(--huap-azul)",
            fontSize: "18px",
            minHeight: "52px",
            cursor: "pointer",
          }}>
          Entrar con Google
        </button>

      </div>
    </main>
  )
}