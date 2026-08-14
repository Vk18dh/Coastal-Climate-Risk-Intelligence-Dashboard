from fastapi import APIRouter, Query
from app.services.weather_service import weather_service

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("")
async def get_weather_data(region_id: int = Query(1, description="Region ID to fetch weather for")):
    """
    GET /api/v1/weather
    Returns latest meteorological observations (temperature, rainfall, wind speed, pressure, condition).
    """
    data = weather_service.get_weather_for_region(region_id)
    return {
        "success": True,
        "message": f"Weather observations retrieved for region {region_id}.",
        "data": data
    }
