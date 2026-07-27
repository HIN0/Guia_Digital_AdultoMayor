import { auth } from "@/auth"

// "/" requiere coincidencia exacta porque startsWith("/") es verdadero para TODA ruta
const RUTAS_PUBLICAS_PREFIJO = ["/bienvenida", "/login", "/api/auth"]

export default auth((req) => {
  const { pathname } = req.nextUrl

  const esPublica =
    pathname === "/" ||
    RUTAS_PUBLICAS_PREFIJO.some((ruta) => pathname.startsWith(ruta))

  if (!esPublica && !req.auth) {
    return Response.redirect(new URL("/", req.nextUrl.origin))
  }
})

export const config = {
  // Excluir: chunks de Next.js, optimizador de imágenes, favicon,
  // y archivos estáticos de /public (svg, png, mp3, etc.)
  matcher: [
    "/((?!_next/static|_next/image|favicon\\.ico|icons/|.*\\.(?:svg|png|jpg|jpeg|gif|mp3|mp4|webp|ico|woff|woff2|ttf|eot)$).*)",
  ],
}
