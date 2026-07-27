# Frontend — Guía Digital Adulto Mayor (Next.js)

Plataforma educativa de IA y salud para adultos mayores del HUAP. Permite a los usuarios completar módulos de aprendizaje y consultar un asistente de salud con IA.

## Requisitos previos

- Node.js 20+
- Backend FastAPI corriendo (ver `../backend/README.md`)

## Instalación

```bash
cd frontend
npm install
```

## Variables de entorno

Copiar `.env.example` a `.env.local` y completar los valores:

```bash
cp .env.example .env.local
```

| Variable | Descripción | Ejemplo local |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | URL del backend FastAPI | `http://localhost:8000/api` |
| `AUTH_GOOGLE_ID` | Client ID de Google OAuth | Ver Google Cloud Console |
| `AUTH_GOOGLE_SECRET` | Client Secret de Google OAuth | Ver Google Cloud Console |
| `AUTH_SECRET` | Clave secreta para NextAuth | Generar con `openssl rand -hex 32` |
| `AUTH_URL` | URL pública del frontend | `http://localhost:3000` |

> Las credenciales de Google OAuth (`AUTH_GOOGLE_ID` y `AUTH_GOOGLE_SECRET`) son las **mismas** que usa el backend.

## Levantar en desarrollo

```bash
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000).

## Otros comandos

```bash
npm run build   # build de producción
npm run lint    # análisis estático con ESLint
npm run start   # servidor de producción (requiere build previo)
```

## Stack

- **Next.js 16** con App Router
- **React 19**, **TypeScript 5**
- **NextAuth v5 beta** para autenticación con Google
- **TailwindCSS v4**

## Estructura principal

```
src/
├── app/                  ← páginas (App Router)
│   ├── modulos/[id]/lecciones/[leccion_id]/page.tsx
│   ├── quiz/[id]/page.tsx
│   ├── chatbot/page.tsx
│   └── progreso/page.tsx
├── components/layout/    ← Header, NavTabs, Footer, SessionProvider
├── lib/api.ts            ← todas las llamadas al backend y sus tipos
└── auth.ts               ← configuración de NextAuth
```
