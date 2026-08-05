def process_weather_data(raw_data: dict) -> dict:
    """Extract values needed for the daily weather report."""

    if not raw_data:
        raise ValueError("Weather data cannot be empty.")

    if "daily" not in raw_data:
        raise ValueError("Weather data is missing the 'daily' section.")

    daily_data = raw_data["daily"]

    required_fields = [
        "time",
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_probability_max",
    ]

    for field in required_fields:
        if field not in daily_data:
            raise ValueError(f"Weather data is missing '{field}'.")

        if not isinstance(daily_data[field], list):
            raise ValueError(f"Weather field '{field}' must be a list.")

        if not daily_data[field]:
            raise ValueError(f"Weather field '{field}' cannot be empty.")

    return {
        "date": daily_data["time"][0],
        "maximum_temperature": daily_data["temperature_2m_max"][0],
        "minimum_temperature": daily_data["temperature_2m_min"][0],
        "rain_probability": daily_data[
            "precipitation_probability_max"
        ][0],
    }