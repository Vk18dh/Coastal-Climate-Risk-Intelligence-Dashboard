"""
ORM models package — Phase 3.

Importing this package registers all model classes with Base.metadata.
Alembic's env.py imports this module so autogenerate detects all tables.

Import order respects foreign-key dependencies:
  1. region     — no FK dependencies (parent of all)
  2. weather    — depends on region
  3. tide       — depends on region
  4. risk       — depends on region (contains ElevationData, HistoricalFlood, RiskScore)
  5. report     — depends on region
  6. analytics  — depends on region
"""
from app.models.analytics import AnalyticsResult
from app.models.region import Region
from app.models.report import AIReport
from app.models.risk import ElevationData, HistoricalFlood, RiskScore
from app.models.tide import TideData
from app.models.weather import WeatherData

__all__ = [
    "Region",
    "WeatherData",
    "TideData",
    "ElevationData",
    "HistoricalFlood",
    "RiskScore",
    "AIReport",
    "AnalyticsResult",
]
