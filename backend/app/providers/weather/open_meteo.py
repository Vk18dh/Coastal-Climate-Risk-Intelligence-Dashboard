import httpx
import logging
from datetime import datetime
from typing import List

from app.models.region import Region
from app.providers.base import WeatherProvider
from app.providers.exceptions import ProviderConnectionError, ProviderValidationError
from app.schemas.weather import WeatherDataCreate

logger = logging.getLogger(__name__)


class OpenMeteoWeatherProvider(WeatherProvider):
    """
    Fetches historical and forecast weather data from the open-meteo API.
    Does not require an API key.
    """
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    async def fetch_weather(
        self, region: Region, start_time: datetime, end_time: datetime
    ) -> List[WeatherDataCreate]:
        
        # Simple extraction of first coordinate pair if region geometry is available as WKT.
        # Fallback to equator coordinates if extraction fails or geometry is raw WKB.
        lat, lon = 0.0, 0.0
        try:
            if isinstance(region.geometry, str) and "POLYGON" in region.geometry:
                coords_str = region.geometry.split("((")[-1].split("))")[0]
                first_pair = coords_str.split(",")[0].strip().split(" ")
                lon, lat = float(first_pair[0]), float(first_pair[1])
        except Exception:
            logger.warning(f"Could not parse coordinates for region {region.id}. Using 0,0.")
            
        # Open-Meteo takes ISO8601 dates (YYYY-MM-DD)
        start_date = start_time.strftime("%Y-%m-%d")
        end_date = end_time.strftime("%Y-%m-%d")
        
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,surface_pressure",
            "timezone": "UTC"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.BASE_URL, params=params, timeout=15.0)
                response.raise_for_status()
            except httpx.RequestError as e:
                raise ProviderConnectionError(f"Network error connecting to Open-Meteo: {e}")
            except httpx.HTTPStatusError as e:
                raise ProviderConnectionError(f"HTTP error {e.response.status_code} from Open-Meteo")
                
        try:
            data = response.json()
            hourly = data.get("hourly", {})
            times = hourly.get("time", [])
            temps = hourly.get("temperature_2m", [])
            humidities = hourly.get("relative_humidity_2m", [])
            precipitations = hourly.get("precipitation", [])
            wind_speeds = hourly.get("wind_speed_10m", [])
            pressures = hourly.get("surface_pressure", [])
            
            results = []
            for i, time_str in enumerate(times):
                obs_time = datetime.fromisoformat(time_str)
                
                # Filter strictly by requested datetime bounds
                if start_time <= obs_time <= end_time:
                    results.append(
                        WeatherDataCreate(
                            region_id=region.id,
                            timestamp=obs_time,
                            provider="open-meteo",
                            temperature=temps[i],
                            humidity=humidities[i],
                            rainfall=precipitations[i],
                            wind_speed=wind_speeds[i],
                            pressure=pressures[i]
                        )
                    )
            return results
        except (ValueError, TypeError, KeyError, IndexError) as e:
            raise ProviderValidationError(f"Invalid response structure from Open-Meteo: {e}")
