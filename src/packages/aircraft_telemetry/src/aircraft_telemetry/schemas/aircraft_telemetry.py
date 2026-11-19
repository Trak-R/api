"""Aircraft telemetry request and response schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

from aircraft_telemetry.models.enums import TransmissionType


class AircraftTelemetryBase(BaseModel):
    """Fields shared by create, update, and response payloads."""

    address: str = Field(pattern=r"^[0-9A-F]{6}$")
    transmission_type: TransmissionType
    observed_at: Optional[datetime] = None
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
    )

    @field_validator("address", mode="before")
    @classmethod
    def normalize_address(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().upper()
        return value

    @field_validator("callsign", "squawk", mode="before")
    @classmethod
    def blank_to_none(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        stripped = value.strip()
        return stripped or None


class AircraftTelemetryCreate(AircraftTelemetryBase):
    """Telemetry required to record a transmission."""


class AircraftTelemetryUpdate(AircraftTelemetryBase):
    """Partial telemetry update. Omitted fields are left unchanged."""

    address: Optional[str] = Field(default=None, pattern=r"^[0-9A-F]{6}$")
    transmission_type: Optional[TransmissionType] = None


class AircraftTelemetryResponse(AircraftTelemetryBase):
    """Stored telemetry record."""

    id: Optional[int] = None
    received_at: Optional[datetime] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
