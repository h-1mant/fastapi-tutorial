"""create users

Revision ID: d1fe41a475ca
Revises: 3a92d1f2cc8d
Create Date: 2026-06-01 22:04:36.967250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1fe41a475ca'
down_revision: Union[str, Sequence[str], None] = '3a92d1f2cc8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(50), nullable=False, unique=True),
        sa.Column("password", sa.String(128), nullable=False),
        sa.Column("created_ts", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_ts", sa.DateTime(timezone=True), nullable=True),
    )

    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "fk_posts_user_id",
        source_table="posts", referent_table="users",
        local_cols=["user_id"], remote_cols=["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_posts_user_id", table_name="posts", type_="foreignkey")
    op.drop_column("posts", "user_id")
    op.drop_table("users")
