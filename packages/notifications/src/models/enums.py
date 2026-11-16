"""Notification enums."""
from enum import Enum


class NotificationType(str, Enum):
    GENERAL = "general"
    DOCUMENT_UPLOAD = "upload-complete"
    REPORT_GENERATION = "report-generation"
