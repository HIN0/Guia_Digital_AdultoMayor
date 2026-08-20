# Guía Digital Adulto Mayor

Plataforma educativa de IA y salud para adultos mayores del HUAP. Permite a los usuarios completar módulos de aprendizaje y consultar un asistente de salud con IA.

## Estructura del repositorio

```
.
├── backend/    ← API FastAPI (Python). Ver backend/README.md
├── frontend/   ← Next.js 16 + React 19. Ver frontend/README.md
└── docker-compose.yml  ← Postgres + backend para desarrollo local
```

Cada carpeta tiene su propio README con instrucciones detalladas de instalación, variables de entorno y stack:

- [`backend/README.md`](backend/README.md) — API FastAPI: arquitectura por capas, cómo levantar el servidor, Alembic.
- [`frontend/README.md`](frontend/README.md) — Next.js: variables de entorno, comandos, estructura de carpetas.

## Levantar el proyecto completo en local

Hay dos formas de levantar el backend + base de datos:

### Opción A — Docker Compose (recomendada, backend + Postgres en contenedores)

```bash
# Desde la raíz del repo, con backend/.env ya creado (ver backend/README.md paso 3)
docker compose up --build
```

Esto levanta Postgres en `localhost:5432` y el backend en `localhost:8000`. Las tablas y el seed educativo se crean automáticamente al iniciar.

### Opción B — Todo nativo (sin Docker)

Sigue las instrucciones de [`backend/README.md`](backend/README.md) (Python + Postgres local) y luego [`frontend/README.md`](frontend/README.md) (Node.js).

### Frontend

En ambos casos, el frontend se levanta aparte (no está incluido en `docker-compose.yml`):

```bash
cd frontend
npm install
npm run dev
```

## Despliegue en producción

- **Backend**: Hugging Face Spaces (Docker SDK) — ver `backend/Dockerfile`.
- **Frontend**: Vercel.

## Tests y análisis estático

```bash
# Backend
cd backend
pytest tests/ -v
ruff check .

# Frontend
cd frontend
npm run lint
```
