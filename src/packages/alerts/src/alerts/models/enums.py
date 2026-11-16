"""Alert enums."""
from enum import Enum


class AlertType(str, Enum):
    GENERAL = "general"
    DOCUMENT_UPLOAD = "upload-complete"
