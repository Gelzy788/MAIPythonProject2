from datetime import datetime

import pytest

from streamstats.errors import InvalidEventError, InvalidTimestampError
from streamstats.models import Event, Level


def test_valid_event_is_created(event_data):
    event = Event.create_event(event_data)

    assert event.timestamp == datetime.fromisoformat("2026-10-01T10:00:00+03:00")
    assert event.level is Level.INFO
    assert event.source == "auth"
    assert event.message == "User logged in"

def test_empty_message_is_allowed(event_data):
    event_data["message"] = ""

    assert Event.create_event(event_data).message == ""

@pytest.mark.parametrize("data", [None, [], 42, "строка"])
def test_non_dict_data_is_rejected(data):
    with pytest.raises(InvalidEventError):
        Event.create_event(data)


@pytest.mark.parametrize("field", ["timestamp", "level", "source", "message"])
def test_missing_field_is_rejected(event_data, field):
    del event_data[field]

    with pytest.raises(InvalidEventError, match=field):
        Event.create_event(event_data)


@pytest.mark.parametrize("field", ["timestamp", "level", "source", "message"])
def test_none_field_is_rejected(event_data, field):
    event_data[field] = None

    with pytest.raises(InvalidEventError, match=field):
        Event.create_event(event_data)


@pytest.mark.parametrize("value", ["", "не дата", 1696150800])
def test_invalid_timestamp_is_rejected(event_data, value):
    event_data["timestamp"] = value

    with pytest.raises(InvalidTimestampError):
        Event.create_event(event_data)


@pytest.mark.parametrize("value", ["", 3])
def test_invalid_level_is_rejected(event_data, value):
    event_data["level"] = value

    with pytest.raises(InvalidEventError):
        Event.create_event(event_data)


@pytest.mark.parametrize("value", ["", "   ", 42])
def test_invalid_source_is_rejected(event_data, value):
    event_data["source"] = value

    with pytest.raises(InvalidEventError):
        Event.create_event(event_data)
        