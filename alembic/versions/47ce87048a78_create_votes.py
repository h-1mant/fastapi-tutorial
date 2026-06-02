"""create votes

Revision ID: 47ce87048a78
Revises: d1fe41a475ca
Create Date: 2026-06-01 22:07:31.393165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47ce87048a78'
down_revision: Union[str, Sequence[str], None] = 'd1fe41a475ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("votes")
