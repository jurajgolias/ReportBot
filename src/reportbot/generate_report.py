def generate_report(weather_data: dict) -> str:
    """Create a readable weather report."""

    return (
        "# Daily Weather Report\n\n"
        f"Date: {weather_data['date']}\n"
        f"Maximum temperature: "
        f"{weather_data['maximum_temperature']} °C\n"
        f"Minimum temperature: "
        f"{weather_data['minimum_temperature']} °C\n"
        f"Rain probability: "
        f"{weather_data['rain_probability']}%\n"
    )