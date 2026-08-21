import { describe, it, expect, beforeEach, vi } from "vitest"
import { render, screen, fireEvent } from "@testing-library/react"

vi.mock("next/navigation", () => ({
  useRouter: () => ({ back: vi.fn(), push: vi.fn() }),
}))
vi.mock("next-auth/react", () => ({
  useSession: () => ({ data: null }),
  signOut: vi.fn(),
}))
vi.mock("next/image", () => ({
  // Stand-in de prueba, no una <img> real de producción.
  // eslint-disable-next-line @next/next/no-img-element, jsx-a11y/alt-text
  default: (props: Record<string, unknown>) => <img {...props} />,
}))
vi.mock("next/link", () => ({
  default: ({ href, children, ...props }: { href: string; children: React.ReactNode }) => (
    <a href={href} {...props}>{children}</a>
  ),
}))

import AjustesPage from "@/app/ajustes/page"

describe("AjustesPage", () => {
  beforeEach(() => {
    localStorage.clear()
    document.documentElement.style.fontSize = ""
  })

  // Regresión: antes, la preferencia se leía en un useEffect de montaje que
  // hacía setState de forma síncrona (react-hooks/set-state-in-effect).
  it("arranca ya reflejando el tamaño guardado en localStorage, sin esperar un efecto extra", () => {
    localStorage.setItem("fontTamano", "grande")
    render(<AjustesPage />)
    expect(document.documentElement.style.fontSize).toBe("22px")
    // Se compara el estilo inline crudo (no el computado): jsdom no resuelve
    // custom properties CSS como --huap-azul al calcular estilos.
    const boton = screen.getByText("Grande").closest("button")
    expect(boton?.style.border).toBe("2px solid var(--huap-azul)")
  })

  it("usa mediano por defecto cuando no hay preferencia guardada", () => {
    render(<AjustesPage />)
    expect(document.documentElement.style.fontSize).toBe("18px")
  })

  it("al elegir un tamaño, lo guarda en localStorage y actualiza el documento", () => {
    render(<AjustesPage />)
    fireEvent.click(screen.getByText("Pequeño"))
    expect(localStorage.getItem("fontTamano")).toBe("pequeño")
    expect(document.documentElement.style.fontSize).toBe("16px")
  })
})
