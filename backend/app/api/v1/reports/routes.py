"""
Reports API endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Path

from app.schemas.report import ClimateRiskReport, GenerateReportRequest
from app.services.report_service import report_service

router = APIRouter()


@router.post("/generate", response_model=ClimateRiskReport, summary="Generate regional climate risk assessment report")
async def generate_report(request: GenerateReportRequest) -> ClimateRiskReport:
    """Generate a structured, evidence-based climate risk assessment report for a coastal region."""
    try:
        return await report_service.generate_report(request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[ClimateRiskReport], summary="List all generated reports")
async def list_reports() -> List[ClimateRiskReport]:
    """Retrieve history of all generated risk assessment reports."""
    return report_service.list_reports()


@router.get("/{report_id}", response_model=ClimateRiskReport, summary="Get generated report by ID")
async def get_report(
    report_id: str = Path(..., description="Report unique identifier")
) -> ClimateRiskReport:
    """Retrieve full structured report document."""
    rep = report_service.get_report(report_id)
    if not rep:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
    return rep

