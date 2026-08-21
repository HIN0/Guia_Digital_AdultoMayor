import { describe, it, expect, beforeEach, vi } from "vitest"
import { render, screen, fireEvent, waitFor } from "@testing-library/react"

const mockReplace = vi.fn()

vi.mock("next/navigation", () => ({
  useRouter: () => ({ replace: mockReplace, push: vi.fn(), back: vi.fn() }),
}))

const mockUseSession = vi.fn()
vi.mock("next-auth/react", () => ({
  useSession: () => mockUseSession(),
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
  preguntarChatbot: vi.fn(),
  valorarMensaje: vi.fn(),
  listarConversaciones: vi.fn(),
  obtenerMensajesConversacion: vi.fn(),
  getProgreso: vi.fn(),
}))

import { preguntarChatbot, valorarMensaje, getProgreso } from "@/lib/api"
import ChatbotPage from "@/app/chatbot/page"

describe("ChatbotPage", () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
    mockUseSession.mockReturnValue({ data: null })
  })

  it("redirige a /modulos si el chatbot no está desbloqueado ni el módulo 2 completado", () => {
    render(<ChatbotPage />)
    expect(mockReplace).toHaveBeenCalledWith("/modulos")
  })

  it("no redirige y marca el chatbot como desbloqueado si el módulo 2 ya está completado", () => {
    localStorage.setItem("huap_mod2_completado", "true")
    render(<ChatbotPage />)
    expect(mockReplace).not.toHaveBeenCalled()
    expect(localStorage.getItem("huap_chatbot_desbloqueado")).toBe("true")
  })

  it("permite enviar una pregunta desde los chips de temas y muestra la respuesta del bot", async () => {
    mockUseSession.mockReturnValue({ data: { accessToken: "fake-token" } })
    vi.mocked(getProgreso).mockResolvedValue(null)
    vi.mocked(preguntarChatbot).mockResolvedValue({
      respuesta: "La neumonía es una infección pulmonar.",
      conversacion_id: 1,
      mensaje_id: 5,
    })

    render(<ChatbotPage />)
    fireEvent.click(screen.getByText("Neumonía"))

    await screen.findByText("La neumonía es una infección pulmonar.")
    expect(preguntarChatbot).toHaveBeenCalledWith("¿Qué es la neumonía?", null, "fake-token")
  })

  it("al valorar una respuesta, llama a valorarMensaje y deshabilita el botón", async () => {
    mockUseSession.mockReturnValue({ data: { accessToken: "fake-token" } })
    vi.mocked(getProgreso).mockResolvedValue(null)
    vi.mocked(preguntarChatbot).mockResolvedValue({
      respuesta: "La neumonía es una infección pulmonar.",
      conversacion_id: 1,
      mensaje_id: 5,
    })
    vi.mocked(valorarMensaje).mockResolvedValue(undefined)

    render(<ChatbotPage />)
    fireEvent.click(screen.getByText("Neumonía"))
    await screen.findByText("La neumonía es una infección pulmonar.")

    const botonUtil = screen.getByTitle("Respuesta útil")
    fireEvent.click(botonUtil)

    await waitFor(() => expect(valorarMensaje).toHaveBeenCalledWith(5, "positiva", "fake-token"))
    expect(botonUtil).toBeDisabled()
  })
})
