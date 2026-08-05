import requests


API_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_weather_data() -> dict:
    """Fetch today's weather forecast for Málaga."""

    parameters = {
        "latitude": 36.72,
        "longitude": -4.42,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
        ],
        "timezone": "Europe/Madrid",
        "forecast_days": 1,
    }

    try:
        response = requests.get(
            API_URL,
            params=parameters,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        raise RuntimeError("Failed to fetch weather data.") from error
    except ValueError as error:
        raise ValueError("The API returned malformed JSON data.") from error

    if not data:
        raise ValueError("The API returned empty data.")

    return data