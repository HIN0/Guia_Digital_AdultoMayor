import "@testing-library/jest-dom/vitest"
import { afterEach } from "vitest"
import { cleanup } from "@testing-library/react"

// jsdom no implementa layout, así que tampoco scrollIntoView; varias páginas
// (lección, quiz) lo llaman para desplazar hacia el siguiente elemento.
Element.prototype.scrollIntoView = () => {}

afterEach(() => {
  cleanup()
})
