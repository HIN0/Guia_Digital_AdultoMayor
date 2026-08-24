import { describe, it, expect } from "vitest"
import { render, screen } from "@testing-library/react"
import ModuloCard from "@/components/modulos/ModuloCard"
import type { Modulo } from "@/types"

function modulo(overrides: Partial<Modulo> = {}): Modulo {
  return {
    id: 1,
    numero: 1,
    titulo: "Conocer la IA",
    descripcion: "Módulo introductorio",
    estado: "disponible",
    progreso: 0,
    leccionesCompletadas: 0,
    leccionesTotales: 6,
    tieneQuiz: true,
    ...overrides,
  }
}

describe("ModuloCard", () => {
  it("muestra el mensaje de bloqueo y no la barra de progreso cuando el módulo está bloqueado", () => {
    render(<ModuloCard modulo={modulo({ numero: 2, estado: "bloqueado" })} />)
    expect(screen.getByText(/Completa el Módulo 1 para desbloquearlo/)).toBeInTheDocument()
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument()
  })

  it("muestra la barra de progreso con el porcentaje real cuando el módulo está disponible", () => {
    render(<ModuloCard modulo={modulo({ estado: "disponible", progreso: 40, leccionesCompletadas: 2, leccionesTotales: 5 })} />)
    const barra = screen.getByRole("progressbar")
    expect(barra).toHaveAttribute("aria-valuenow", "40")
    expect(screen.getByText("2 de 5 pasos")).toBeInTheDocument()
  })

  it('muestra "Completado" en vez del conteo de lecciones cuando el módulo ya terminó', () => {
    render(<ModuloCard modulo={modulo({ estado: "completado", progreso: 100 })} />)
    expect(screen.getByText("Completado")).toBeInTheDocument()
  })

  it('muestra el atajo "Abrir asistente" para módulos sin lecciones, como el chatbot', () => {
    render(<ModuloCard modulo={modulo({ numero: 3, estado: "disponible", leccionesTotales: 0 })} />)
    expect(screen.getByText(/Abrir asistente/)).toBeInTheDocument()
  })
})
