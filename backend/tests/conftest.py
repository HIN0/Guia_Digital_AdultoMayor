"""Configuración de pytest: agrega backend/ al sys.path para poder importar
los paquetes del proyecto (modules, core) igual que lo hace main.py.

Ejecutar desde la carpeta backend/:  python -m pytest tests/ -v
Requiere:  pip install pytest
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Valores dummy para que Settings() (backend/core/config.py) no falle si no
# hay backend/.env disponible (p.ej. en CI). Si ya existe un .env real o
# variables de entorno reales, esas tienen prioridad y estas no se usan.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("GOOGLE_CLIENT_ID", "test-client-id.apps.googleusercontent.com")
os.environ.setdefault("GOOGLE_CLIENT_SECRET", "test-client-secret")
os.environ.setdefault("SECRET_KEY", "test-secret-key-solo-para-pytest")

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.database import Base, get_db

# Importar todas las entidades para que se registren en Base.metadata
# antes de crear las tablas de prueba.
from modules.auth import entity as auth_entity  # noqa: F401
from modules.chatbot import entity as chatbot_entity  # noqa: F401
from modules.educacion import entity as educacion_entity  # noqa: F401
from modules.progreso import entity as progreso_entity  # noqa: F401


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    """El Limiter de slowapi es un singleton en memoria a nivel de proceso.
    Sin este reset, todos los tests comparten los mismos contadores (el
    TestClient siempre reporta la misma IP), y tests de rate limiting
    contaminarían a los demás."""
    from core.rate_limit import limiter

    limiter.reset()
    yield


@pytest.fixture()
def db_session():
    """Sesión SQLAlchemy sobre una base SQLite en memoria, aislada por test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def client(db_session):
    """TestClient con solo los routers de auth y progreso (evita levantar
    el chatbot/FAISS del lifespan de main.py) y con get_db() apuntando a la
    base de datos de prueba en memoria."""
    from modules.auth.controller import router as auth_router
    from modules.progreso.controller import router as progreso_router

    app = FastAPI()
    app.include_router(auth_router, prefix="/api")
    app.include_router(progreso_router, prefix="/api")

    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def crear_usuario(db_session):
    """Factory para crear un Usuario directo en la BD de prueba."""
    from modules.auth.entity import RolUsuario, Usuario

    def _crear(
        google_id="google-123", email="ana@example.com", nombre="Ana",
        rol=RolUsuario.alumno,
    ):
        usuario = Usuario(
            google_id=google_id, email=email, nombre=nombre, rol=rol,
        )
        db_session.add(usuario)
        db_session.commit()
        db_session.refresh(usuario)
        return usuario

    return _crear


@pytest.fixture()
def token_para(db_session):
    """Factory que genera un JWT válido para un usuario dado (como si hubiera
    pasado por /auth/login)."""
    from core.security import create_access_token

    def _token(usuario):
        return create_access_token({"sub": str(usuario.id), "rol": usuario.rol.value})

    return _token


@pytest.fixture()
def crear_estructura_modulo(db_session):
    """Factory para armar un módulo educativo completo (lecciones + quiz +
    preguntas + opciones) usado por los tests de progreso."""
    from modules.educacion.entity import (
        Leccion,
        Modulo,
        OpcionRespuesta,
        PreguntaQuiz,
        QuizFinal,
    )

    def _crear(
        orden, nombre=None, requiere_modulo_previo=False,
        n_lecciones=2, con_quiz=False, quiz_bloqueante=False, minimo_aciertos=1,
    ):
        modulo = Modulo(
            nombre=nombre or f"Módulo {orden}",
            orden=orden,
            requiere_modulo_previo=requiere_modulo_previo,
        )
        db_session.add(modulo)
        db_session.commit()
        db_session.refresh(modulo)

        lecciones = []
        for i in range(1, n_lecciones + 1):
            leccion = Leccion(
                modulo_id=modulo.id, titulo=f"Lección {i}", orden=i,
                contenido={"concepto": "..."},
            )
            db_session.add(leccion)
            lecciones.append(leccion)
        db_session.commit()
        for leccion in lecciones:
            db_session.refresh(leccion)

        quiz = None
        pregunta = None
        opcion_correcta = None
        opcion_incorrecta = None
        if con_quiz:
            quiz = QuizFinal(
                modulo_id=modulo.id, minimo_aciertos=minimo_aciertos,
                bloqueante=quiz_bloqueante,
            )
            db_session.add(quiz)
            db_session.commit()
            db_session.refresh(quiz)

            pregunta = PreguntaQuiz(
                quiz_final_id=quiz.id, enunciado="¿2 + 2?", feedback="Repasa la suma.",
            )
            db_session.add(pregunta)
            db_session.commit()
            db_session.refresh(pregunta)

            opcion_correcta = OpcionRespuesta(
                pregunta_id=pregunta.id, texto="4", es_correcta=True,
            )
            opcion_incorrecta = OpcionRespuesta(
                pregunta_id=pregunta.id, texto="5", es_correcta=False,
            )
            db_session.add_all([opcion_correcta, opcion_incorrecta])
            db_session.commit()
            db_session.refresh(opcion_correcta)
            db_session.refresh(opcion_incorrecta)

        return {
            "modulo": modulo,
            "lecciones": lecciones,
            "quiz": quiz,
            "pregunta": pregunta,
            "opcion_correcta": opcion_correcta,
            "opcion_incorrecta": opcion_incorrecta,
        }

    return _crear


@pytest.fixture()
def crear_insignia(db_session):
    from modules.progreso.entity import Insignia

    def _crear(nombre, descripcion="desc", icono_url="http://x/icono.png"):
        insignia = Insignia(nombre=nombre, descripcion=descripcion, icono_url=icono_url)
        db_session.add(insignia)
        db_session.commit()
        db_session.refresh(insignia)
        return insignia

    return _crear


# ── Fixtures del chatbot ─────────────────────────────────────────────────────
# Compartidas por test_whitelist.py y test_conversacion_multiturno.py.
# Perezosas: el modelo de embeddings (~470 MB) solo se carga si un test las pide.

@pytest.fixture(scope="module")
def embeddings():
    pytest.importorskip("langchain_huggingface")
    pytest.importorskip("langchain_community")
    from langchain_huggingface import HuggingFaceEmbeddings

    # Misma configuración que service._get_embeddings (normalización incluida)
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        encode_kwargs={"normalize_embeddings": True},
    )


@pytest.fixture(scope="module")
def pregunta_store(embeddings):
    from langchain_community.vectorstores import FAISS

    from modules.chatbot.seeds import SEED_DATA

    texts, metadatas = [], []
    for i, (patologia, preguntas) in enumerate(SEED_DATA.items()):
        for item in preguntas:
            for texto in [item["pregunta"]] + item.get("variantes", []):
                texts.append(texto)
                metadatas.append({
                    "patologia": patologia,
                    "respuesta": item["respuesta"],
                    "pregunta_id": i,  # placeholder: en producción es el id de BD
                })
    return FAISS.from_texts(texts, embeddings, metadatas=metadatas)


@pytest.fixture(scope="module")
def service_configurado(embeddings, pregunta_store):
    """Configura los índices de service desde los seeds (sin base de datos)
    para poder testear la lógica real de _buscar_en_whitelist y los umbrales."""
    _service = pytest.importorskip(
        "modules.chatbot.service",
        reason="modules.chatbot.service no importable (falta .env o dependencias)",
    )
    from langchain_community.vectorstores import FAISS

    from modules.chatbot.normalizacion import normalizar_texto
    from modules.chatbot.seeds import SEED_DATA

    ruta = os.path.join(os.path.dirname(_service.__file__), "data", "conocimiento.txt")
    with open(ruta, encoding="utf-8") as f:
        chunks = _service._dividir_por_secciones(f.read())
    knowledge = FAISS.from_texts(
        chunks, embeddings, metadatas=_service.metadatas_de_chunks(chunks)
    )

    lookup = {}
    for i, preguntas in enumerate(SEED_DATA.values()):
        for item in preguntas:
            for texto in [item["pregunta"]] + item.get("variantes", []):
                lookup[normalizar_texto(texto)] = (i, item["respuesta"])

    anterior = (
        _service._pregunta_store,
        _service._knowledge_store,
        _service._exact_lookup,
        _service._retriever,
    )
    _service._pregunta_store = pregunta_store
    _service._knowledge_store = knowledge
    _service._exact_lookup = lookup
    # Mismo k que inicializar_base_conocimiento, para que los tests de
    # recuperación ejerciten el retriever real y no una réplica.
    _service._retriever = knowledge.as_retriever(search_kwargs={"k": 3})
    yield _service
    (
        _service._pregunta_store,
        _service._knowledge_store,
        _service._exact_lookup,
        _service._retriever,
    ) = anterior


@pytest.fixture()
def bot(service_configurado, db_session, crear_usuario, monkeypatch):
    """Ejecuta generar_y_guardar_respuesta de verdad (SQLite en memoria) con el
    LLM reemplazado por un doble que registra con qué consulta se recuperó."""
    from types import SimpleNamespace

    usuario = crear_usuario(email="abuela@example.com")
    llamadas = []

    def _llm_doble(pregunta, historial, tema=None):
        llamadas.append({"pregunta": pregunta, "historial": historial, "tema": tema})
        return "Respuesta del modelo.", ["NEUMONÍA ADQUIRIDA EN LA COMUNIDAD — Síntomas"]

    monkeypatch.setattr(service_configurado, "_invocar_llm", _llm_doble)
    service_configurado._llm_cache.clear()

    estado = {"conversacion_id": None}

    def _preguntar(texto):
        resultado = service_configurado.generar_y_guardar_respuesta(
            db=db_session,
            usuario_id=usuario.id,
            pregunta=texto,
            conversacion_id=estado["conversacion_id"],
        )
        estado["conversacion_id"] = resultado["conversacion_id"]
        return resultado

    return SimpleNamespace(preguntar=_preguntar, llamadas=llamadas)
