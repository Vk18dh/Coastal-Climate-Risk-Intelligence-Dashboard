"""
Mock weather provider for testing and development.
Returns randomized but plausible data without requiring external API keys.
"""
import random
from datetime import datetime, timedelta
from typing import List

from app.models.region import Region
from app.providers.base import WeatherProvider
from app.schemas.weather import WeatherDataCreate


class MockWeatherProvider(WeatherProvider):
    """Generates synthetic weather data for the requested time range."""
    
    async def fetch_weather(
        self, region: Region, start_time: datetime, end_time: datetime
    ) -> List[WeatherDataCreate]:
        results = []
        current_time = start_time
        
        while current_time <= end_time:
            # Generate plausible dummy values
            temp = random.uniform(22.0, 35.0)
            rainfall = random.uniform(0.0, 15.0) if random.random() > 0.7 else 0.0
            humidity = random.uniform(60.0, 95.0)
            wind = random.uniform(5.0, 45.0)
            pressure = random.uniform(995.0, 1015.0)
            
            results.append(
                WeatherDataCreate(
                    region_id=region.id,
                    timestamp=current_time,
                    provider="mock",
                    temperature=temp,
                    rainfall=rainfall,
                    humidity=humidity,
                    wind_speed=wind,
                    pressure=pressure,
                )
            )
            # 1-hour increments
            current_time += timedelta(hours=1)
            
        return results
