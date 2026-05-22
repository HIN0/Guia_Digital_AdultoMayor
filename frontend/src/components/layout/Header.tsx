"use client"

import { useSession, signOut } from "next-auth/react"
import Image from "next/image"
import Link from "next/link"

export default function Header() {
  const { data: session } = useSession()

  return (
    <header className="w-full px-6 py-3 flex items-center justify-between"
      style={{ backgroundColor: "var(--huap-azul)" }}>
      <Link href="/modulos" className="flex items-center gap-3">
        <Image
          src="/logo-huap.png"
          alt="Logo HUAP"
          width={40}
          height={40}
        />
        <span style={{ color: "white", fontWeight: 600, fontSize: "16px" }}>
          IA y Salud
        </span>
      </Link>

      <div className="flex items-center gap-3">
        {session?.user?.image && (
          <Image
            src={session.user.image}
            alt="Foto de perfil"
            width={36}
            height={36}
            className="rounded-full"
          />
        )}
        <span style={{ color: "white", fontSize: "14px" }}>
          {session?.user?.name}
        </span>
        <button
          onClick={() => {
            if (window.confirm("¿Estás seguro que deseas cerrar sesión?")) {
              signOut({ callbackUrl: "/" })
            }
          }}
          className="px-3 py-1 rounded text-sm"
          style={{
            backgroundColor: "transparent",
            color: "white",
            border: "1px solid white",
            cursor: "pointer",
            minHeight: "36px",
          }}>
          Cerrar sesión
        </button>
      </div>
    </header>
  )
}