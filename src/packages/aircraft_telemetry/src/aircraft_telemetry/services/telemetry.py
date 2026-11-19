"""Aircraft telemetry service."""

from datetime import datetime, timezone

from aircraft_telemetry.models.aircraft_telemetry import AircraftTelemetry
from aircraft_telemetry.repository.aircraft_telemetry import AircraftTelemetryRepository
from trakr_core.services.base import BaseService


class AircraftTelemetryService(BaseService[AircraftTelemetry]):
    def __init__(self):
        super().__init__(AircraftTelemetry)
        self.repository = AircraftTelemetryRepository()
