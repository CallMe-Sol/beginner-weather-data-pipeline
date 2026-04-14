import argparse
import logging
import sys
import time
from pathlib import Path

from fetch_weather import WeatherFetcher
from transform import WeatherTransformer
from db import WeatherDatabase

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# --------------------------------------------------
# Default Configuration
# --------------------------------------------------
DEFAULT_CITIES = [
    "London", "New York", "Tokyo", "Sydney",
    "Paris", "Dubai", "Toronto", "Berlin",
]
DEFAULT_DB = "weather_data.db"

# --------------------------------------------------
# Pipeline
# --------------------------------------------------
def run_pipeline(cities: list[str], db_path: str) -> dict:
    start = time.perf_counter()

    fetcher     = WeatherFetcher()
    transformer = WeatherTransformer()
    database    = WeatherDatabase(db_path)

    stats = {"fetched": 0, "transformed": 0, "loaded": 0, "failed": 0}

    log.info("=== Weather Pipeline START (cities=%d) ===", len(cities))

    for city in cities:
        try:
            # ── EXTRACT ──────────────────────────────────────────────────
            raw = fetcher.fetch(city)
            if raw is None:
                log.warning("Skipping %s - no data returned", city)
                stats["failed"] += 1
                continue
            stats["fetched"] += 1
            
            # ── TRANSFORM ──────────────────────────────────────────────────
            record = transformer.transform(raw)
            if record is None:
                log.warning("Skipping %s - no data returned", city)
                stats["failed"] += 1
                continue
            stats["fetched"] += 1

            # ── LOAD ──────────────────────────────────────────────────
            database.upsert(record)
            stats["loaded"] += 1
            log.info("✓  %-20s  %.1f°C  %s", city, record["temp_c"], record["description"])
        
        except Exception as exc:
            log.error("Pipeline error for %s: %s", city, exc, exc_info=True)
            stats["failed"] += 1
    
    stats["duration_sec"] = round(time.perf_counter() - start, 2)

    log.info(
        "=== Pipeline DONE fetched=%d loaded=%d failed=%d (%.2fs) ===",
        stats["fetched"], stats["loaded"], stats["failed"], stats["duration_sec"],
    )

    database.close()
    return stats

# --------------------------------------------------
# CLI Entry Point
# --------------------------------------------------
def _pars_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Beginner Weather Data Pipeline - Batch ETL",
    )
    parser.add_argument(
        "--cities",
        type=str,
        default=",".join(DEFAULT_CITIES),
        help="Comma-separated list of cities (default: built-in 8-city list)",
    )
    parser.add_argument(
        "--db",
        type=str,
        default=DEFAULT_DB,
        help=f"SQLite database file path (default: {DEFAULT_DB})",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    cities = [c.strip() for c in args.cities.split(",") if c.strip()]

    result = run_pipeline(cities, args.db)
    sys.exit(0 if result["failed"] == 0 else 1)
