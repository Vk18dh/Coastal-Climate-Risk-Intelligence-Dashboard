from fastapi import APIRouter, Query
from app.services.ai_service import ai_service

router = APIRouter(prefix="/ai-report", tags=["AI Intelligence"])


@router.get("")
async def get_ai_report(region_id: int = Query(1, description="Region ID to generate AI report for")):
    """
    GET /api/v1/ai-report
    Returns AI-generated executive summaries, key threats, and actionable advisories.
    """
    data = ai_service.generate_ai_report(region_id)
    return {
        "success": True,
        "message": f"AI Climate Advisory generated for region {region_id}.",
        "data": data
    }
