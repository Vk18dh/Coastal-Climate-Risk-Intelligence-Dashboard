"""
AI Insights API endpoints.
"""
from typing import Any, Dict
from fastapi import APIRouter, Body, HTTPException, Path

from app.services.ai_service import ai_service

router = APIRouter()


@router.get("/regions/{region_id}/insights", summary="Get grounded AI insights for a coastal region")
async def get_region_insights(
    region_id: int = Path(..., description="Region ID")
) -> Dict[str, Any]:
    """
    Retrieve grounded explanation of region's climate risk, contributor analysis,
    practical recommendations, and limitations.
    Uses local Qwen 3 if available, or deterministic rule reasoning fallback.
    """
    insights = await ai_service.get_insights(region_id)
    if "error" in insights:
        raise HTTPException(status_code=404, detail=insights["error"])
    return insights


@router.post("/ask", summary="Ask an interactive question about coastal risk")
async def ask_ai_question(
    region_id: int = Body(1, description="Target region ID"),
    question: str = Body(..., description="User question (e.g. 'Why is this region at risk?')")
) -> Dict[str, Any]:
    """
    Interactive Q&A grounded strictly in deterministic backend CCRI metrics.
    """
    return await ai_service.answer_question(region_id, question)

