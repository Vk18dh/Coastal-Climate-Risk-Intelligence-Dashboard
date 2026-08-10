from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("")
async def get_reports_data():
    """
    GET /api/v1/reports
    Returns downloadable PDF / CSV executive reports metadata.
    (Structural route boundary - Report generation service deferred to Sprint 3)
    """
    return {
        "success": True,
        "message": "Reports API endpoint registered. Report generation service prepared.",
        "data": {
            "status": "route_registered",
            "module": "app.services.report_service"
        }
    }
