"""create a table for supabase

Revision ID: 9c06830161f0
Revises: 2f05f3095947
Create Date: 2024-11-02 22:19:47.348923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c06830161f0'
down_revision: Union[str, None] = '2f05f3095947'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
