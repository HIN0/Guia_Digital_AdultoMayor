"""valoracion_mensaje

Revision ID: b3f9a2c1e047
Revises: 536e8f6de3a8
Create Date: 2026-06-13

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'b3f9a2c1e047'
down_revision: Union[str, None] = '536e8f6de3a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('mensaje_chat', sa.Column('valoracion', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('mensaje_chat', 'valoracion')
