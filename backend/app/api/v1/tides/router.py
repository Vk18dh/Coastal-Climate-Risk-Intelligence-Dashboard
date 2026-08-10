from fastapi import APIRouter

router = APIRouter(prefix="/tides", tags=["Tides"])


@router.get("")
async def get_tides_data():
    """
    GET /api/v1/tides
    Returns ocean tide and sea surface observations.
    (Structural route boundary - Oceanographic data integration deferred to Sprint 2)
    """
    return {
        "success": True,
        "message": "Tides API endpoint registered. Oceanographic data integration scheduled for Sprint 2.",
        "data": {
            "status": "route_registered",
            "provider": "open-meteo-marine",
            "module": "app.services.tide_service"
        }
    }
