import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

// URL base del backend. En producción se define con NEXT_PUBLIC_API_URL
// (ej: https://<tu-space>.hf.space/api). En local cae a localhost:8000.
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api"

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
