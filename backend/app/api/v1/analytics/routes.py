"""
Analytics API endpoints — Phase 6 Statistical Analytics.
"""
from fastapi import APIRouter, Query

from app.schemas.analytics import (
    ComparisonResult,
    CorrelationResult,
    RiskDistributionResult,
    TimeSeriesResult,
)
from app.services.analytics_service import analytics_service

router = APIRouter()


@router.get("/timeseries", response_model=TimeSeriesResult, summary="Get historical metric timeseries and stats")
async def get_timeseries(
    region_id: int = Query(1, description="Region ID"),
    metric: str = Query("rainfall", description="Metric to analyze: rainfall, tide, or risk"),
    days: int = Query(30, ge=2, le=90, description="Analysis window in days (default: 30)"),
) -> TimeSeriesResult:
    """
    Retrieve daily-aligned observations along with descriptive statistics
    (count, min, max, mean, median, sample standard deviation, and trend).
    """
    return analytics_service.get_timeseries(region_id, metric, days=days)


@router.get("/correlation", response_model=CorrelationResult, summary="Compute Pearson correlation for paired metrics")
async def get_correlation(
    region_id: int = Query(1, description="Region ID"),
    variable_x: str = Query("rainfall", description="First metric in pair (e.g. rainfall)"),
    variable_y: str = Query("risk", description="Second metric in pair (e.g. risk or tide)"),
    days: int = Query(30, ge=2, le=90, description="Analysis window in days"),
) -> CorrelationResult:
    """
    Compute Pearson correlation across strictly paired daily observations.
    Note: Statistical association only, not causal inference.
    """
    return analytics_service.get_correlation(region_id, variable_x, variable_y, days=days)


@router.get("/distribution", response_model=RiskDistributionResult, summary="Get risk classification distribution")
async def get_risk_distribution(
    region_id: int = Query(1, description="Region ID"),
    days: int = Query(30, ge=2, le=90, description="Analysis window in days"),
) -> RiskDistributionResult:
    """Retrieve percentage distribution across Low, Moderate, High, and Critical risk categories."""
    return analytics_service.get_risk_distribution(region_id, days=days)


@router.get("/comparison", response_model=ComparisonResult, summary="Compare metric across coastal regions")
async def get_comparison(
    metric: str = Query("risk", description="Metric to compare: rainfall, tide, or risk"),
    days: int = Query(30, ge=2, le=90, description="Analysis window in days"),
) -> ComparisonResult:
    """Compare descriptive statistics for a chosen metric across all monitored coastal zones."""
    return analytics_service.get_comparison(metric, days=days)

