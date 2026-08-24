# Guía Digital Adulto Mayor

Plataforma educativa de IA y salud para adultos mayores del HUAP. Permite a los usuarios completar módulos de aprendizaje y consultar un asistente de salud con IA.

## Estructura del repositorio

```
.
├── backend/                 ← API FastAPI (Python). Ver backend/README.md
├── frontend/                ← Next.js 16 + React 19. Ver frontend/README.md
├── docker-compose.yml       ← Postgres + backend + frontend para desarrollo local
└── docker-compose.prod.yml  ← Los tres servicios para el servidor de producción
```

Cada carpeta tiene su propio README con instrucciones detalladas de instalación, variables de entorno y stack:

- [`backend/README.md`](backend/README.md) — API FastAPI: arquitectura por capas, cómo levantar el servidor, Alembic.
- [`frontend/README.md`](frontend/README.md) — Next.js: variables de entorno, comandos, estructura de carpetas.

## Levantar el proyecto completo en local

### Opción A — Docker Compose (recomendada)

Levanta los tres servicios de una vez.

```bash
# Desde la raíz del repo, con backend/.env y frontend/.env.local ya creados
docker compose up --build
```

| Servicio | Dirección |
|---|---|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000 |
| Postgres | localhost:5432 |

Las tablas y el seed educativo se crean automáticamente al iniciar.

El primer build tarda varios minutos: el backend pre-descarga el modelo de embeddings del chatbot (~470 MB) y el frontend compila la aplicación. Los arranques posteriores son de segundos.

### Opción B — Frontend en modo desarrollo

El contenedor del frontend sirve la aplicación ya compilada, así que no refleja cambios en el código mientras programas. Para desarrollar, levanta en Docker solo la base de datos y el backend:

```bash
docker compose up db backend
```

y el frontend aparte, con recarga en caliente:

```bash
cd frontend
npm install
npm run dev
```

### Opción C — Todo nativo (sin Docker)

Sigue las instrucciones de [`backend/README.md`](backend/README.md) (Python + Postgres local) y luego [`frontend/README.md`](frontend/README.md) (Node.js).

## Despliegue en producción

El despliegue se realiza en servidor propio con Docker. `docker-compose.prod.yml` levanta los tres servicios:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Backend y frontend escuchan solo en `127.0.0.1`: nginx hace de proxy inverso y es quien expone el sitio hacia afuera con TLS. Postgres no se publica fuera de la red interna de Docker.

**Importante:** las variables `NEXT_PUBLIC_*` se hornean dentro del build de Next.js. Si cambia el dominio público hay que reconstruir la imagen del frontend; reiniciar el contenedor no basta.

El procedimiento completo —credenciales, configuración de OAuth, dominio, variables
de entorno y puesta en marcha— está documentado en
[`docs/Guia_traspaso_tecnico_HUAP.docx`](docs/Guia_traspaso_tecnico_HUAP.docx).

## Tests y análisis estático

```bash
# Backend
cd backend
pytest tests/ -v
ruff check .

# Frontend
cd frontend
npm run lint
npm run test
```
