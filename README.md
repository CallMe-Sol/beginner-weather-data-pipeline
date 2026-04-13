# 🌤️ Beginner Weather Data

A clean, production-style **Python batch pipeline** that fetches current weather data for a list of cities via the **OpenWeatherMap REST API**, transforms and enriches the records, and persists them to a SQLite database using hand-written SQL.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | ≥ 3.10  |
| pip         | any     |
| OpenWeatherMap API Key | Free Tier |

---

## Setup

### 1 - Clone and install dependencies

```bash
git clone https://github.com/CallMe-Sol beginner-weather-data-pipeline.git
cd beginner-weather-data-pipeline
pip install -r requirements.txt
```

### 2 - Set your API key

Register for a free key at <https://openweathermap.org/api> (Current Weather Data, Free Tier).