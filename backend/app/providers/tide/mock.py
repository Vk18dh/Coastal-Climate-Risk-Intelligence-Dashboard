"""
Mock tide provider for testing and development.
Returns randomized but plausible ocean data.
"""
import math
import random
from datetime import datetime, timedelta
from typing import List

from app.models.region import Region
from app.providers.base import TideProvider
from app.schemas.tide import TideDataCreate


class MockTideProvider(TideProvider):
    """Generates synthetic tide data with a simple sine wave for tides."""
    
    async def fetch_tides(
        self, region: Region, start_time: datetime, end_time: datetime
    ) -> List[TideDataCreate]:
        results = []
        current_time = start_time
        
        # Base offset for tide sine wave based on region id to make them distinct
        base_offset = float(region.id)
        
        while current_time <= end_time:
            # Simple semi-diurnal tide simulation (12.42 hour period)
            hours_since_epoch = current_time.timestamp() / 3600.0
            tide_cycle = (hours_since_epoch % 12.42) / 12.42
            
            # Tide height between -1.5m and +1.5m
            tide_height = math.sin(tide_cycle * 2 * math.pi + base_offset) * 1.5
            
            wave_height = random.uniform(0.2, 2.5)
            sst = random.uniform(26.0, 31.0)
            
            results.append(
                TideDataCreate(
                    region_id=region.id,
                    timestamp=current_time,
                    provider="incois-mock",
                    tide_height=tide_height,
                    wave_height=wave_height,
                    sea_surface_temperature=sst,
                )
            )
            # 1-hour increments
            current_time += timedelta(hours=1)
            
        return results
