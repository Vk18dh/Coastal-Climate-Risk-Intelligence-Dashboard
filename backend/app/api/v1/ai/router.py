from fastapi import APIRouter

router = APIRouter(prefix="/ai-report", tags=["AI Intelligence"])


@router.get("")
async def get_ai_report():
    """
    GET /api/v1/ai-report
    Returns AI-generated executive summaries and advisories.
    (Structural route boundary - Groq LLM integration deferred to Sprint 3)
    """
    return {
        "success": True,
        "message": "AI Advisory API endpoint registered. Groq LLM intelligence generation scheduled for Sprint 3.",
        "data": {
            "status": "route_registered",
            "provider": "groq",
            "module": "app.services.ai_service"
        }
    }
