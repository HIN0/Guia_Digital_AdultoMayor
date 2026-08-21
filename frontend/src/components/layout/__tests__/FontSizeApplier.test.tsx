import { describe, it, expect, beforeEach } from "vitest"
import { render } from "@testing-library/react"
import FontSizeApplier from "@/components/layout/FontSizeApplier"

describe("FontSizeApplier", () => {
  beforeEach(() => {
    localStorage.clear()
    document.documentElement.style.fontSize = ""
  })

  it("aplica 18px por defecto cuando no hay preferencia guardada", () => {
    render(<FontSizeApplier />)
    expect(document.documentElement.style.fontSize).toBe("18px")
  })

  it("aplica el tamaño guardado en localStorage", () => {
    localStorage.setItem("fontTamano", "grande")
    render(<FontSizeApplier />)
    expect(document.documentElement.style.fontSize).toBe("22px")
  })
})
