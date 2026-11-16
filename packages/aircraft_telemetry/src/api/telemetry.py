"""Aircraft telemetry API routes."""

from fastapi import APIRouter, Depends, status
from querymate import Querymate

from aircraft_telemetry.models.aircraft_telemetry import AircraftTelemetry
from aircraft_telemetry.schemas.aircraft_telemetry import (
    AircraftTelemetryCreate,
    AircraftTelemetryResponse,
    AircraftTelemetryUpdate,
)
from aircraft_telemetry.services.telemetry import AircraftTelemetryService
from identity.dependencies import authorization
from identity.models.user import User
from trakr_core.exceptions import ERROR_RESPONSES
from trakr_core.schemas.responses import ListResponse

router = APIRouter(prefix="/aircraft-telemetry", tags=["Aircraft telemetry"])


def get_telemetry_service() -> AircraftTelemetryService:
    return AircraftTelemetryService()


@router.get(
    "",
    response_model=ListResponse[AircraftTelemetryResponse],
    responses=ERROR_RESPONSES,
    summary="List aircraft telemetry",
)
async def list_telemetry(
    query: Querymate = Depends(Querymate.fastapi_dependency),
    service: AircraftTelemetryService = Depends(get_telemetry_service),
    current_user: User = Depends(authorization()),
) -> ListResponse[AircraftTelemetryResponse]:
    return await service.list(query)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AircraftTelemetryResponse,
    responses=ERROR_RESPONSES,
    summary="Create an aircraft telemetry record",
)
async def create_telemetry(
    body: AircraftTelemetryCreate,
    service: AircraftTelemetryService = Depends(get_telemetry_service),
    current_user: User = Depends(authorization()),
) -> AircraftTelemetry:
    return await service.create(body.model_dump())


@router.get(
    "/{id}",
    response_model=AircraftTelemetryResponse,
    responses=ERROR_RESPONSES,
    summary="Get an aircraft telemetry record",
)
async def get_telemetry(
    id: int,
    service: AircraftTelemetryService = Depends(get_telemetry_service),
    current_user: User = Depends(authorization()),
) -> AircraftTelemetry:
    return await service.get(id)


@router.patch(
    "/{id}",
    response_model=AircraftTelemetryResponse,
    responses=ERROR_RESPONSES,
    summary="Update an aircraft telemetry record",
)
async def update_telemetry(
    id: int,
    body: AircraftTelemetryUpdate,
    service: AircraftTelemetryService = Depends(get_telemetry_service),
    current_user: User = Depends(authorization()),
) -> AircraftTelemetry:
    return await service.update(id, body.model_dump(exclude_unset=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=ERROR_RESPONSES,
    summary="Delete an aircraft telemetry record",
)
async def delete_telemetry(
    id: int,
    service: AircraftTelemetryService = Depends(get_telemetry_service),
    current_user: User = Depends(authorization()),
) -> None:
    await service.delete(id)
