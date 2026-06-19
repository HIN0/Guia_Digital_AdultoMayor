import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import Credentials from "next-auth/providers/credentials"

// URL base del backend. En producción se define con NEXT_PUBLIC_API_URL
// (ej: https://<tu-space>.hf.space/api). En local cae a localhost:8000.
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api"

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Google,
    Credentials({
      name: "guest",
      credentials: {},
      async authorize() {
        try {
          const response = await fetch(`${API_URL}/auth/invitado`, {
            method: "POST",
          })
          if (!response.ok) return null
          const data = await response.json()
          return {
            id: String(data.usuario.id),
            name: data.usuario.nombre,
            email: data.usuario.email,
            backendToken: data.access_token,
          }
        } catch {
          return null
        }
      },
    }),
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

    async jwt({ token, account, user }) {
      if (account?.backend_access_token) {
        token.accessToken = account.backend_access_token;
      }
      // Para el proveedor de invitado (Credentials), el token viene en user
      if (account?.provider === "credentials" && user && (user as Record<string, unknown>).backendToken) {
        token.accessToken = (user as Record<string, unknown>).backendToken;
      }
      return token;
    },

    async session({ session, token }) {
      // @ts-expect-error (evitar error tipado si no has extendido los types de NextAuth)
      session.accessToken = token.accessToken;
      return session;
    }
  },
  session: {
    strategy: "jwt",
  },
})
