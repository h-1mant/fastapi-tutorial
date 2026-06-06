"""add cascade delete to posts user_id fk

Revision ID: a7f3c8e91b2d
Revises: e941b4279637
Create Date: 2026-06-06 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7f3c8e91b2d'
down_revision: Union[str, Sequence[str], None] = 'e941b4279637'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add ON DELETE CASCADE to posts.user_id foreign key."""
    op.drop_constraint('fk_posts_user_id', 'posts', type_='foreignkey')
    op.create_foreign_key(
        'fk_posts_user_id', 'posts', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Remove ON DELETE CASCADE from posts.user_id foreign key."""
    op.drop_constraint('fk_posts_user_id', 'posts', type_='foreignkey')
    op.create_foreign_key(
        'fk_posts_user_id', 'posts', 'users',
        ['user_id'], ['id']
    )
