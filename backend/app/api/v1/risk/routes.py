from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.services.risk_engine import ClimateRiskEngine
from app.schemas.risk import RiskEngineResult

router = APIRouter()

def get_risk_engine() -> ClimateRiskEngine:
    return ClimateRiskEngine()

@router.get("/calculate", response_model=RiskEngineResult, summary="Test the Climate Risk Engine")
async def calculate_risk(
    region_id: int = Query(1, description="Region ID (demo)"),
    rainfall_mm: Optional[float] = Query(None, description="Rainfall in mm (e.g. 150.0)"),
    tide_m: Optional[float] = Query(None, description="Tide height in meters (e.g. 2.5)"),
    elevation_m: Optional[float] = Query(None, description="Elevation in meters (e.g. 5.0)"),
    flood_severity: Optional[str] = Query(None, description="Flood severity (none, low, moderate, high, extreme)"),
    engine: ClimateRiskEngine = Depends(get_risk_engine)
) -> RiskEngineResult:
    """
    Manually test the deterministic Climate Risk Engine with arbitrary inputs.
    Missing inputs will be handled according to ENGINE_MISSING_DATA_MODE (default: RENORMALIZE).
    """
    timestamp = datetime.now(timezone.utc)
    
    result = engine.calculate(
        region_id=region_id,
        timestamp=timestamp,
        rainfall_mm=rainfall_mm,
        tide_m=tide_m,
        elevation_m=elevation_m,
        flood_severity=flood_severity
    )
    return result
