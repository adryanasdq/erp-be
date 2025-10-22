"""change menu id to str cuid

Revision ID: c4799188e6d4
Revises: 31f62db5636a
Create Date: 2025-10-20 21:06:47.310069

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "c4799188e6d4"
down_revision: Union[str, Sequence[str], None] = "31f62db5636a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        "menu_parent_id_fkey", "menu", schema="admin", type_="foreignkey"
    )

    op.alter_column(
        "menu",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=False,
        schema="admin",
    )

    op.alter_column(
        "menu",
        "parent_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=True,
        schema="admin",
    )

    op.create_foreign_key(
        "menu_parent_id_fkey",
        "menu",
        "menu",
        local_cols=["parent_id"],
        remote_cols=["id"],
        source_schema="admin",
        referent_schema="admin",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "menu_parent_id_fkey", "menu", schema="admin", type_="foreignkey"
    )

    op.alter_column(
        "menu",
        "parent_id",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=True,
        schema="admin",
    )

    op.alter_column(
        "menu",
        "id",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        schema="admin",
    )

    op.create_foreign_key(
        "menu_parent_id_fkey",
        "menu",
        "menu",
        local_cols=["parent_id"],
        remote_cols=["id"],
        source_schema="admin",
        referent_schema="admin",
    )

    # ### end Alembic commands ###
