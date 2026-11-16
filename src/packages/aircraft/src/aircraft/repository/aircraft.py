"""Aircraft repository."""

from aircraft.models.aircraft import Aircraft
from trakr_core.repository.base import BaseRepository


class AircraftRepository(BaseRepository[Aircraft]):
    def __init__(self):
        super().__init__(Aircraft)
