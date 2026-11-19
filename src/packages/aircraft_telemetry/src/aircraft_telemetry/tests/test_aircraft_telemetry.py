"""Schema tests for aircraft telemetry records."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from aircraft_telemetry.models.enums import TransmissionType
from aircraft_telemetry.schemas.aircraft_telemetry import (
    AircraftTelemetryCreate,
    AircraftTelemetryResponse,
    AircraftTelemetryUpdate,
)


SAMPLE = {
    "address": "102B04",
    "alert": False,
    "altitude": 31839,
    "emergency": False,
    "observedAt": "2026-11-15T23:57:19.363",
    "isOnGround": False,
    "spi": False,
    "squawk": "0885",
    "transmissionType": "Unknown",
}


def test_sample_record_parses_and_omits_missing_fields():
    record = AircraftTelemetryCreate.model_validate(SAMPLE)

    assert record.address == "102B04"
    assert record.transmission_type is TransmissionType.Unknown
    assert record.observed_at == datetime(2026, 11, 15, 23, 57, 19, 363000)
    assert record.altitude == 31839
    assert record.alert is False
    assert record.emergency is False
    assert record.spi is False
    assert record.is_on_ground is False
    assert record.squawk == "0885"
    assert record.callsign is None
    assert record.latitude is None
    assert record.longitude is None
    assert record.ground_speed is None
    assert record.track is None
    assert record.vertical_rate is None


def test_explicit_zero_and_false_are_kept():
    record = AircraftTelemetryCreate.model_validate(
        {
            "address": "abc123",
            "transmissionType": "AirbornePosition",
            "altitude": 0,
            "isOnGround": False,
        }
    )

    assert record.address == "ABC123"
    assert record.altitude == 0
    assert record.is_on_ground is False
    assert record.alert is None
    assert record.callsign is None


@pytest.mark.parametrize(
    "payload",
    [
        {**SAMPLE, "address": "12345"},
        {**SAMPLE, "address": "102B0G"},
        {**SAMPLE, "transmissionType": "NotAType"},
    ],
)
def test_invalid_record_is_rejected(payload):
    with pytest.raises(ValidationError):
        AircraftTelemetryCreate.model_validate(payload)


def test_update_can_omit_create_required_fields():
    record = AircraftTelemetryUpdate.model_validate({"altitude": 0, "callsign": " "})

    assert record.address is None
    assert record.transmission_type is None
    assert record.altitude == 0
    assert record.callsign is None
    assert record.model_dump(exclude_unset=True) == {"altitude": 0, "callsign": None}


def test_update_inherits_address_normalization():
    record = AircraftTelemetryUpdate.model_validate({"address": " abc123 "})

    assert record.address == "ABC123"


def test_response_reads_attributes():
    class Row:
        id = 7
        address = "102B04"
        transmission_type = TransmissionType.Unknown
        observed_at = None
        received_at = None
        callsign = None
        altitude = 31839
        ground_speed = None
        track = None
        latitude = None
        longitude = None
        vertical_rate = None
        squawk = None
        alert = None
        emergency = None
        spi = None
        is_on_ground = None

    record = AircraftTelemetryResponse.model_validate(Row())

    assert record.id == 7
    assert record.address == "102B04"
    assert record.altitude == 31839
