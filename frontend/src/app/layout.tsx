import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IA y Salud · Guía Digital para Personas Mayores",
  description:
    "Plataforma educativa del Hospital de Urgencia Asistencia Pública (HUAP) para aprender a usar inteligencia artificial de forma segura en información de salud.",
  keywords: [
    "adultos mayores",
    "alfabetización digital",
    "inteligencia artificial",
    "salud",
    "HUAP",
    "Posta Central",
  ],
  authors: [{ name: "HUAP - Posta Central" }],
  robots: {
    index: false,
    follow: false,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="h-full antialiased">
      <body className="min-h-full flex flex-col bg-huap-fondo text-huap-texto">
        {children}
      </body>
    </html>
  );
}
