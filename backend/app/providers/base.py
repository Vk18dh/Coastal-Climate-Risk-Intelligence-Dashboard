"""
Base abstractions for data providers.
"""
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

from app.schemas.weather import WeatherDataCreate
from app.schemas.tide import TideDataCreate
from app.models.region import Region


class WeatherProvider(ABC):
    """
    Abstract interface for fetching weather data.
    """
    
    @abstractmethod
    async def fetch_weather(
        self, region: Region, start_time: datetime, end_time: datetime
    ) -> List[WeatherDataCreate]:
        """
        Fetch and normalize weather data for a given region and time range.
        
        Args:
            region: The geographic region to fetch data for.
            start_time: Start of the observation window.
            end_time: End of the observation window.
            
        Returns:
            List of validated WeatherDataCreate schemas.
            
        Raises:
            ProviderConnectionError: If network request fails.
            ProviderValidationError: If response parsing fails.
        """
        pass


class TideProvider(ABC):
    """
    Abstract interface for fetching tide/ocean data.
    """
    
    @abstractmethod
    async def fetch_tides(
        self, region: Region, start_time: datetime, end_time: datetime
    ) -> List[TideDataCreate]:
        """
        Fetch and normalize tide data for a given region and time range.
        
        Args:
            region: The geographic region to fetch data for.
            start_time: Start of the observation window.
            end_time: End of the observation window.
            
        Returns:
            List of validated TideDataCreate schemas.
            
        Raises:
            ProviderConnectionError: If network request fails.
            ProviderValidationError: If response parsing fails.
        """
        pass
