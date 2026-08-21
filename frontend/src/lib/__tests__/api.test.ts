import { describe, it, expect, beforeEach } from "vitest"
import { sincronizarLocalStorage, type ResumenProgreso } from "@/lib/api"

function progreso(overrides: Partial<ResumenProgreso> = {}): ResumenProgreso {
  return {
    lecciones_completadas: [],
    quizzes_aprobados: [],
    insignias: [],
    modulos: [],
    chatbot_desbloqueado: false,
    ...overrides,
  }
}

describe("sincronizarLocalStorage", () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it("guarda las lecciones completadas de cada módulo bajo su propia key", () => {
    const p = progreso({
      modulos: [
        { modulo_id: 1, orden: 1, desbloqueado: true, completado: false, lecciones_completadas: [10, 11] },
      ],
    })
    sincronizarLocalStorage(p, [1])
    expect(JSON.parse(localStorage.getItem("huap_mod1_lecciones_completadas")!)).toEqual([10, 11])
  })

  it("marca el módulo 1 como completado cuando el backend lo confirma", () => {
    const p = progreso({
      modulos: [{ modulo_id: 1, orden: 1, desbloqueado: true, completado: true, lecciones_completadas: [1, 2, 3, 4, 5, 6] }],
    })
    sincronizarLocalStorage(p, [1])
    expect(localStorage.getItem("huap_mod1_completado")).toBe("true")
  })

  it("elimina la marca de completado del módulo 2 si el backend dice que ya no lo está", () => {
    localStorage.setItem("huap_mod2_completado", "true")
    const p = progreso({
      modulos: [{ modulo_id: 2, orden: 2, desbloqueado: true, completado: false, lecciones_completadas: [] }],
    })
    sincronizarLocalStorage(p, [2])
    expect(localStorage.getItem("huap_mod2_completado")).toBeNull()
  })

  it("habilita el chatbot en localStorage cuando el backend lo desbloquea", () => {
    sincronizarLocalStorage(progreso({ chatbot_desbloqueado: true }), [])
    expect(localStorage.getItem("huap_chatbot_desbloqueado")).toBe("true")
  })

  it("quita la marca del chatbot si el backend dice que ya no está desbloqueado", () => {
    localStorage.setItem("huap_chatbot_desbloqueado", "true")
    sincronizarLocalStorage(progreso({ chatbot_desbloqueado: false }), [])
    expect(localStorage.getItem("huap_chatbot_desbloqueado")).toBeNull()
  })

  it("limpia el progreso local de un módulo que ya no viene del backend", () => {
    localStorage.setItem("huap_mod3_lecciones_completadas", JSON.stringify([1]))
    sincronizarLocalStorage(progreso({ modulos: [] }), [3])
    expect(localStorage.getItem("huap_mod3_lecciones_completadas")).toBeNull()
  })
})
