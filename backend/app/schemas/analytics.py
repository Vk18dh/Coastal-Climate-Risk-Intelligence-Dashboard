from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

# ── Base / Shared ─────────────────────────────────────────────────────────────

class Trend(BaseModel):
    first_value: float = Field(..., description="First value in the time window")
    last_value: float = Field(..., description="Last value in the time window")
    absolute_change: float = Field(..., description="Absolute change (last - first)")
    percentage_change: Optional[float] = Field(
        None, description="Percentage change. Null if first_value is 0."
    )

class DescriptiveStats(BaseModel):
    count: int = Field(..., description="Number of valid observations")
    min: Optional[float] = Field(None, description="Minimum value")
    max: Optional[float] = Field(None, description="Maximum value")
    mean: Optional[float] = Field(None, description="Arithmetic mean")
    median: Optional[float] = Field(None, description="Median value")
    sample_stddev: Optional[float] = Field(
        None, description="Sample standard deviation (n-1 degrees of freedom). Null if n < 2."
    )
    trend: Optional[Trend] = Field(None, description="Descriptive trend from first to last point")

class Observation(BaseModel):
    timestamp: datetime
    value: float

# ── TimeSeries ────────────────────────────────────────────────────────────────

class TimeSeriesResult(BaseModel):
    metric: str = Field(..., description="The metric analyzed (e.g., rainfall, tide, risk)")
    observations: List[Observation] = Field(default_factory=list, description="Array of time-series observations")
    statistics: DescriptiveStats = Field(..., description="Aggregated statistics over the requested period")
    provenance: Dict[str, str] = Field(
        ..., description="Metric-level data provenance (e.g., {'rainfall': 'open-meteo'})"
    )
    status: str = Field(..., description="'success' or 'insufficient_data'")

# ── Distribution ──────────────────────────────────────────────────────────────

class RiskDistributionResult(BaseModel):
    region_id: int
    distribution: Dict[str, float] = Field(
        ..., description="Percentage distribution of risk levels (e.g. {'Low': 50.0, 'Moderate': 50.0})"
    )
    count: int = Field(..., description="Total number of risk scores analyzed")
    provenance: Dict[str, str] = Field(
        ..., description="Metric-level data provenance (e.g., {'risk': 'climate-risk-engine'})"
    )
    status: str = Field(..., description="'success' or 'insufficient_data'")

# ── Correlation ───────────────────────────────────────────────────────────────

class CorrelationResult(BaseModel):
    variable_x: str = Field(..., description="First metric in the pair (e.g., rainfall)")
    variable_y: str = Field(..., description="Second metric in the pair (e.g., risk)")
    correlation: Optional[float] = Field(
        None, description="Pearson correlation coefficient (-1.0 to 1.0). Null if variance is 0 or insufficient data."
    )
    paired_observation_count: int = Field(
        ..., description="Number of strictly aligned paired observations used"
    )
    provenance: Dict[str, str] = Field(
        ..., description="Metric-level provenance (e.g., {'rainfall': 'open-meteo', 'risk': 'climate-risk-engine'})"
    )
    status: str = Field(..., description="'success' or 'insufficient_data'")

# ── Comparison ────────────────────────────────────────────────────────────────

class RegionComparison(BaseModel):
    region_id: int
    statistics: DescriptiveStats
    provenance: Dict[str, str]

class ComparisonResult(BaseModel):
    metric: str = Field(..., description="The metric compared across regions")
    regions: List[RegionComparison] = Field(default_factory=list, description="Statistics per region")
    status: str = Field(..., description="'success' or 'insufficient_data'")
