"""
Pydantic schemas for Weather data ingestion and API responses.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WeatherDataCreate(BaseModel):
    """
    Schema for validating incoming weather data before DB insertion.
    Normalizes data from various providers.
    """
    region_id: int
    timestamp: datetime
    provider: str
    
    # Measurements - nullable as providers might not have all data
    rainfall: Optional[float] = Field(None, description="Rainfall in mm")
    temperature: Optional[float] = Field(None, description="Temperature in °C")
    humidity: Optional[float] = Field(None, description="Humidity percentage")
    wind_speed: Optional[float] = Field(None, description="Wind speed in km/h")
    pressure: Optional[float] = Field(None, description="Atmospheric pressure in hPa")


class WeatherDataResponse(WeatherDataCreate):
    """
    Schema for API responses containing weather data.
    """
    id: int

    class Config:
        from_attributes = True
