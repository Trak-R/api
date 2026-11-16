"""Role model."""
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

from trakr_core.models.base import BaseModel

if TYPE_CHECKING:
    from identity.models.user import User


class Role(BaseModel, table=True):
    """Role model representing user roles in the system."""

    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    
    # Relationship
    users: list["User"] = Relationship(back_populates="role")
