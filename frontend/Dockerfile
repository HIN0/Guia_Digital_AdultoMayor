# Imagen de contenedor del frontend Next.js.
#
# Build multi-etapa: las dependencias de desarrollo y los artefactos de
# compilación quedan en etapas intermedias que no viajan a la imagen final.
# Requiere output: "standalone" en next.config.ts.

# ── Etapa 1: dependencias ────────────────────────────────────────────────────
FROM node:24-alpine AS deps
# libc6-compat: algunas dependencias nativas de Next lo necesitan en Alpine
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# ── Etapa 2: compilación ─────────────────────────────────────────────────────
FROM node:24-alpine AS builder
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# IMPORTANTE: las variables NEXT_PUBLIC_* se hornean DURANTE EL BUILD; no se
# leen en tiempo de ejecución. Si cambia el dominio del backend hay que
# reconstruir la imagen, no basta con reiniciar el contenedor.
# El valor por defecto sirve para desarrollo local; en producción lo inyecta
# docker-compose.prod.yml vía build args.
ARG NEXT_PUBLIC_API_URL=http://localhost:8000/api
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# NextAuth exige que AUTH_SECRET exista durante la compilación. Este valor es
# solo un relleno para que el build no falle: el secreto real se inyecta en
# tiempo de ejecución desde frontend/.env y nunca queda dentro de la imagen.
ENV AUTH_SECRET=build-time-placeholder

RUN npm run build

# ── Etapa 3: ejecución ───────────────────────────────────────────────────────
FROM node:24-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production \
    PORT=3000 \
    HOSTNAME=0.0.0.0

# Se ejecuta como usuario no-root, igual que el backend
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000

CMD ["node", "server.js"]
