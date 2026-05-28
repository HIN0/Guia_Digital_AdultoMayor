from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine, SessionLocal

# Importamos las entidades para que SQLAlchemy las registre antes de crear tablas
from modules.auth import entity as auth_entity
from modules.educacion import entity as educacion_entity
from modules.progreso import entity as progreso_entity
#from modules.chatbot import entity as chatbot_entity

# Importamos los routers (controllers) de cada módulo
from modules.auth.controller import router as auth_router
from modules.educacion.controller import router as educacion_router
from modules.progreso.controller import router as progreso_router
#from modules.chatbot.controller import router as chatbot_router
#from modules.admin.controller import router as admin_router

# Crea las tablas en PostgreSQL si no existen (útil en desarrollo)
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        if db.query(educacion_entity.Modulo).count() == 0:
            from seed import poblar
            print("⏳ Base de datos vacía — poblando con seed...")
            poblar(db)
    except Exception as e:
        db.rollback()
        print(f"❌ Error en auto-seed: {e}")
    finally:
        db.close()
    yield


app = FastAPI(
    title="Guía Digital Adulto Mayor - API",
    description="API educativa de IA y Salud para personas mayores",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS: permite que el frontend (React/Next) llame a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ajusta a la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registramos todos los routers bajo el prefijo /api
app.include_router(auth_router, prefix="/api")
app.include_router(educacion_router, prefix="/api")
app.include_router(progreso_router, prefix="/api")
#app.include_router(chatbot_router, prefix="/api")
#app.include_router(admin_router, prefix="/api")


@app.get("/")
def root():
    return {"mensaje": "API funcionando. Visita /docs para ver la documentación."}
