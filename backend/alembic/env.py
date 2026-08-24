from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# ── Configuración de Alembic ─────────────────────────────────────────────────
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── Importar settings y modelos ───────────────────────────────────────────────
# Importamos settings para leer DATABASE_URL desde .env
from core.config import settings  # noqa: E402

# Importamos Base y TODOS los módulos de entidades para que SQLAlchemy
# registre los modelos antes de que Alembic compare contra la BD.
# Si agregas un nuevo módulo con modelos, agrégalo aquí también.
from core.database import Base  # noqa: E402
from modules.auth import entity as _auth  # noqa: E402, F401
from modules.chatbot import entity as _chatbot  # noqa: E402, F401
from modules.educacion import entity as _educacion  # noqa: E402, F401
from modules.progreso import entity as _progreso  # noqa: E402, F401

# Inyectamos la URL desde .env (no desde alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# target_metadata le dice a Alembic qué tablas/columnas debería existir
target_metadata = Base.metadata


# ── Modo offline (genera SQL sin conectarse a la BD) ─────────────────────────
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Modo online (se conecta y aplica los cambios) ────────────────────────────
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
