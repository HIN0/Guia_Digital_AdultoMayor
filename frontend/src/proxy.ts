import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function proxy(request: NextRequest) {
  const sessionToken =
    request.cookies.get("authjs.session-token") ||
    request.cookies.get("__Secure-authjs.session-token")

  const isProtectedRoute =
    request.nextUrl.pathname.startsWith("/modulos") ||
    request.nextUrl.pathname.startsWith("/quiz") ||
    request.nextUrl.pathname.startsWith("/chatbot") ||
    request.nextUrl.pathname.startsWith("/perfil")

  if (isProtectedRoute && !sessionToken) {
    return NextResponse.redirect(new URL("/login", request.nextUrl))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/modulos/:path*", "/quiz/:path*", "/chatbot/:path*", "/perfil/:path*"],
}