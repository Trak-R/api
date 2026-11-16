"""Identity enums."""

from enum import Enum


class RoleType(str, Enum):
    USER = "User"
    ADMIN = "Administrator"
