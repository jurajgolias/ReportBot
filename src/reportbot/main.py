from .fetch_data import fetch_weather_data
from .process_data import process_weather_data


def main() -> None:
    raw_data = fetch_weather_data()
    weather = process_weather_data(raw_data)

    print(weather)


if __name__ == "__main__":
    main()
