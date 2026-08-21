"""eliminar_es_invitado

Revision ID: a4c8e2f6b193
Revises: e7f2a4b9c01d
Create Date: 2026-08-13

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = 'a4c8e2f6b193'
down_revision: Union[str, None] = 'e7f2a4b9c01d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # El login de invitado se eliminó del producto; el campo quedó sin uso.
    op.drop_column('usuario', 'es_invitado')


def downgrade() -> None:
    op.add_column('usuario', sa.Column('es_invitado', sa.Boolean(), nullable=False, server_default='false'))
