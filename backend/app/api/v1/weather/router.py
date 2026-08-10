from fastapi import APIRouter

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("")
async def get_weather_data():
    """
    GET /api/v1/weather
    Returns latest weather observations.
    (Structural route boundary - Data ingestion deferred to Sprint 2)
    """
    return {
        "success": True,
        "message": "Weather API endpoint registered. Data ingestion scheduled for Sprint 2.",
        "data": {
            "status": "route_registered",
            "provider": "open-meteo",
            "module": "app.services.weather_service"
        }
    }
