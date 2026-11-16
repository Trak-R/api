"""Aircraft request and response schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class AircraftCreate(BaseModel):
    address: str = Field(pattern=r"^[0-9A-F]{6}$")
    callsign: Optional[str] = Field(default=None, max_length=8)
    last_seen_at: Optional[datetime] = None

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

    @field_validator("callsign", mode="before")
    @classmethod
    def blank_callsign_to_none(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        stripped = value.strip()
        return stripped or None


class AircraftUpdate(BaseModel):
    address: Optional[str] = Field(default=None, pattern=r"^[0-9A-F]{6}$")
    callsign: Optional[str] = Field(default=None, max_length=8)
    last_seen_at: Optional[datetime] = None

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

    @field_validator("callsign", mode="before")
    @classmethod
    def blank_callsign_to_none(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        stripped = value.strip()
        return stripped or None


class AircraftResponse(BaseModel):
    id: Optional[int] = None
    address: Optional[str] = None
    callsign: Optional[str] = None
    last_seen_at: Optional[datetime] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
