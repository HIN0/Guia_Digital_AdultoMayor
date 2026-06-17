"""agregar_fk_reales_en_progreso

Revision ID: c4a1d7e83f12
Revises: b3f9a2c1e047
Create Date: 2026-06-17

"""
from typing import Sequence, Union
from alembic import op

revision: str = 'c4a1d7e83f12'
down_revision: Union[str, None] = 'b3f9a2c1e047'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_progreso_leccion_usuario",
        "progreso_leccion", "usuario",
        ["usuario_id"], ["id"],
    )
    op.create_foreign_key(
        "fk_progreso_leccion_leccion",
        "progreso_leccion", "leccion",
        ["leccion_id"], ["id"],
    )
    op.create_foreign_key(
        "fk_intento_quiz_usuario",
        "intento_quiz", "usuario",
        ["usuario_id"], ["id"],
    )
    op.create_foreign_key(
        "fk_intento_quiz_quiz_final",
        "intento_quiz", "quiz_final",
        ["quiz_id"], ["id"],
    )
    op.create_foreign_key(
        "fk_insignia_obtenida_usuario",
        "insignia_obtenida", "usuario",
        ["usuario_id"], ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_insignia_obtenida_usuario", "insignia_obtenida", type_="foreignkey")
    op.drop_constraint("fk_intento_quiz_quiz_final", "intento_quiz", type_="foreignkey")
    op.drop_constraint("fk_intento_quiz_usuario", "intento_quiz", type_="foreignkey")
    op.drop_constraint("fk_progreso_leccion_leccion", "progreso_leccion", type_="foreignkey")
    op.drop_constraint("fk_progreso_leccion_usuario", "progreso_leccion", type_="foreignkey")
