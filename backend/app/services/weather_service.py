import datetime
import urllib.request
import json
from typing import Dict, Any, Optional
from app.config.settings import settings
from app.config.logging import logger
from app.services.region_service import region_service

class WeatherService:
    """
    Service layer for meteorological weather data processing.
    Fetches real-time observations via Open-Meteo free weather API with realistic fallback generation.
    """

    def fetch_live_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Fetches live meteorological observations from Open-Meteo API."""
        try:
            url = (
                f"{settings.WEATHER_API_URL}?"
                f"latitude={lat}&longitude={lon}&"
                f"current=temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,weather_code"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "CoastalClimatePlatform/1.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                if resp.status == 200:
                    payload = json.loads(resp.read().decode("utf-8"))
                    curr = payload.get("current", {})
                    
                    code = curr.get("weather_code", 0)
                    condition = "Clear"
                    if code in [1, 2, 3]:
                        condition = "Partly Cloudy"
                    elif code in [51, 53, 55, 61, 63, 65]:
                        condition = "Rainy"
                    elif code in [80, 81, 82, 95, 96, 99]:
                        condition = "Heavy Storm / Monsoon"

                    return {
                        "temperature_c": round(curr.get("temperature_2m", 29.5), 1),
                        "rainfall_mm": round(curr.get("precipitation", 12.4), 1),
                        "humidity_pct": round(curr.get("relative_humidity_2m", 82.0), 1),
                        "wind_speed_kmh": round(curr.get("wind_speed_10m", 24.5), 1),
                        "pressure_hpa": round(curr.get("surface_pressure", 1008.5), 1),
                        "condition": condition,
                        "provider": "Open-Meteo Live API"
                    }
        except Exception as e:
            logger.warning(f"Failed to fetch live weather from Open-Meteo for ({lat}, {lon}): {e}")
        return None

    def get_weather_for_region(self, region_id: int) -> Dict[str, Any]:
        """Gets weather observations for a specific coastal region."""
        region = region_service.get_region_by_id(region_id)
        if not region:
            region = {
                "id": 1,
                "name": "Mumbai South Coast & Harbor",
                "latitude": 18.9388,
                "longitude": 72.8353
            }

        lat = region.get("latitude", 18.9388)
        lon = region.get("longitude", 72.8353)

        live = self.fetch_live_weather(lat, lon)
        if live:
            live.update({
                "region_id": region.get("id"),
                "region_name": region.get("name"),
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
            return live

        # Baseline fallback weather data
        return {
            "region_id": region.get("id"),
            "region_name": region.get("name"),
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "temperature_c": 30.2,
            "rainfall_mm": 28.5,
            "humidity_pct": 85.0,
            "wind_speed_kmh": 22.4,
            "pressure_hpa": 1006.2,
            "condition": "Monsoon Showers",
            "provider": "Regional Baseline Fallback"
        }

weather_service = WeatherService()
