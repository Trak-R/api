"""Aircraft telemetry repository."""

from aircraft_telemetry.models.aircraft_telemetry import AircraftTelemetry
from trakr_core.repository.base import BaseRepository


class AircraftTelemetryRepository(BaseRepository[AircraftTelemetry]):
    def __init__(self):
        super().__init__(AircraftTelemetry)
