import type { Metadata } from "next"
import "./globals.css"
import NextAuthProvider from "@/components/layout/SessionProvider"
import NavTabs from "@/components/layout/NavTabs"
import FontSizeApplier from "@/components/layout/FontSizeApplier"

export const metadata: Metadata = {
  title: "IA y Salud · Guía Digital para Personas Mayores",
  description: "Aprende a usar la inteligencia artificial para entender información de salud de forma segura",
  keywords: ["IA", "salud", "adulto mayor", "HUAP", "inteligencia artificial"],
  authors: [{ name: "Hospital de Urgencia Asistencia Pública" }],
  robots: "noindex, nofollow",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className="antialiased min-h-screen flex flex-col">
        <NextAuthProvider>
          <FontSizeApplier />
          {children}
          <NavTabs />
        </NextAuthProvider>
      </body>
    </html>
  )
} 