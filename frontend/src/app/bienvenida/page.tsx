"use client"

import { useRouter } from "next/navigation"
import Image from "next/image"

export default function BienvenidaPage() {
  const router = useRouter()

  const handleContinuar = () => {
    router.push("/modulos")
  }

  return (
    <div className="min-h-screen flex flex-col"
      style={{ backgroundColor: "var(--huap-fondo)" }}>

      <header className="w-full px-4 py-3 flex items-center gap-3"
        style={{ backgroundColor: "var(--huap-azul)" }}>
        <Image src="/logo-huap.png" alt="Logo HUAP" width={36} height={36} />
        <div>
          <p style={{ color: "white", fontWeight: 600, fontSize: "16px", lineHeight: 1.2 }}>
            IA y Salud
          </p>
          <p style={{ color: "#a8c8e8", fontSize: "12px" }}>HUAP</p>
        </div>
      </header>

      <main className="flex-1 flex flex-col px-5 py-6 gap-5 max-w-lg mx-auto w-full">

        <div>
          <h1 style={{ color: "var(--huap-azul)", fontSize: "28px", fontWeight: 700 }}>
            ¡Bienvenido!
          </h1>
          <p style={{ color: "var(--huap-texto)", fontSize: "18px", marginTop: "8px" }}>
            Te vamos a enseñar a usar esta aplicación paso a paso.
          </p>
        </div>

        <div className="rounded-lg p-4"
          style={{ backgroundColor: "white", border: "2px solid var(--huap-verde)" }}>
          <p style={{ color: "var(--huap-texto)", fontSize: "17px" }}>
            <strong>No te preocupes si te equivocas.</strong> Siempre puedes volver atrás cuando quieras.
          </p>
        </div>

        <div className="rounded-lg p-4"
          style={{ backgroundColor: "var(--huap-ambar-claro)", border: "1px solid var(--huap-ambar)" }}>
          <p style={{ color: "var(--huap-texto)", fontSize: "17px" }}>
            Esta aplicación entrega información educativa sobre IA y salud.{" "}
            <strong>No reemplaza la consulta con tu médico o médica.</strong>
          </p>
        </div>

        <div className="rounded-lg p-4"
          style={{ backgroundColor: "var(--huap-gris-suave)", border: "1px solid #ddd" }}>
          <p style={{ color: "var(--huap-texto)", fontSize: "17px" }}>
            Toca el botón verde para continuar →
          </p>
        </div>

        <button
          onClick={handleContinuar}
          className="w-full py-4 rounded-xl font-semibold text-white mt-20"
          style={{
            backgroundColor: "var(--huap-verde)",
            fontSize: "20px",
            minHeight: "56px",
            cursor: "pointer",
          }}>
          Continuar
        </button>

      </main>

    </div>
  )
}