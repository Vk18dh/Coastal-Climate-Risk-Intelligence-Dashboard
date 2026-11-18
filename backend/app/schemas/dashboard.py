"""
Dashboard schemas for Overview, KPI Cards, and System Summary.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.schemas.region import RegionSummary


class KPICard(BaseModel):
    title: str
    value: str
    numeric_value: Optional[float] = None
    unit: Optional[str] = None
    status: str = Field(..., description="normal, warning, critical, or info")
    subtext: str
    icon: str


class DashboardKPIs(BaseModel):
    overall_risk_score: KPICard
    high_risk_regions: KPICard
    active_alerts: KPICard
    average_rainfall: KPICard
    average_tide: KPICard
    timestamp: datetime


class TodaySituation(BaseModel):
    timestamp: datetime
    overall_classification: str
    overall_score: float
    headline: str
    summary_text: str
    main_contributors: List[str]
    active_alerts_count: int
    data_freshness: str
    provenance: Dict[str, str]
    methodology_disclosure: str = (
        "DEMO ONLY: Current CCRI weights and thresholds are configured for prototype demonstration "
        "and have not undergone scientific peer validation or official disaster agency certification."
    )


class DashboardOverviewResponse(BaseModel):
    kpis: DashboardKPIs
    today_situation: TodaySituation
    regions: List[RegionSummary]

