from .fetch_data import fetch_weather_data
from .generate_report import generate_report
from .process_data import process_weather_data
from .send_report import send_report


def main() -> None:
    try:
        raw_data = fetch_weather_data()
        weather_data = process_weather_data(raw_data)
        report = generate_report(weather_data)

        print(report)

        send_report(report)

        print("Daily report sent successfully.")
    except (RuntimeError, ValueError) as error:
        print(f"Report bot failed: {error}")
        raise


if __name__ == "__main__":
    main()