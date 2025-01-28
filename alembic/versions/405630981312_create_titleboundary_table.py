"""create titleboundary table

Revision ID: 405630981312
Revises: 
Create Date: 2025-01-24 11:45:00.214257

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import geoalchemy2


# revision identifiers, used by Alembic.
revision: str = "405630981312"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "title_boundary",
        sa.Column("id", sa.String(255), primary_key=True),  # Primary key column
        sa.Column("dataset", sa.String(255), nullable=False),
        sa.Column("end_date", sa.String(255), nullable=True),
        sa.Column("entity", sa.String(255), nullable=False),
        sa.Column("entry_date", sa.String(255), nullable=False),
         sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(
                srid=4326,
                spatial_index=False,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=True,
        ),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("organisation_entity", sa.String(255), nullable=True),
        sa.Column("point", sa.String, nullable=True),
        sa.Column("prefix", sa.String(255), nullable=True),
        sa.Column("reference", sa.String(255), nullable=True),
        sa.Column("start_date", sa.String(255), nullable=True),
        sa.Column("typology", sa.String(255), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("title_boundary")  # nosec - B608: SQLAlchemy injection is not a concern in this context
    pass
