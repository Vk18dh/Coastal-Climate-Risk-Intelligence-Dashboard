"""
Report generation schemas.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.schemas.risk import RiskEngineResult


class GenerateReportRequest(BaseModel):
    region_id: int = Field(..., description="Target coastal region ID")
    include_ai_insights: bool = True
    include_statistical_trends: bool = True
    notes: Optional[str] = None


class ReportSection(BaseModel):
    title: str
    content: str
    key_metrics: Optional[Dict[str, Any]] = None


class ClimateRiskReport(BaseModel):
    report_id: str
    title: str
    generated_at: datetime
    region_id: int
    region_name: str
    district: str
    state: str
    elevation_m: float
    current_ccri: RiskEngineResult
    environmental_overview: Dict[str, Any]
    statistical_summary: Dict[str, Any]
    ai_interpretation: Optional[Dict[str, Any]] = None
    recommended_actions: List[str]
    provenance: Dict[str, str]
    disclaimer: str
    executive_summary: str

