from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("")
async def get_analytics_data():
    """
    GET /api/v1/analytics
    Returns statistical climate analytics, time series, and correlations.
    (Structural route boundary - Analytics Engine deferred to Sprint 3)
    """
    return {
        "success": True,
        "message": "Analytics API endpoint registered. Statistical engine calculation scheduled for Sprint 3.",
        "data": {
            "status": "route_registered",
            "module": "app.services.analytics_service"
        }
    }
