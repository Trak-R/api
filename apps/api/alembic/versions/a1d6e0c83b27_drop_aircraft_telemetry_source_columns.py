"""drop aircraft telemetry source columns

Revision ID: a1d6e0c83b27
Revises: f4c8b2a17e90
Create Date: 2026-11-15 21:28:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1d6e0c83b27"
down_revision: Union[str, None] = "f4c8b2a17e90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "uq_aircraft_telemetry_source",
        "aircraft_telemetry",
        type_="unique",
    )
    op.drop_column("aircraft_telemetry", "source_offset")
    op.drop_column("aircraft_telemetry", "source_partition")
    op.drop_column("aircraft_telemetry", "source_topic")


def downgrade() -> None:
    op.add_column(
        "aircraft_telemetry",
        sa.Column("source_topic", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "aircraft_telemetry",
        sa.Column("source_partition", sa.Integer(), nullable=True),
    )
    op.add_column(
        "aircraft_telemetry",
        sa.Column("source_offset", sa.BigInteger(), nullable=True),
    )
    op.create_unique_constraint(
        "uq_aircraft_telemetry_source",
        "aircraft_telemetry",
        ["source_topic", "source_partition", "source_offset"],
    )
