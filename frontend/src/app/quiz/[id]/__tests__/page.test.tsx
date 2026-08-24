import { describe, it, expect, beforeEach, vi } from "vitest"
import { render, screen, fireEvent } from "@testing-library/react"
import type { ModuloDetalle, ResultadoQuiz } from "@/lib/api"

vi.mock("next/navigation", () => ({
  useParams: () => ({ id: "100" }),
  useRouter: () => ({ back: vi.fn(), push: vi.fn() }),
}))
vi.mock("next-auth/react", () => ({
  useSession: () => ({ data: { accessToken: "fake-token" } }),
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
vi.mock("@/lib/api", () => ({
  getModuloDetalle: vi.fn(),
  submitQuizFinal: vi.fn(),
}))

import { getModuloDetalle, submitQuizFinal } from "@/lib/api"
import QuizFinalPage from "@/app/quiz/[id]/page"

const moduloMock: ModuloDetalle = {
  id: 10,
  nombre: "Conocer la IA",
  orden: 1,
  requiere_modulo_previo: false,
  lecciones: [],
  quiz_final: {
    id: 100,
    minimo_aciertos: 1,
    bloqueante: true,
    preguntas: [
      { id: 1, enunciado: "¿Qué es la IA?", opciones: [{ id: 11, texto: "Una herramienta" }, { id: 12, texto: "Un robot" }] },
      { id: 2, enunciado: "¿La IA puede fallar?", opciones: [{ id: 21, texto: "Sí" }, { id: 22, texto: "No" }] },
    ],
  },
}

function resultado(overrides: Partial<ResultadoQuiz> = {}): ResultadoQuiz {
  return {
    puntaje: 2,
    minimo_aciertos: 1,
    aprobado: true,
    feedbacks: [
      { pregunta_id: 1, opcion_correcta_id: 11, opcion_seleccionada_id: 11, es_correcta: true, feedback: "¡Correcto!" },
      { pregunta_id: 2, opcion_correcta_id: 21, opcion_seleccionada_id: 21, es_correcta: true, feedback: "¡Correcto!" },
    ],
    insignia_otorgada: { id: 1, nombre: "Conocedor de la IA", descripcion: "Completaste el Módulo 1", icono_url: "🧠" },
    ...overrides,
  }
}

describe("QuizFinalPage", () => {
  beforeEach(() => {
    sessionStorage.clear()
    localStorage.clear()
    vi.clearAllMocks()
  })

  it("muestra un error si no hay un módulo de origen guardado en sessionStorage", () => {
    render(<QuizFinalPage />)
    expect(screen.getByText(/No se pudo cargar la prueba/)).toBeInTheDocument()
    expect(getModuloDetalle).not.toHaveBeenCalled()
  })

  it("al aprobar, guarda las insignias en localStorage y muestra la fase de felicitaciones", async () => {
    sessionStorage.setItem("huap_quiz_modulo_id", "10")
    vi.mocked(getModuloDetalle).mockResolvedValue(moduloMock)
    vi.mocked(submitQuizFinal).mockResolvedValue(resultado({ aprobado: true }))

    render(<QuizFinalPage />)

    await screen.findByText("¿Qué es la IA?")
    fireEvent.click(screen.getByText("Una herramienta"))
    fireEvent.click(screen.getByText("Siguiente pregunta →"))

    await screen.findByText("¿La IA puede fallar?")
    fireEvent.click(screen.getByText("Sí"))
    fireEvent.click(screen.getByText("Ver resultado →"))

    await screen.findByText("¡Felicitaciones!")
    expect(submitQuizFinal).toHaveBeenCalledWith(
      100,
      [{ pregunta_id: 1, opcion_id: 11 }, { pregunta_id: 2, opcion_id: 21 }],
      "fake-token",
    )
    expect(localStorage.getItem("huap_mod1_completado")).toBe("true")
    expect(localStorage.getItem("huap_quiz1_aprobado")).toBe("true")
  })

  it("si no aprueba, muestra la fase de resultado sin desbloquear nada y permite reintentar", async () => {
    sessionStorage.setItem("huap_quiz_modulo_id", "10")
    vi.mocked(getModuloDetalle).mockResolvedValue(moduloMock)
    vi.mocked(submitQuizFinal).mockResolvedValue(
      resultado({ aprobado: false, puntaje: 0, feedbacks: [] }),
    )

    render(<QuizFinalPage />)

    await screen.findByText("¿Qué es la IA?")
    fireEvent.click(screen.getByText("Un robot"))
    fireEvent.click(screen.getByText("Siguiente pregunta →"))

    await screen.findByText("¿La IA puede fallar?")
    fireEvent.click(screen.getByText("No"))
    fireEvent.click(screen.getByText("Ver resultado →"))

    await screen.findByText("¡Casi lo logras!")
    expect(screen.getByText("Intentar de nuevo")).toBeInTheDocument()
    expect(localStorage.getItem("huap_mod1_completado")).toBeNull()
  })
})
