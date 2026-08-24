"use client"

import { signIn } from "next-auth/react"
import Image from "next/image"
import Link from "next/link"

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4"
      style={{ backgroundColor: "var(--huap-fondo)" }}>

      <div className="w-full max-w-sm sm:max-w-lg flex flex-col items-center gap-6">

        <Image
          src="/logo-huap.png"
          alt="Logo Hospital de Urgencia Asistencia Pública"
          width={110}
          height={110}
          priority
        />

        <div className="text-center">
          <h1 style={{ color: "var(--huap-azul)" }}>
            IA y Salud
          </h1>
          <p className="text-lg mt-1" style={{ color: "var(--huap-texto)" }}>
            Hospital de Urgencia Asistencia Pública
          </p>
          <p className="mt-3" style={{ color: "var(--huap-texto)", fontSize: "18px" }}>
            Aprende a usar la inteligencia artificial para entender
            información de salud de forma segura
          </p>
        </div>

        <div className="w-full p-4 rounded-lg"
          style={{
            backgroundColor: "white",
            border: "2px solid var(--huap-verde)",
          }}>
          <p style={{ color: "var(--huap-texto)", fontSize: "18px" }}>
            Esta aplicación te enseña paso a paso. No necesitas experiencia previa.
          </p>
        </div>

        <div className="w-full flex flex-col gap-3">
          <button
            onClick={() => signIn("google", { callbackUrl: "/bienvenida" }).catch(console.error)}
            className="w-full py-3 px-6 rounded-lg font-medium text-white flex items-center justify-center gap-3"
            style={{
              backgroundColor: "var(--huap-azul)",
              fontSize: "18px",
              minHeight: "52px",
              cursor: "pointer",
            }}>
            <svg width="22" height="22" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
              <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
              <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
              <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
              <path fill="none" d="M0 0h48v48H0z"/>
            </svg>
            Entrar con Google 
          </button>

          <Link
            href="/ayuda-google"
            className="w-full py-3 px-6 rounded-lg font-medium"
            style={{
              backgroundColor: "transparent",
              border: "2px solid var(--huap-azul)",
              color: "var(--huap-azul)",
              fontSize: "18px",
              minHeight: "52px",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
              textDecoration: "none",
            }}>
            ¿No tienes una cuenta de Google?
          </Link>
        </div>

        <footer className="text-center mt-4">
          <p style={{ color: "var(--huap-texto)", fontSize: "14px" }}>
            Hospital de Urgencia Asistencia Pública — Posta Central
          </p>
        </footer>

      </div>
    </main>
  )
}