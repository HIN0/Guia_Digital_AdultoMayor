"""secciones_en_mensaje_chat

Guarda con cada respuesta del LLM los títulos de las secciones del conocimiento
que se usaron para generarla. Sin esto, una respuesta valorada negativamente en
el panel de revisión no se puede auditar: no queda registro de con qué contexto
respondió el bot.

Revision ID: f2c9e17b4a83
Revises: d5b1f04a7c26
Create Date: 2026-08-21

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = 'f2c9e17b4a83'
down_revision: Union[str, None] = 'd5b1f04a7c26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("mensaje_chat", sa.Column("secciones", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("mensaje_chat", "secciones")
