"""
Region schemas for Coastal Climate Risk Intelligence Dashboard.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.schemas.risk import RiskEngineResult


class RegionBase(BaseModel):
    name: str = Field(..., description="Region name")
    district: str = Field(..., description="District name")
    state: Optional[str] = Field(None, description="State name")
    description: Optional[str] = Field(None, description="Region description and vulnerability overview")
    elevation_m: float = Field(..., description="Mean topographic elevation in meters")
    flood_severity: str = Field("none", description="Historical flood severity classification")


class RegionCoordinates(BaseModel):
    latitude: float
    longitude: float


class RegionSummary(RegionBase):
    id: int
    coordinates: RegionCoordinates
    coast: Optional[str] = None
    latest_risk: Optional[RiskEngineResult] = None
    latest_rainfall_mm: Optional[float] = None
    latest_tide_m: Optional[float] = None
    data_freshness: str = "Current Demo Baseline"
    data_provenance: Dict[str, str] = Field(
        default_factory=lambda: {
            "weather": "open-meteo (DEMO SEED)",
            "tide": "mock-tide-engine (DEMO MOCK - NOT INCOIS)",
            "elevation": "coastal-topographic-dem (DEMO DATA)",
            "risk_engine": "CCRI Phase 5 Deterministic Engine",
        }
    )


class RegionDetail(RegionSummary):
    geojson_polygon: Optional[Dict[str, Any]] = None
    historical_flood_events_count: int = 0
    monitoring_stations: int = 1

