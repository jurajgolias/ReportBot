def process_weather_data(raw_data: dict) -> dict:

    daily_data = raw_data["daily"]

    return {
        "date": daily_data["time"][0],
        "maximum_temperature": daily_data["temperature_2m_max"][0],
        "minimum_temperature": daily_data["temperature_2m_min"][0],
        "rain_probability": daily_data[
            "precipitation_probability_max"
        ][0],
    }