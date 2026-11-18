"""
Pydantic schemas for Tide/Ocean data ingestion and API responses.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TideDataCreate(BaseModel):
    """
    Schema for validating incoming tide data before DB insertion.
    Normalizes data from various providers.
    """
    region_id: int
    timestamp: datetime
    provider: str
    
    # Measurements - nullable as providers might not have all data
    tide_height: Optional[float] = Field(None, description="Tide height in meters")
    wave_height: Optional[float] = Field(None, description="Wave height in meters")
    sea_surface_temperature: Optional[float] = Field(None, description="SST in °C")


class TideDataResponse(TideDataCreate):
    """
    Schema for API responses containing tide data.
    """
    id: int

    class Config:
        from_attributes = True
