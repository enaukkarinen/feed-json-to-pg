"""create gist index

Revision ID: fbbb0842fbe9
Revises: 405630981312
Create Date: 2025-01-30 11:43:26.231354

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fbbb0842fbe9"
down_revision: Union[str, None] = "405630981312"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "idx_title_boundary_geometry",
        "title_boundary",
        ["geometry"],
        unique=False,
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index("idx_title_boundary_geometry", table_name="title_boundary")
