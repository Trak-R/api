"""add aircraft and aircraft telemetry

Revision ID: f4c8b2a17e90
Revises: ca918f25512c
Create Date: 2026-11-15 20:55:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "f4c8b2a17e90"
down_revision: Union[str, None] = "ca918f25512c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

transmission_type = postgresql.ENUM(
    "Identification",
    "SurfacePosition",
    "AirbornePosition",
    "AirborneVelocity",
    "SurveillanceAlt",
    "SurveillanceId",
    "AirToAir",
    "AllCallReply",
    "Unknown",
    name="transmissiontype",
    create_type=False,
)


def upgrade() -> None:
    transmission_type.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "aircraft",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=6), nullable=False),
        sa.Column("callsign", sa.String(length=8), nullable=True),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_aircraft_address"), "aircraft", ["address"], unique=True)
    op.create_table(
        "aircraft_telemetry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=6), nullable=False),
        sa.Column("transmission_type", transmission_type, nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("callsign", sa.String(length=8), nullable=True),
        sa.Column("altitude", sa.Float(), nullable=True),
        sa.Column("ground_speed", sa.Float(), nullable=True),
        sa.Column("track", sa.Float(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("vertical_rate", sa.Float(), nullable=True),
        sa.Column("squawk", sa.String(length=4), nullable=True),
        sa.Column("alert", sa.Boolean(), nullable=True),
        sa.Column("emergency", sa.Boolean(), nullable=True),
        sa.Column("spi", sa.Boolean(), nullable=True),
        sa.Column("is_on_ground", sa.Boolean(), nullable=True),
        sa.Column("source_topic", sa.String(length=255), nullable=True),
        sa.Column("source_partition", sa.Integer(), nullable=True),
        sa.Column("source_offset", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "source_topic",
            "source_partition",
            "source_offset",
            name="uq_aircraft_telemetry_source",
        ),
    )
    op.create_index(
        op.f("ix_aircraft_telemetry_address"),
        "aircraft_telemetry",
        ["address"],
        unique=False,
    )
    op.create_index(
        "ix_aircraft_telemetry_address_observed_at",
        "aircraft_telemetry",
        ["address", "observed_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_aircraft_telemetry_address_observed_at",
        table_name="aircraft_telemetry",
    )
    op.drop_index(
        op.f("ix_aircraft_telemetry_address"), table_name="aircraft_telemetry"
    )
    op.drop_table("aircraft_telemetry")
    transmission_type.drop(op.get_bind(), checkfirst=True)
    op.drop_index(op.f("ix_aircraft_address"), table_name="aircraft")
    op.drop_table("aircraft")
