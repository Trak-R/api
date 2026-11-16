"""Aircraft API routes."""

from fastapi import APIRouter, Depends, status
from querymate import Querymate

from aircraft.models.aircraft import Aircraft
from aircraft.schemas.aircraft import AircraftCreate, AircraftResponse, AircraftUpdate
from aircraft.services.aircraft import AircraftService
from identity.dependencies import authorization
from identity.models.user import User
from trakr_core.exceptions import ERROR_RESPONSES
from trakr_core.schemas.responses import ListResponse

router = APIRouter(prefix="/aircraft", tags=["Aircraft"])


def get_aircraft_service() -> AircraftService:
    return AircraftService()


@router.get(
    "",
    response_model=ListResponse[AircraftResponse],
    responses=ERROR_RESPONSES,
    summary="List aircraft",
)
async def list_aircraft(
    query: Querymate = Depends(Querymate.fastapi_dependency),
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(authorization()),
) -> ListResponse[AircraftResponse]:
    return await service.list(query)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AircraftResponse,
    responses=ERROR_RESPONSES,
    summary="Create an aircraft",
)
async def create_aircraft(
    body: AircraftCreate,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(authorization()),
) -> Aircraft:
    return await service.create(Aircraft(**body.model_dump()))


@router.get(
    "/{id}",
    response_model=AircraftResponse,
    responses=ERROR_RESPONSES,
    summary="Get an aircraft",
)
async def get_aircraft(
    id: int,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(authorization()),
) -> Aircraft:
    return await service.get(id)


@router.patch(
    "/{id}",
    response_model=AircraftResponse,
    responses=ERROR_RESPONSES,
    summary="Update an aircraft",
)
async def update_aircraft(
    id: int,
    body: AircraftUpdate,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(authorization()),
) -> Aircraft:
    return await service.update(id, body.model_dump(exclude_unset=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=ERROR_RESPONSES,
    summary="Delete an aircraft",
)
async def delete_aircraft(
    id: int,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(authorization()),
) -> None:
    await service.delete(id)
