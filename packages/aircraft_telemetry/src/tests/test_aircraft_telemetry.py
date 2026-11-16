"""Schema tests for aircraft telemetry records."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from aircraft_telemetry.models.enums import TransmissionType
from aircraft_telemetry.schemas.aircraft_telemetry import AircraftTelemetryCreate


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
