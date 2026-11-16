"""Aircraft telemetry table."""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, DateTime, Enum, Index, func
from sqlmodel import Field

from aircraft_telemetry.models.enums import TransmissionType
from trakr_core.models.base import BaseModel


class AircraftTelemetry(BaseModel, table=True):
    """A telemetry record for an aircraft."""

    __tablename__ = "aircraft_telemetry"
    __table_args__ = (
        Index("ix_aircraft_telemetry_address_observed_at", "address", "observed_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    address: str = Field(index=True, max_length=6)
    transmission_type: TransmissionType = Field(
        sa_column=Column(
            Enum(
                TransmissionType,
                name="transmissiontype",
                values_callable=lambda members: [member.value for member in members],
            ),
            nullable=False,
        )
    )
    observed_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    received_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
    callsign: Optional[str] = Field(default=None, max_length=8)
    altitude: Optional[float] = None
    ground_speed: Optional[float] = None
    track: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    vertical_rate: Optional[float] = None
    squawk: Optional[str] = Field(default=None, max_length=4)
    alert: Optional[bool] = None
    emergency: Optional[bool] = None
    spi: Optional[bool] = None
    is_on_ground: Optional[bool] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
