import Link from "next/link"
import { Check, Lightbulb } from "lucide-react"

// Se listan los DATOS que pide Google, no los pasos de sus pantallas: el orden y
// el diseño de su registro cambian cada cierto tiempo, pero los datos no.
const DATOS = [
  {
    titulo: "Tu nombre y tu apellido",
    texto: "Escríbelos como aparecen en tu carnet.",
  },
  {
    titulo: "Tu fecha de nacimiento",
    texto: "El día, el mes y el año en que naciste.",
  },
  {
    titulo: "Un nombre para tu correo",
    texto: "Es lo que va antes de @gmail.com. Si el que elegiste ya está ocupado, Google te va a pedir que pruebes con otro.",
  },
  {
    titulo: "Una contraseña",
    texto: "La eliges tú. Google va a pedirte que la escribas dos veces para confirmar.",
  },
  {
    titulo: "Tu número de celular",
    texto: "Google te envía un código por mensaje de texto y tienes que escribirlo para confirmar que eres tú.",
  },
]

const CONSEJOS = [
  "Ten tu celular a mano antes de empezar. El código llega por mensaje y hay que escribirlo en el momento.",
  "Anota tu contraseña en un papel y guárdalo en un lugar seguro. La vas a necesitar cada vez que entres.",
  "No te preocupes si las pantallas de Google no se ven igual que aquí. Van cambiando, pero los datos que piden son estos.",
]

export default function AyudaGooglePage() {
  return (
    <main
      className="min-h-screen flex flex-col items-center px-5 py-8"
      style={{ backgroundColor: "var(--huap-fondo)" }}
    >
      <div className="w-full flex flex-col gap-6" style={{ maxWidth: "680px" }}>

        <Link
          href="/"
          className="py-3 px-6 rounded-lg font-medium text-white"
          style={{
            alignSelf: "flex-start",
            backgroundColor: "var(--huap-azul)",
            fontSize: "18px",
            minHeight: "52px",
            display: "flex",
            alignItems: "center",
            textDecoration: "none",
          }}
        >
          ← Volver
        </Link>

        <h1 style={{ color: "var(--huap-azul)", fontSize: "1.75rem", fontWeight: 800, lineHeight: 1.2 }}>
          ¿No tienes una cuenta de Google?
        </h1>

        {/* Bloque 1 — la mayoría ya tiene cuenta y no lo sabe */}
        <section
          className="w-full p-5 rounded-lg"
          style={{ backgroundColor: "white", border: "2px solid var(--huap-verde)" }}
        >
          <h2 style={{ color: "var(--huap-texto)", fontSize: "20px", fontWeight: 700, marginBottom: "12px" }}>
            Primero: quizás ya tienes una
          </h2>
          <p style={{ color: "var(--huap-texto)", fontSize: "18px", lineHeight: 1.6 }}>
            Mucha gente tiene una cuenta de Google sin saberlo. Si usas un celular
            Android, o alguna vez abriste <strong>Gmail</strong>, <strong>YouTube</strong> o
            la tienda <strong>Play Store</strong>, entonces ya tienes una.
          </p>
          <p style={{ color: "var(--huap-texto)", fontSize: "18px", lineHeight: 1.6, marginTop: "12px" }}>
            Es tu correo que termina en <strong>@gmail.com</strong>. Prueba entrar con
            ese antes de crear uno nuevo.
          </p>
        </section>

        {/* Bloque 2 — cómo crear una */}
        <section
          className="w-full p-5 rounded-lg"
          style={{ backgroundColor: "white", border: "0.5px solid #E5E7EB" }}
        >
          <h2 style={{ color: "var(--huap-texto)", fontSize: "20px", fontWeight: 700, marginBottom: "8px" }}>
            Si no tienes: qué te va a pedir Google
          </h2>
          <p style={{ color: "var(--huap-texto)", fontSize: "18px", lineHeight: 1.6, marginBottom: "20px" }}>
            No importa en qué orden te los pida. Estos son los datos que necesitas
            tener listos:
          </p>

          <ul className="flex flex-col gap-5" style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {DATOS.map((dato) => (
              <li key={dato.titulo} style={{ display: "flex", gap: "14px", alignItems: "flex-start" }}>
                <div
                  aria-hidden="true"
                  style={{
                    width: "40px",
                    height: "40px",
                    borderRadius: "50%",
                    backgroundColor: "var(--huap-verde)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                  }}
                >
                  <Check size={22} color="#FFFFFF" strokeWidth={3} />
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <h3 style={{ color: "var(--huap-texto)", fontSize: "18px", fontWeight: 700, marginBottom: "4px" }}>
                    {dato.titulo}
                  </h3>
                  <p style={{ color: "var(--huap-texto)", fontSize: "18px", lineHeight: 1.6 }}>
                    {dato.texto}
                  </p>
                </div>
              </li>
            ))}
          </ul>

          {/* Consejos: no son pasos, son cosas que conviene saber antes de partir */}
          <div
            className="rounded-lg p-4"
            style={{ backgroundColor: "#F9FAFB", border: "0.5px solid #E5E7EB", marginTop: "24px" }}
          >
            <h3
              style={{
                color: "var(--huap-texto)",
                fontSize: "18px",
                fontWeight: 700,
                marginBottom: "12px",
                display: "flex",
                alignItems: "center",
                gap: "8px",
              }}
            >
              <Lightbulb size={22} color="var(--huap-azul)" strokeWidth={2.5} aria-hidden="true" />
              Consejos antes de empezar
            </h3>
            <ul className="flex flex-col gap-3" style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {CONSEJOS.map((consejo) => (
                <li
                  key={consejo}
                  style={{ color: "var(--huap-texto)", fontSize: "18px", lineHeight: 1.6, display: "flex", gap: "10px" }}
                >
                  <span aria-hidden="true" style={{ color: "var(--huap-azul)", fontWeight: 700 }}>•</span>
                  <span>{consejo}</span>
                </li>
              ))}
            </ul>
          </div>

          <a
            href="https://accounts.google.com/signup"
            target="_blank"
            rel="noopener noreferrer"
            className="w-full py-3 px-6 rounded-lg font-medium text-white"
            style={{
              backgroundColor: "var(--huap-azul)",
              fontSize: "18px",
              minHeight: "52px",
              marginTop: "24px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
              textDecoration: "none",
            }}
          >
            Abrir la página de Google
          </a>
          <p style={{ color: "#6B7280", fontSize: "16px", marginTop: "8px", textAlign: "center" }}>
            Se abre en una ventana nueva
          </p>
        </section>

        {/* Bloque 3 — ayuda de una persona */}
        <section
          className="w-full p-5 rounded-lg"
          style={{ backgroundColor: "white", border: "2px solid var(--huap-azul)" }}
        >
          <h2 style={{ color: "var(--huap-texto)", fontSize: "20px", fontWeight: 700, marginBottom: "12px" }}>
            ¿Prefieres que alguien te ayude?
          </h2>
          <p style={{ color: "var(--huap-texto)", fontSize: "18px", lineHeight: 1.6 }}>
            No tienes que hacerlo solo. Puedes pedir ayuda a un familiar de confianza,
            o acercarte al hospital y preguntar por el equipo de la plataforma.
          </p>
          {/* TODO (equipo HUAP): reemplazar por el contacto real — teléfono, mesón o correo. */}
          <p style={{ color: "var(--huap-texto)", fontSize: "18px", lineHeight: 1.6, marginTop: "12px" }}>
            Hospital de Urgencia Asistencia Pública — Posta Central
          </p>
        </section>

      </div>
    </main>
  )
}
