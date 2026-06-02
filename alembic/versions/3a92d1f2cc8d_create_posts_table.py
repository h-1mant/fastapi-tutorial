"""create posts table

Revision ID: 3a92d1f2cc8d
Revises: 
Create Date: 2026-06-01 21:36:44.251544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a92d1f2cc8d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts", 
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(50), nullable=False),
        sa.Column("content", sa.String(200), nullable=False),
        sa.Column("published", sa.Boolean(), server_default="FALSE", nullable=False),
        sa.Column("created_ts", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_ts", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
