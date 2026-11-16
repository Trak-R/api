"""Aircraft telemetry service."""

from datetime import datetime, timezone

from aircraft_telemetry.models.aircraft_telemetry import AircraftTelemetry
from aircraft_telemetry.repository.aircraft_telemetry import AircraftTelemetryRepository
from trakr_core.services.base import BaseService


class AircraftTelemetryService(BaseService[AircraftTelemetry]):
    def __init__(self):
        super().__init__(AircraftTelemetry)
        self.repository = AircraftTelemetryRepository()

    async def create(self, obj_in: AircraftTelemetry | dict) -> AircraftTelemetry:
        if isinstance(obj_in, dict):
            obj_in = {
                **obj_in,
                "received_at": obj_in.get("received_at") or datetime.now(timezone.utc),
            }
        elif obj_in.received_at is None:
            obj_in.received_at = datetime.now(timezone.utc)
        return await super().create(obj_in)
