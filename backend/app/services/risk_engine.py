import logging
from datetime import datetime
from typing import Dict, Optional

from app.config.engine import RiskEngineConfig
from app.schemas.risk import RiskEngineResult

logger = logging.getLogger(__name__)


class ClimateRiskEngine:
    """
    Deterministic Climate Risk Engine.
    Converts raw environmental data into a Composite Climate Risk Index (CCRI).
    """

    @staticmethod
    def _normalize_rainfall(rainfall_mm: float) -> float:
        if rainfall_mm < 0:
            return 0.0
        if rainfall_mm >= RiskEngineConfig.RAINFALL_MAX_MM:
            return 1.0
        return rainfall_mm / RiskEngineConfig.RAINFALL_MAX_MM

    @staticmethod
    def _normalize_tide(tide_m: float) -> float:
        if tide_m < 0:
            return 0.0
        if tide_m >= RiskEngineConfig.TIDE_MAX_M:
            return 1.0
        return tide_m / RiskEngineConfig.TIDE_MAX_M

    @staticmethod
    def _normalize_elevation(elevation_m: float) -> float:
        """Inverted logic: lower elevation -> higher risk."""
        if elevation_m <= RiskEngineConfig.ELEVATION_MIN_M:
            return 1.0
        if elevation_m >= RiskEngineConfig.ELEVATION_MAX_M:
            return 0.0
        
        range_m = RiskEngineConfig.ELEVATION_MAX_M - RiskEngineConfig.ELEVATION_MIN_M
        # Map ELEVATION_MIN_M -> 1.0, ELEVATION_MAX_M -> 0.0
        val = 1.0 - ((elevation_m - RiskEngineConfig.ELEVATION_MIN_M) / range_m)
        return val

    @staticmethod
    def _normalize_flood(severity_str: str) -> float:
        return RiskEngineConfig.FLOOD_SEVERITY_MAPPING.get(severity_str.lower().strip(), 0.0)

    @staticmethod
    def _classify_risk(score: float) -> str:
        for level, threshold in RiskEngineConfig.CLASSIFICATION_THRESHOLDS.items():
            if score <= threshold:
                return level
        return "Critical" # Fallback if > 100 somehow

    def calculate(
        self,
        region_id: int,
        timestamp: datetime,
        rainfall_mm: Optional[float] = None,
        tide_m: Optional[float] = None,
        elevation_m: Optional[float] = None,
        flood_severity: Optional[str] = None,
    ) -> RiskEngineResult:
        
        # 1. Normalize available inputs
        raw_scores: Dict[str, Optional[float]] = {
            "rainfall_score": self._normalize_rainfall(rainfall_mm) if rainfall_mm is not None else None,
            "tide_score": self._normalize_tide(tide_m) if tide_m is not None else None,
            "elevation_score": self._normalize_elevation(elevation_m) if elevation_m is not None else None,
            "flood_score": self._normalize_flood(flood_severity) if flood_severity is not None else None,
        }

        # 2. Identify missing components
        missing = [k for k, v in raw_scores.items() if v is None]
        available_count = len(RiskEngineConfig.WEIGHTS) - len(missing)
        data_completeness = available_count / len(RiskEngineConfig.WEIGHTS)

        warnings = []
        if missing:
            warnings.append(f"Missing data for components: {', '.join(missing)}")

        # 3. Handle Missing Data Modes
        effective_weights = dict(RiskEngineConfig.WEIGHTS)
        
        if missing:
            if RiskEngineConfig.MISSING_DATA_MODE == "STRICT":
                return RiskEngineResult(
                    region_id=region_id,
                    timestamp=timestamp,
                    final_score=None,
                    risk_level=None,
                    component_scores=raw_scores,
                    original_weights=RiskEngineConfig.WEIGHTS,
                    effective_weights=effective_weights,
                    methodology_version=RiskEngineConfig.METHODOLOGY_VERSION,
                    normalization_config_version=RiskEngineConfig.NORMALIZATION_CONFIG_VERSION,
                    data_completeness=data_completeness,
                    missing_components=missing,
                    warnings=warnings + ["Strict mode enforced: insufficient data for calculation."],
                    status="insufficient_data"
                )
            elif RiskEngineConfig.MISSING_DATA_MODE == "RENORMALIZE":
                # Proportional redistribution of weights among available components
                available_weight_sum = sum(RiskEngineConfig.WEIGHTS[k] for k, v in raw_scores.items() if v is not None)
                if available_weight_sum == 0:
                    warnings.append("No data available to renormalize.")
                    return RiskEngineResult(
                        region_id=region_id,
                        timestamp=timestamp,
                        final_score=None,
                        risk_level=None,
                        component_scores=raw_scores,
                        original_weights=RiskEngineConfig.WEIGHTS,
                        effective_weights=effective_weights,
                        methodology_version=RiskEngineConfig.METHODOLOGY_VERSION,
                        normalization_config_version=RiskEngineConfig.NORMALIZATION_CONFIG_VERSION,
                        data_completeness=data_completeness,
                        missing_components=missing,
                        warnings=warnings,
                        status="insufficient_data"
                    )
                
                # Redistribute missing weight
                for k in effective_weights.keys():
                    if k in missing:
                        effective_weights[k] = 0.0
                    else:
                        # e.g., if total available weight was 0.8, a 0.4 weight becomes 0.4 / 0.8 = 0.5
                        effective_weights[k] = RiskEngineConfig.WEIGHTS[k] / available_weight_sum
                        
                warnings.append("Renormalize mode applied: missing component weights redistributed.")

        # 4. Calculate Final Composite Score [0.0, 100.0]
        final_score = 0.0
        for key, score in raw_scores.items():
            if score is not None:
                final_score += score * effective_weights[key]
        final_score *= 100.0

        # 5. Classify Risk
        risk_level = self._classify_risk(final_score)

        return RiskEngineResult(
            region_id=region_id,
            timestamp=timestamp,
            final_score=final_score,
            risk_level=risk_level,
            component_scores=raw_scores,
            original_weights=RiskEngineConfig.WEIGHTS,
            effective_weights=effective_weights,
            methodology_version=RiskEngineConfig.METHODOLOGY_VERSION,
            normalization_config_version=RiskEngineConfig.NORMALIZATION_CONFIG_VERSION,
            data_completeness=data_completeness,
            missing_components=missing,
            warnings=warnings,
            status="success"
        )
