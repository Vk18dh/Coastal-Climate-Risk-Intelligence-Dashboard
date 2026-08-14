from fastapi import APIRouter
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("")
async def get_analytics_summary():
    """
    GET /api/v1/analytics
    Returns statistical climate analytics, risk distributions, and historical flood trends.
    """
    data = analytics_service.get_analytics_summary()
    return {
        "success": True,
        "message": "Statistical climate analytics summary retrieved.",
        "data": data
    }


@router.get("/historical-floods")
async def get_historical_floods():
    """
    GET /api/v1/analytics/historical-floods
    Returns historical disaster events and inundation records.
    """
    floods = analytics_service.get_historical_floods()
    return {
        "success": True,
        "message": f"Retrieved {len(floods)} historical flood records.",
        "data": floods
    }
