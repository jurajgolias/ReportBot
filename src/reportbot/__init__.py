"""ReportBot package."""

from .fetch_data import fetch_weather_data
from .process_data import process_weather_data

__all__ = ["main", "fetch_weather_data", "process_weather_data"]


def __getattr__(name: str):
    if name == "main":
        from .main import main as main_function

        return main_function

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
