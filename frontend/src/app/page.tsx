import Image from "next/image";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-huap-fondo">

      <main className="mx-auto flex w-full max-w-sm flex-1 flex-col items-center gap-6 px-6 py-10 sm:max-w-lg">

        <div className="flex flex-col items-center gap-3 pt-6">
          <Image
            src="/logo-huap.png"
            alt="Logo del Hospital de Urgencia Asistencia Pública"
            width={110}
            height={110}
            priority
            className="h-24 w-24 sm:h-28 sm:w-28"
          />
          <div className="text-center">
            <h1 className="text-3xl font-medium text-huap-azul sm:text-4xl">
              IA y Salud
            </h1>
            <p className="mt-1 text-sm text-zinc-500 sm:text-base">
              Hospital de Urgencia Asistencia Pública
            </p>
          </div>
        </div>

        <p className="text-center text-lg leading-relaxed text-huap-texto sm:text-xl">
          Aprende a usar la inteligencia artificial para entender información
          de salud de forma segura.
        </p>

        <div
          role="note"
          aria-label="Aviso sobre la plataforma"
          className="w-full border-l-4 border-huap-verde bg-white px-4 py-4 rounded-r-2xl"
        >
          <p className="text-center text-base leading-relaxed text-huap-verde sm:text-lg">
            Esta aplicación te enseña paso a paso.{" "}
            <strong className="font-medium">
              No necesitas experiencia previa.
            </strong>
          </p>
        </div>

        <div className="flex w-full flex-col gap-3 pt-1">
          <button
            type="button"
            className="flex items-center justify-center gap-3 rounded-2xl bg-huap-azul px-6 py-4 text-lg font-medium text-white transition-colors hover:bg-[#163d5e] active:scale-95"
          >
            <svg aria-hidden="true" className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21.35 11.1h-9.17v2.93h6.5c-.28 3-2.83 4.27-6.48 4.27-3.92 0-7.07-2.85-7.07-6.84 0-3.99 3.15-6.84 7.07-6.84 1.7 0 3.21.57 4.42 1.68l2.39-2.39C16.91 1.74 14.7.79 12.18.79 6.97.79 2.7 4.84 2.7 11.45c0 6.62 4.27 10.66 9.48 10.66 5.7 0 9.84-3.83 9.84-9.62 0-.51-.06-.93-.17-1.39z" />
            </svg>
            Entrar con Google
          </button>

          <button
            type="button"
            className="rounded-2xl border-2 border-huap-azul bg-white px-6 py-4 text-lg font-medium text-huap-azul transition-colors hover:bg-huap-gris-suave active:scale-95"
          >
            Necesito ayuda
          </button>
        </div>

        <p className="text-xs text-zinc-400">
          Plataforma en desarrollo · Sprint 1
        </p>

      </main>

      <footer className="border-t border-huap-gris-suave bg-white py-4">
        <p className="text-center text-sm text-zinc-600">
          Hospital de Urgencia Asistencia Pública · Posta Central
        </p>
      </footer>

    </div>
  );
}