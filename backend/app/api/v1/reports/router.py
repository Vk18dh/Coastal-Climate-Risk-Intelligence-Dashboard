from fastapi import APIRouter, Query
from app.services.report_service import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("")
async def get_report_data(region_id: int = Query(1, description="Region ID to generate report for")):
    """
    GET /api/v1/reports
    Generates a full structured Climate Risk Intelligence Snapshot Report for download.
    """
    report = report_service.generate_full_report(region_id)
    return {
        "success": True,
        "message": f"Full Climate Risk Intelligence Report generated for region {region_id}.",
        "data": report
    }
