# ReportBot

A Python automation bot that fetches the daily Málaga weather forecast, turns it into a short report, and can send the report automatically by email.

## Problem it solves

ReportBot removes the need to manually check and summarize the weather every day. It is designed for anyone who wants a simple daily weather summary delivered automatically, and it also demonstrates how a small Python script can be turned into a complete automated system using APIs, tests, email delivery, and GitHub Actions.

## Features

- Fetches daily weather data from the Open-Meteo public API
- Uses the forecast for Málaga, Spain
- Extracts the date, maximum temperature, minimum temperature, and rain probability
- Validates empty or malformed API data
- Handles network and API failures
- Generates a readable daily weather report
- Sends the report through Gmail SMTP
- Runs automated tests with pytest
- Runs automatically with GitHub Actions
- Can also be started manually from the GitHub Actions page

## Requirements

- Git
- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- Internet connection for live weather data
- Gmail account with an App Password if you want email delivery

## Installation

Clone the repository:

```bash
git clone https://github.com/jurajgolias/ReportBot.git
cd ReportBot
```

Install the project and development dependencies:

```bash
uv sync --locked --dev
```

Run the automated tests:

```bash
uv run pytest
```

## Usage

### Run without email configuration

Run the bot from the repository root:

```bash
uv run python -m reportbot
```

The program fetches the current Málaga forecast and prints the generated report. If email environment variables are not configured, email delivery is skipped.

### Run with email delivery

ReportBot expects these environment variables:

- `EMAIL_ADDRESS` — Gmail address used to send the report
- `EMAIL_PASSWORD` — Gmail App Password
- `EMAIL_RECIPIENT` — email address that receives the report

PowerShell example:

```powershell
$env:EMAIL_ADDRESS = "sender@gmail.com"
$env:EMAIL_PASSWORD = "your-app-password"
$env:EMAIL_RECIPIENT = "recipient@example.com"
uv run python -m reportbot
```

Linux/macOS example:

```bash
export EMAIL_ADDRESS="sender@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export EMAIL_RECIPIENT="recipient@example.com"
uv run python -m reportbot
```

Never commit real passwords or App Passwords to the repository.

## Example input

The application does not require manual user input. It automatically requests forecast data from Open-Meteo for Málaga using approximately these coordinates:

```text
Latitude: 36.72
Longitude: -4.42
Forecast days: 1
Timezone: Europe/Madrid
```

The API response contains daily forecast fields such as:

```json
{
  "daily": {
    "time": ["2026-08-06"],
    "temperature_2m_max": [31.2],
    "temperature_2m_min": [24.5],
    "precipitation_probability_max": [0]
  }
}
```

## Example output

```text
# Daily Weather Report

Date: 2026-08-06
Maximum temperature: 31.2 °C
Minimum temperature: 24.5 °C
Rain probability: 0%
```

When email delivery succeeds, the console also prints:

```text
Daily report sent successfully.
```

## How it works

```text
GitHub Actions / manual run
          |
          v
   fetch_weather_data()
          |
          v
    Open-Meteo API
          |
          v
  process_weather_data()
          |
          v
    generate_report()
          |
          +-------------------+
          |                   |
          v                   v
     print report        send_report()
                              |
                              v
                         Gmail SMTP
                              |
                              v
                         Recipient
```

The project is split into small modules so that each function has one main responsibility:

- `fetch_data.py` requests weather data from Open-Meteo and handles network or malformed-response errors.
- `process_data.py` validates the response and extracts only the fields needed for the report.
- `generate_report.py` converts the processed dictionary into readable text.
- `send_report.py` sends the report using Gmail SMTP and environment variables.
- `main.py` connects the complete pipeline together.

## Project structure

```text
ReportBot/
├── .github/
│   └── workflows/
│       ├── daily-report.yml
│       └── tests.yml
├── src/
│   └── reportbot/
│       ├── __init__.py
│       ├── __main__.py
│       ├── fetch_data.py
│       ├── generate_report.py
│       ├── main.py
│       ├── process_data.py
│       └── send_report.py
├── tests/
│   └── test_core.py
├── README.md
├── pyproject.toml
└── uv.lock
```

## Automated scheduling

The `daily-report.yml` GitHub Actions workflow runs the complete pipeline automatically using Python 3.13. It currently uses this schedule:

```yaml
- cron: "0 9,14 * * *"
```

This means the scheduled workflow starts every day at 09:00 UTC and 14:00 UTC. GitHub Actions schedules use UTC.

The workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs uv and dependencies.
4. Runs the pytest test suite.
5. Fetches the weather forecast.
6. Processes and generates the report.
7. Sends it by email when email secrets are configured.

The workflow can also be run manually using `workflow_dispatch` from the repository's **Actions** tab.

### GitHub Secrets

For automatic email delivery, add these repository secrets under:

`Settings → Secrets and variables → Actions`

```text
EMAIL_ADDRESS
EMAIL_PASSWORD
EMAIL_RECIPIENT
```

`EMAIL_PASSWORD` should contain a Gmail App Password, not the normal Google account password.

## Testing

The project uses pytest. Run all tests with:

```bash
uv run pytest
```

The tests cover core behaviour including:

- processing valid weather data
- rejecting empty data
- rejecting malformed or incomplete data
- successful API fetching using a mocked request
- handling network failures
- report generation
- the module entry point
- behaviour when the email recipient is not configured

GitHub Actions also runs the test suite automatically so changes can be checked in a clean Linux environment.

## Tech stack

- **Python 3.12+** — application language
- **uv** — dependency and environment management
- **Requests** — HTTP requests to the weather API
- **Open-Meteo API** — live public weather data
- **pytest** — automated testing
- **smtplib / EmailMessage** — email delivery through Gmail SMTP
- **GitHub Actions** — CI and scheduled automation

## Data

The production application uses live public weather forecast data from Open-Meteo. No private user data is required for weather processing.

The automated tests use synthetic sample weather data instead of depending on live API values. Example test values include a maximum temperature of `31.5 °C`, minimum temperature of `22.0 °C`, and rain probability of `10%`. This makes the tests repeatable and independent of changing weather conditions.

## Clean-clone check

A new user should be able to verify the project with only these commands:

```bash
git clone https://github.com/jurajgolias/ReportBot.git
cd ReportBot
uv sync --locked --dev
uv run pytest
uv run python -m reportbot
```

The first four commands install and test the project. The final command fetches live weather data and prints a report. Email delivery requires the optional environment variables described above.
