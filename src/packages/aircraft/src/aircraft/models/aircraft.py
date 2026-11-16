"""Aircraft identity model."""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, DateTime
from sqlmodel import Field

from trakr_core.models.base import BaseModel


class Aircraft(BaseModel, table=True):
    """One row per ICAO24 address."""

    __tablename__ = "aircraft"

    id: Optional[int] = Field(default=None, primary_key=True)
    address: str = Field(unique=True, index=True, max_length=6)
    callsign: Optional[str] = Field(default=None, max_length=8)
    last_seen_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
