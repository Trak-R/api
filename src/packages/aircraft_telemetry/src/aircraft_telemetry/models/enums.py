"""Transmission types from the BaseStation feed."""

from enum import Enum


class TransmissionType(str, Enum):
    Identification = "Identification"
    SurfacePosition = "SurfacePosition"
    AirbornePosition = "AirbornePosition"
    AirborneVelocity = "AirborneVelocity"
    SurveillanceAlt = "SurveillanceAlt"
    SurveillanceId = "SurveillanceId"
    AirToAir = "AirToAir"
    AllCallReply = "AllCallReply"
    Unknown = "Unknown"
