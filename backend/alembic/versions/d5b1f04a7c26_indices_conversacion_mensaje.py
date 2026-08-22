"""indices_conversacion_mensaje

Cada turno del chatbot consulta los mensajes recientes filtrando por
conversacion_id, y el historial lista las conversaciones filtrando por
usuario_id. Ninguna de las dos columnas estaba indexada, así que ambas
consultas hacían scan completo de la tabla.

Revision ID: d5b1f04a7c26
Revises: a4c8e2f6b193
Create Date: 2026-08-21

"""
from typing import Sequence, Union

from alembic import op

revision: str = 'd5b1f04a7c26'
down_revision: Union[str, None] = 'a4c8e2f6b193'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("ix_mensaje_chat_conversacion_id", "mensaje_chat", ["conversacion_id"])
    op.create_index("ix_conversacion_usuario_id", "conversacion", ["usuario_id"])


def downgrade() -> None:
    op.drop_index("ix_conversacion_usuario_id", table_name="conversacion")
    op.drop_index("ix_mensaje_chat_conversacion_id", table_name="mensaje_chat")
