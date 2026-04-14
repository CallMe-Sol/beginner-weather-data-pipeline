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

```bash
# Linux / macOS
export OPENWEATHER_API_KEY="your_key_here"

# Windows PowerShell
$env:OPENWEATHER_API_KEY="your_key_here"
```

### 3 - Run the pipeline

```
# Deafult 8-city batch
python pipeline.py

# Custom city list
python pipeline.py --cities "Paris, Tokyo, Cairo, Lagos"

# Custom database path
python pipeline.py --db /data/weather.db
```

## Running Tests

```bash
python -m unittest tests.test_pipeline -v
```

Expected:
```
Ran 27 tests in 0.49s
OK
```

Tests cover:
- Transform Layer: Field Extraction, Unit Conversions, Compass Directions, Edge Cases
- Database Layer: Upsert Logic, History Append, Aggregate Queries, Schema Validation
- Fetch Layer: Mocked HTTP 200 Success and 404 City-Not-Found

## License

MIT License - Free to use, modify, and distribute.S
