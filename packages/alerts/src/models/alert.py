from typing import Optional

from sqlmodel import Field

from trakr_core.models import BaseModel
from alerts.models.enums import AlertType


class Alert(BaseModel, table=True):
    __tablename__ = "alerts"

    id: Optional[int] = Field(default=None, primary_key=True)
    message: Optional[str] = None
    alert_type: AlertType = Field(default=AlertType.GENERAL)
    user_id: int = Field(foreign_key="users.id", index=True)
