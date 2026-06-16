import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [Google],
  pages: {
    signIn: "/login",
  },
  callbacks: {
    async signIn({ account }) {
      if (account?.provider === "google" && account.id_token) {
        try {
          // Se verifica la URL correcta. CON http://localhost:8000//api/auth/login 
          const response = await fetch("http://localhost:8000/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ google_token: account.id_token }),
          });

          // Si el status HTTP no es 2xx, bloquea el login y muestra el error
          if (!response.ok) {
            const errorText = await response.text();
            console.error("Backend error status:", response.status, errorText);
            return false; 
          }

          const data = await response.json();
          
          // Guardamos el token propio del backend dentro del objeto account temporalmente
          // para pasarlo al callback de jwt
          (account as Record<string, unknown>).backend_access_token = data.access_token;
          
          return true;
        } catch (error) {
          console.error("Error de conexión con el backend:", error);
          return false;
        }
      }
      return true;
    },

    // El callback jwt recibe el account cuando el usuario inicia sesión
    async jwt({ token, account }) {
      // Si account.backend_access_token existe, lo inyectamos en el token de la sesión
      if (account?.backend_access_token) {
        token.accessToken = account.backend_access_token;
      }
      return token;
    },

    // El callback session expone los datos al cliente (frontend)
    async session({ session, token }) {
      // @ts-expect-error (evitar error tipado si no has extendido los types de NextAuth)
      session.accessToken = token.accessToken;
      return session;
    }
  },
})