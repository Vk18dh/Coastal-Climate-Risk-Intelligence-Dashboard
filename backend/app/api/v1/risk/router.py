from fastapi import APIRouter

router = APIRouter(prefix="/risk", tags=["Risk Engine"])


@router.get("")
async def get_risk_data():
    """
    GET /api/v1/risk
    Returns calculated composite climate risk index.
    (Structural route boundary - Climate Risk Engine calculation deferred to Sprint 3)
    """
    return {
        "success": True,
        "message": "Risk API endpoint registered. Climate Risk Engine integration scheduled for Sprint 3.",
        "data": {
            "status": "route_registered",
            "module": "app.services.risk_service"
        }
    }
