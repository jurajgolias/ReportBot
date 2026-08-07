import importlib
import runpy

import pytest
import requests

import reportbot.main as reportbot_main
from reportbot.fetch_data import fetch_weather_data
from reportbot.process_data import process_weather_data
from reportbot.generate_report import generate_report


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

def test_generate_report() -> None:
    weather_data = {
        "date": "2026-08-06",
        "maximum_temperature": 31.5,
        "minimum_temperature": 22.0,
        "rain_probability": 10,
    }

    report = generate_report(weather_data)

    assert "Daily Weather Report" in report
    assert "2026-08-06" in report
    assert "31.5 °C" in report
    assert "10%" in report


def test_module_entrypoint_runs_main(monkeypatch) -> None:
    monkeypatch.setattr(reportbot_main, "fetch_weather_data", lambda: SAMPLE_DATA)
    monkeypatch.setattr(
        reportbot_main,
        "process_weather_data",
        lambda raw_data: {
            "date": "2026-08-06",
            "maximum_temperature": 31.5,
            "minimum_temperature": 22.0,
            "rain_probability": 10,
        },
    )
    monkeypatch.setattr(reportbot_main, "generate_report", lambda weather_data: "report")
    monkeypatch.setattr(reportbot_main, "send_report", lambda report: None)

    runpy.run_module("reportbot", run_name="__main__")


def test_main_skips_email_when_recipient_missing(monkeypatch, capsys) -> None:
    importlib.reload(reportbot_main)

    monkeypatch.setattr(reportbot_main, "fetch_weather_data", lambda: SAMPLE_DATA)
    monkeypatch.setattr(
        reportbot_main,
        "process_weather_data",
        lambda raw_data: {
            "date": "2026-08-06",
            "maximum_temperature": 31.5,
            "minimum_temperature": 22.0,
            "rain_probability": 10,
        },
    )
    monkeypatch.setattr(reportbot_main, "generate_report", lambda weather_data: "report")

    def fake_send_report(report: str) -> None:
        raise ValueError("EMAIL_RECIPIENT is not configured.")

    monkeypatch.setattr(reportbot_main, "send_report", fake_send_report)

    reportbot_main.main()

    captured = capsys.readouterr()
    assert "Email sending skipped: EMAIL_RECIPIENT is not configured." in captured.out

        