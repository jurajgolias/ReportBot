import pytest
import requests

from fetch_data import fetch_weather_data
from process_data import process_weather_data


SAMPLE_DATA = {
    "daily": {
        "time": ["2026-08-05"],
        "temperature_2m_max": [31.5],
        "temperature_2m_min": [22.0],
        "precipitation_probability_max": [10],
    }
}


def test_process_weather_data() -> None:
    result = process_weather_data(SAMPLE_DATA)

    assert result == {
        "date": "2026-08-05",
        "maximum_temperature": 31.5,
        "minimum_temperature": 22.0,
        "rain_probability": 10,
    }


def test_process_weather_data_rejects_empty_data() -> None:
    with pytest.raises(
        ValueError,
        match="Weather data cannot be empty",
    ):
        process_weather_data({})


def test_process_weather_data_rejects_missing_daily_section() -> None:
    malformed_data = {"temperature": 25}

    with pytest.raises(
        ValueError,
        match="missing the 'daily' section",
    ):
        process_weather_data(malformed_data)


def test_process_weather_data_rejects_missing_field() -> None:
    malformed_data = {
        "daily": {
            "time": ["2026-08-05"],
            "temperature_2m_max": [31.5],
            "temperature_2m_min": [22.0],
        }
    }

    with pytest.raises(
        ValueError,
        match="precipitation_probability_max",
    ):
        process_weather_data(malformed_data)


def test_fetch_weather_data_success(monkeypatch) -> None:
    class FakeResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> dict:
            return SAMPLE_DATA

    def fake_get(*args, **kwargs) -> FakeResponse:
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    result = fetch_weather_data()

    assert result == SAMPLE_DATA


def test_fetch_weather_data_handles_network_failure(
    monkeypatch,
) -> None:
    def fake_get(*args, **kwargs) -> None:
        raise requests.ConnectionError("No connection")

    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(
        RuntimeError,
        match="Failed to fetch weather data",
    ):
        fetch_weather_data()