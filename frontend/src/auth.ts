import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

// URL base del backend para las llamadas que hace el SERVIDOR de Next.js
// (este archivo se ejecuta solo en el servidor, nunca en el navegador).
//
// Dentro de Docker no sirve NEXT_PUBLIC_API_URL: esa apunta al dominio que
// resuelve el NAVEGADOR del usuario, y desde el contenedor del frontend
// "localhost" es el propio contenedor, no el backend. Por eso se usa
// BACKEND_INTERNAL_URL, que apunta al nombre del servicio de Docker
// (http://backend:7860/api). Fuera de Docker no se define y cae a las
// alternativas siguientes.
const API_URL =
  process.env.BACKEND_INTERNAL_URL ??
  process.env.NEXT_PUBLIC_API_URL ??
  "http://localhost:8000/api"

// El JWT propio del backend expira en ACCESS_TOKEN_EXPIRE_MINUTES (60 min por
// defecto), pero la sesión de NextAuth dura mucho más — sin esto, pasada 1h
// todas las llamadas a la API empiezan a fallar con 401 en silencio hasta que
// el usuario vuelve a iniciar sesión.
function decodificarJwt(jwt: string): Record<string, unknown> | null {
  try {
    const [, payload] = jwt.split(".")
    // Los JWT usan base64url (- y _ en lugar de + y /); atob() requiere base64 estándar
    const base64 = payload.replace(/-/g, "+").replace(/_/g, "/")
    return JSON.parse(atob(base64))
  } catch {
    return null
  }
}

function estaPorExpirar(jwt: string, margenSegundos = 300): boolean {
  const payload = decodificarJwt(jwt)
  const exp = payload?.exp
  if (typeof exp !== "number") return true
  return Date.now() / 1000 > exp - margenSegundos
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Google,
  ],
  pages: {
    signIn: "/login",
  },
  callbacks: {
    async signIn({ account }) {
      if (account?.provider === "google" && account.id_token) {
        try {
          const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ google_token: account.id_token }),
          });

          if (!response.ok) {
            const errorText = await response.text();
            console.error("Backend error status:", response.status, errorText);
            return false;
          }

          const data = await response.json();
          (account as Record<string, unknown>).backend_access_token = data.access_token;

          return true;
        } catch (error) {
          console.error("Error de conexión con el backend:", error);
          return false;
        }
      }
      return true;
    },

    async jwt({ token, account }) {
      if (account?.backend_access_token) {
        const accessToken = account.backend_access_token as string
        token.accessToken = accessToken;
        token.rol = (decodificarJwt(accessToken)?.rol as string) ?? "alumno"
        return token;
      }

      if (typeof token.accessToken === "string" && estaPorExpirar(token.accessToken)) {
        try {
          const response = await fetch(`${API_URL}/auth/refresh`, {
            method: "POST",
            headers: { Authorization: `Bearer ${token.accessToken}` },
          });
          if (response.ok) {
            const data = await response.json();
            token.accessToken = data.access_token;
            token.rol = (decodificarJwt(data.access_token)?.rol as string) ?? token.rol;
          }
          // Si el refresh falla (token ya vencido, backend caído, etc.) se
          // deja el token actual: las llamadas a la API fallarán con 401 y
          // el usuario deberá volver a iniciar sesión.
        } catch (error) {
          console.error("Error al renovar el token del backend:", error);
        }
      }

      return token;
    },

    async session({ session, token }) {
      // @ts-expect-error -- no se extendieron los types de NextAuth para accessToken
      session.accessToken = token.accessToken;
      // @ts-expect-error -- no se extendieron los types de NextAuth para rol
      session.rol = token.rol;
      return session;
    }
  },
  session: {
    strategy: "jwt",
  },
})
