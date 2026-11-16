"""Aircraft service."""

from sqlalchemy.exc import IntegrityError

from aircraft.models.aircraft import Aircraft
from aircraft.repository.aircraft import AircraftRepository
from trakr_core.exceptions import AlreadyExistsError
from trakr_core.services.base import BaseService


class AircraftService(BaseService[Aircraft]):
    def __init__(self):
        super().__init__(Aircraft)
        self.repository = AircraftRepository()

    async def create(self, obj_in: Aircraft | dict) -> Aircraft:
        try:
            return await super().create(obj_in)
        except IntegrityError as exc:
            address = (
                obj_in.address
                if isinstance(obj_in, Aircraft)
                else obj_in.get("address")
            )
            raise AlreadyExistsError("Aircraft", "address", str(address)) from exc
