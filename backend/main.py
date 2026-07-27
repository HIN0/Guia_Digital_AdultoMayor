import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine, SessionLocal
from modules.auth import entity as auth_entity
from modules.auth.controller import router as auth_router
from modules.chatbot import entity as chatbot_entity
from modules.chatbot.controller import router as chatbot_router
from modules.chatbot.service import inicializar_chatbot
from modules.educacion import entity as educacion_entity
from modules.educacion.controller import router as educacion_router
from modules.progreso import entity as progreso_entity
from modules.progreso.controller import router as progreso_router

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Seed educativo (módulos y lecciones)
    db = SessionLocal()
    try:
        if db.query(educacion_entity.Modulo).count() == 0:
            from seed import poblar
            logger.info("Base de datos vacía — poblando con seed educativo...")
            poblar(db)
    except Exception as e:
        db.rollback()
        logger.error("Error en auto-seed educativo: %s", e)
    finally:
        db.close()

    # 2. Seed whitelist chatbot (idempotente, va ANTES del FAISS)
    try:
        from modules.chatbot.seed import seed_chatbot
        seed_chatbot()
    except Exception as e:
        logger.warning("Error en seed del chatbot: %s", e)

    # 3. Inicializar FAISS (ya con la whitelist poblada)
    logger.info("Cargando base de conocimiento del chatbot...")
    try:
        inicializar_chatbot()
        logger.info("Chatbot listo.")
    except Exception as e:
        logger.warning("Chatbot no pudo inicializarse: %s", e)

    yield


_en_desarrollo = os.getenv("ENVIRONMENT", "production") == "development"

app = FastAPI(
    title="Guía Digital Adulto Mayor - API",
    description="API educativa de IA y Salud para personas mayores",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if _en_desarrollo else None,
    redoc_url="/redoc" if _en_desarrollo else None,
)

# Orígenes permitidos para CORS.
# En local usa http://localhost:3000; en producción define ALLOWED_ORIGINS
# como lista separada por comas, ej:
#   ALLOWED_ORIGINS=https://mi-app.vercel.app,http://localhost:3000
_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [o.strip() for o in _origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(educacion_router, prefix="/api")
app.include_router(progreso_router, prefix="/api")
app.include_router(chatbot_router, prefix="/api")


@app.get("/")
def root():
    return {"mensaje": "API funcionando. Visita /docs para ver la documentación."}


@app.get("/health")
def health():
    """Endpoint liviano para el ping anti-sueño (no toca la base de datos)."""
    return {"status": "ok"}
