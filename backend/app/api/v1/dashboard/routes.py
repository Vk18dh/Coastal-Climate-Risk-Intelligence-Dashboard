"""
Dashboard API endpoints.
"""
from fastapi import APIRouter

from app.schemas.dashboard import DashboardKPIs, DashboardOverviewResponse
from app.services.dashboard_service import dashboard_service

router = APIRouter()


@router.get("", response_model=DashboardOverviewResponse, summary="Get complete dashboard overview")
async def get_dashboard() -> DashboardOverviewResponse:
    """Retrieve full dashboard state including KPI cards, Today's situation, and region summaries."""
    return dashboard_service.get_overview()


@router.get("/kpis", response_model=DashboardKPIs, summary="Get dashboard KPI cards")
async def get_dashboard_kpis() -> DashboardKPIs:
    """Retrieve system-wide aggregated KPI metrics."""
    overview = dashboard_service.get_overview()
    return overview.kpis

