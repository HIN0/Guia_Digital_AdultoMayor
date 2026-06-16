# Guía Digital · Adulto Mayor — Frontend

Plataforma educativa de IA y salud para personas mayores del **HUAP** (Hospital de Urgencia Asistencia Pública). Los usuarios aprenden a usar IA para entender información de salud de forma segura.

## Stack

- **Next.js 16.2.6** con App Router (no Pages Router)
- **React 19**, **TypeScript 5**
- **NextAuth v5 beta** (`next-auth@^5.0.0-beta.31`) — la API difiere de v4
- **TailwindCSS v4** — la config es `postcss.config.mjs`, no `tailwind.config.js`
- **Lucide React** para íconos
- **Backend**: FastAPI corriendo en `http://localhost:8000/api` (repo separado, no está en este directorio)

## Comandos esenciales

```bash
cd frontend
npm run dev       # desarrollo en localhost:3000
npm run build     # build de producción
npm run lint      # ESLint sobre todo el proyecto
```

## Variables de entorno necesarias

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api   # URL del backend
AUTH_SECRET=...                                  # NextAuth secret
AUTH_URL=http://localhost:3000                   # NextAuth URL
```

## Arquitectura de la aplicación

### Módulos educativos (secuenciales)

| Orden | Nombre | Lecciones | Flag localStorage |
|---|---|---|---|
| 1 | Entender qué es la IA | 6 | `huap_mod1_completado` |
| 2 | Practicar con la IA | 6 | `huap_mod2_completado` |
| 3 | Asistente de IA | 1 + chatbot | `huap_chatbot_desbloqueado` |

El desbloqueo es progresivo: Módulo 2 requiere Módulo 1 completo, el chatbot requiere Módulo 2 completo.

### Progreso en localStorage

```
huap_mod1_completado         → "true"
huap_mod2_completado         → "true"
huap_chatbot_desbloqueado    → "true"
huap_mod{id}_lecciones_completadas → JSON array de IDs de lecciones
```

### Chatbot

- Backend usa índice **FAISS** con preguntas/respuestas médicas validadas (whitelist)
- Tiene sistema de valoración de respuestas (thumbs up/down)
- Panel admin en `/admin/chatbot` para gestionar patologías y preguntas validadas
- El botón "Recargar FAISS" en admin reconstruye el índice semántico

### Rutas principales

```
/                    → redirect a /bienvenida o /inicio
/bienvenida          → onboarding para nuevos usuarios
/inicio              → home autenticado
/modulos             → lista de módulos
/modulos/[id]        → detalle del módulo con lecciones
/modulos/[id]/lecciones/[leccion_id] → lección individual
/quiz/[id]           → quiz final del módulo
/chatbot             → asistente de salud (requiere chatbot desbloqueado)
/progreso            → progreso del usuario e insignias
/ajustes             → configuración (tamaño de fuente, etc.)
/admin/chatbot       → panel admin (requiere rol admin)
```

## Convenciones de código

### Estilos

Se mezclan clases de Tailwind con estilos inline. Para componentes con mucha lógica visual se prefieren **inline styles** (más predecibles en componentes de cliente). Las CSS custom properties del tema son:

```css
--huap-azul     /* color primario */
--huap-rojo     /* alertas y errores */
--huap-verde    /* éxito y completado */
--huap-fondo    /* fondo de página */
--huap-texto    /* texto principal */
```

### Audiencia objetivo

Los usuarios son adultos mayores. Priorizar siempre:
- Texto grande (mínimo 16px en cuerpo)
- Contraste alto
- Lenguaje simple, sin jerga técnica
- Botones grandes y fáciles de tocar

### Autenticación

El token de sesión se accede como `(session as any)?.accessToken`. Es un JWT del backend Django/FastAPI que se pasa en el header `Authorization: Bearer {token}`.

### Tipos y API

- Todos los tipos del backend están en `src/lib/api.ts`
- Tipos de UI en `src/types/index.ts`
- Nunca hacer fetch directo fuera de `src/lib/api.ts` — agregar las funciones allí

## Estructura de archivos clave

```
src/
├── app/
│   ├── layout.tsx              ← layout raíz (NextAuth provider, NavTabs, FontSizeApplier)
│   ├── chatbot/page.tsx        ← chatbot de salud
│   ├── modulos/[id]/
│   │   └── lecciones/[leccion_id]/page.tsx
│   ├── quiz/[id]/page.tsx
│   ├── progreso/page.tsx
│   └── admin/chatbot/page.tsx  ← panel admin whitelist
├── components/
│   ├── layout/                 ← Header, NavTabs, Footer, SessionProvider, FontSizeApplier
│   └── modulos/ModuloCard.tsx
├── lib/
│   └── api.ts                  ← TODAS las llamadas al backend y sus tipos TypeScript
└── types/
    └── index.ts                ← tipos de UI (Modulo, EstadoModulo, AppRouteId)
```

## Insignias del sistema

| Nombre | Condición | Ícono |
|---|---|---|
| Conocedor de la IA | Completa Módulo 1 | 🧠 |
| Practicante de la IA | Completa Módulo 2 | 💪 |
| Asistente de IA | Completa Módulo 3 | 🤖 |
