from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class RiskEngineResult(BaseModel):
    """
    Structured output from the Climate Risk Engine.
    Contains both the computed scores and traceability metadata.
    """
    region_id: int
    timestamp: datetime
    
    # Core output
    final_score: Optional[float] = Field(None, description="Composite Climate Risk Index (0-100)")
    risk_level: Optional[str] = Field(None, description="Risk classification (e.g., Low, Moderate, High, Critical)")
    component_scores: Dict[str, Optional[float]] = Field(
        ..., description="Normalized component scores (0.0 - 1.0)"
    )
    
    # Traceability and explainability metadata
    original_weights: Dict[str, float] = Field(..., description="Configured baseline weights")
    effective_weights: Dict[str, float] = Field(..., description="Actual weights applied (adjusted for missing data)")
    methodology_version: str = Field(..., description="Methodology version identifier (e.g. demo-1.0)")
    normalization_config_version: str = Field(..., description="Configuration parameters version")
    
    # Data quality
    data_completeness: float = Field(..., description="Ratio of available components to required components (0.0 - 1.0)")
    missing_components: List[str] = Field(default_factory=list, description="List of component keys that were missing")
    warnings: List[str] = Field(default_factory=list, description="Any warnings generated during calculation")
    status: str = Field(..., description="'success' or 'insufficient_data'")
