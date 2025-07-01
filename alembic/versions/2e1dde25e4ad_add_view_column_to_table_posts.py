"""add view column to table posts

Revision ID: 2e1dde25e4ad
Revises: 37984b568bb5
Create Date: 2025-06-30 20:55:48.670363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '2e1dde25e4ad'
down_revision: Union[str, Sequence[str], None] = '37984b568bb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column('views', sa.Integer, server_default=text("0"), nullable=False))



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("posts","views")

    pass
