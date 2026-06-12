from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine, SessionLocal

from modules.auth import entity as auth_entity
from modules.educacion import entity as educacion_entity
from modules.progreso import entity as progreso_entity
from modules.chatbot import entity as chatbot_entity

from modules.auth.controller import router as auth_router
from modules.educacion.controller import router as educacion_router
from modules.progreso.controller import router as progreso_router
from modules.chatbot.controller import router as chatbot_router
from modules.chatbot.service import inicializar_chatbot

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Seed educativo (módulos y lecciones)
    db = SessionLocal()
    try:
        if db.query(educacion_entity.Modulo).count() == 0:
            from seed import poblar
            print("⏳ Base de datos vacía — poblando con seed educativo...")
            poblar(db)
    except Exception as e:
        db.rollback()
        print(f"❌ Error en auto-seed educativo: {e}")
    finally:
        db.close()

    # 2. Seed whitelist chatbot (idempotente, va ANTES del FAISS)
    try:
        from modules.chatbot.seed import seed_chatbot
        seed_chatbot()
    except Exception as e:
        print(f"⚠️  Error en seed del chatbot: {e}")

    # 3. Inicializar FAISS (ya con la whitelist poblada)
    print("⏳ Cargando base de conocimiento del chatbot...")
    try:
        inicializar_chatbot()
        print("✅ Chatbot listo.")
    except Exception as e:
        print(f"⚠️  Chatbot no pudo inicializarse: {e}")

    yield


app = FastAPI(
    title="Guía Digital Adulto Mayor - API",
    description="API educativa de IA y Salud para personas mayores",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
