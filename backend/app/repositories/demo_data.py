"""
Demonstration dataset for Coastal Climate Risk Intelligence Dashboard.

Contains controlled, reproducible, internally consistent data for 5 coastal regions:
1. Chennai (Tamil Nadu)
2. Mumbai (Maharashtra)
3. Kochi (Kerala)
4. Visakhapatnam (Andhra Pradesh)
5. Kolkata / Sundarbans (West Bengal)

DISCLOSURE & PROVENANCE:
- Weather data: Derived from Open-Meteo baseline patterns (DEMO DATA).
- Tide data: Synthetic tidal simulation (MOCK DATA - NOT genuine INCOIS observations).
- Elevation data: Coastal topographic reference estimates (DEMO DATA).
- Flood severity: Regional historical hazard profiles (DEMO DATA).
- Risk methodology: Phase 5 Composite Climate Risk Index (DEMO ONLY - NOT scientifically validated).
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

# Standard evaluation anchor date (last 30 days)
BASE_DATE = datetime(2026, 11, 18, 12, 0, 0, tzinfo=timezone.utc)

DEMO_REGIONS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Chennai Coastal Zone",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "coast": "East Coast (Bay of Bengal)",
        "elevation_m": 6.5,
        "flood_severity": "moderate",
        "description": "Urban coastal plain subject to seasonal northeast monsoon rains and cyclonic depressions in the Bay of Bengal.",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "base_rainfall": 45.0,
        "base_tide": 1.4,
        "geojson_coordinates": [
            [
                [80.25, 13.00],
                [80.32, 13.00],
                [80.34, 13.12],
                [80.28, 13.15],
                [80.24, 13.08],
                [80.25, 13.00]
            ]
        ]
    },
    {
        "id": 2,
        "name": "Mumbai Harbor & Suburbs",
        "district": "Mumbai City",
        "state": "Maharashtra",
        "coast": "West Coast (Arabian Sea)",
        "elevation_m": 4.2,
        "flood_severity": "high",
        "description": "High-density metropolis on reclaimed land vulnerable to severe southwest monsoon deluges and spring high tides.",
        "latitude": 18.9220,
        "longitude": 72.8347,
        "base_rainfall": 85.0,
        "base_tide": 2.2,
        "geojson_coordinates": [
            [
                [72.80, 18.90],
                [72.86, 18.90],
                [72.90, 19.05],
                [72.84, 19.10],
                [72.80, 19.00],
                [72.80, 18.90]
            ]
        ]
    },
    {
        "id": 3,
        "name": "Kochi Backwaters Zone",
        "district": "Ernakulam",
        "state": "Kerala",
        "coast": "West Coast (Arabian Sea)",
        "elevation_m": 2.1,
        "flood_severity": "extreme",
        "description": "Low-lying deltaic estuarine network with tidal backwaters subject to heavy monsoon inundation and sea-level rise pressure.",
        "latitude": 9.9312,
        "longitude": 76.2673,
        "base_rainfall": 120.0,
        "base_tide": 2.6,
        "geojson_coordinates": [
            [
                [76.22, 9.88],
                [76.30, 9.88],
                [76.32, 10.02],
                [76.25, 10.04],
                [76.21, 9.95],
                [76.22, 9.88]
            ]
        ]
    },
    {
        "id": 4,
        "name": "Visakhapatnam Port Coastal",
        "district": "Visakhapatnam",
        "state": "Andhra Pradesh",
        "coast": "East Coast (Bay of Bengal)",
        "elevation_m": 12.0,
        "flood_severity": "low",
        "description": "Natural deep-water harbor flanked by rocky coastal hills; elevated terrain moderates flood impact though cyclonic storm surges remain a hazard.",
        "latitude": 17.6868,
        "longitude": 83.2185,
        "base_rainfall": 25.0,
        "base_tide": 1.1,
        "geojson_coordinates": [
            [
                [83.20, 17.65],
                [83.28, 17.65],
                [83.33, 17.75],
                [83.27, 17.80],
                [83.18, 17.72],
                [83.20, 17.65]
            ]
        ]
    },
    {
        "id": 5,
        "name": "Sundarbans Coastal Delta",
        "district": "South 24 Parganas",
        "state": "West Bengal",
        "coast": "East Coast (Bay of Bengal Delta)",
        "elevation_m": 1.8,
        "flood_severity": "extreme",
        "description": "Vast mangrove estuarine delta with critically low elevation, severe tidal embankment vulnerability, and high cyclone susceptibility.",
        "latitude": 21.9497,
        "longitude": 88.9024,
        "base_rainfall": 140.0,
        "base_tide": 2.8,
        "geojson_coordinates": [
            [
                [88.80, 21.80],
                [89.05, 21.80],
                [89.10, 22.10],
                [88.85, 22.15],
                [88.75, 21.95],
                [88.80, 21.80]
            ]
        ]
    }
]

def generate_region_timeseries(region: Dict[str, Any], days: int = 30) -> List[Dict[str, Any]]:
    """
    Generate internally consistent daily observations for a region over the last N days.
    Values oscillate smoothly to represent realistic weather patterns and tidal cycles.
    """
    records = []
    reg_id = region["id"]
    base_rain = region["base_rainfall"]
    base_tide = region["base_tide"]

    import math
    for i in range(days):
        dt = BASE_DATE - timedelta(days=(days - 1 - i))
        # Daily variance with realistic seasonal / tidal oscillations
        rain_cycle = math.sin(i * 0.45 + reg_id) * 0.5 + 0.5
        rain_val = max(0.0, round(base_rain * rain_cycle + (12.0 if i % 7 == 0 else 0.0), 1))
        
        # Semi-diurnal / spring-neap tidal oscillation
        tide_cycle = math.sin(i * 0.6 + reg_id * 1.5) * 0.4 + 0.6
        tide_val = round(min(3.2, max(0.5, base_tide * tide_cycle)), 2)

        records.append({
            "region_id": reg_id,
            "timestamp": dt.isoformat(),
            "date": dt.strftime("%Y-%m-%d"),
            "rainfall_mm": rain_val,
            "temperature_c": round(27.0 + math.cos(i * 0.2) * 3.5, 1),
            "wind_speed_kmh": round(15.0 + math.sin(i * 0.5) * 12.0, 1),
            "humidity_percent": round(70.0 + math.sin(i * 0.3) * 18.0, 1),
            "pressure_hpa": round(1008.0 - rain_val * 0.1, 1),
            "tide_height_m": tide_val,
            "wave_height_m": round(0.8 + (rain_val / 80.0) + (tide_val * 0.3), 2),
            "weather_provider": "open-meteo (DEMO SEED)",
            "tide_provider": "mock-tide-engine (DEMO MOCK - NOT INCOIS)",
        })
    return records

