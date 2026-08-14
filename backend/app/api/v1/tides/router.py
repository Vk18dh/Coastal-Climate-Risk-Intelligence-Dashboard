from fastapi import APIRouter, Query
from app.services.tide_service import tide_service

router = APIRouter(prefix="/tides", tags=["Tides"])


@router.get("")
async def get_tides_data(region_id: int = Query(1, description="Region ID to fetch tide data for")):
    """
    GET /api/v1/tides
    Returns ocean tide, wave height, sea surface temperature, and anomaly metrics.
    """
    data = tide_service.get_tides_for_region(region_id)
    return {
        "success": True,
        "message": f"Tide and ocean observations retrieved for region {region_id}.",
        "data": data
    }
