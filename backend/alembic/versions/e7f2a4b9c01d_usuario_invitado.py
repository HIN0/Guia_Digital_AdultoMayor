"""usuario_invitado

Revision ID: e7f2a4b9c01d
Revises: c4a1d7e83f12
Create Date: 2026-06-19

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'e7f2a4b9c01d'
down_revision: Union[str, None] = 'c4a1d7e83f12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('usuario', 'google_id', nullable=True)
    op.add_column('usuario', sa.Column('es_invitado', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    op.drop_column('usuario', 'es_invitado')
    op.alter_column('usuario', 'google_id', nullable=False)
