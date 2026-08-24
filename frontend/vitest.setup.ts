import "@testing-library/jest-dom/vitest"
import { afterEach } from "vitest"
import { cleanup } from "@testing-library/react"

// jsdom no implementa layout, así que tampoco scrollIntoView; varias páginas
// (lección, quiz) lo llaman para desplazar hacia el siguiente elemento.
Element.prototype.scrollIntoView = () => {}

// jsdom tampoco implementa matchMedia; el chatbot lo usa para detectar
// pantallas táctiles ("(pointer: coarse)") vía useSyncExternalStore.
window.matchMedia = window.matchMedia || ((query: string) => ({
  matches: false,
  media: query,
  onchange: null,
  addEventListener: () => {},
  removeEventListener: () => {},
  addListener: () => {},
  removeListener: () => {},
  dispatchEvent: () => false,
})) as typeof window.matchMedia

afterEach(() => {
  cleanup()
})
