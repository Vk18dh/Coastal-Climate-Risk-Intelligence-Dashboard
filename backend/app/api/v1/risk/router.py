from fastapi import APIRouter, Query
from app.services.risk_service import risk_service

router = APIRouter(prefix="/risk", tags=["Risk Engine"])


@router.get("")
async def get_all_risk_scores():
    """
    GET /api/v1/risk
    Returns calculated Composite Climate Risk Index for all coastal regions.
    """
    data = risk_service.get_all_region_risks()
    return {
        "success": True,
        "message": f"Successfully calculated climate risk scores for {len(data)} coastal regions.",
        "data": data
    }


@router.get("/{region_id}")
async def get_risk_score_by_region(region_id: int):
    """
    GET /api/v1/risk/{region_id}
    Returns detailed multi-hazard climate risk breakdown for a specific coastal region.
    """
    data = risk_service.compute_risk_for_region(region_id)
    return {
        "success": True,
        "message": f"Climate risk breakdown generated for region {region_id}.",
        "data": data
    }
