from faststream import Depends

from aircraft_telemetry.schemas import AircraftTelemetryCreate
from aircraft_telemetry.services import AircraftTelemetryService
from trakr_persistence_worker.broker import CONSUMER_GROUP_ID, broker

def get_telemetry_service() -> AircraftTelemetryService:
    return AircraftTelemetryService()

@broker.subscriber("adsb.basestation", group_id=CONSUMER_GROUP_ID)
async def ingest_telemetry(
        message: AircraftTelemetryCreate,
        service: AircraftTelemetryService = Depends(get_telemetry_service)
) -> None:
    await service.create(message)