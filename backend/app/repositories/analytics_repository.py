"""
Analytics repository implementing Phase 6 temporal alignment and observational extraction.
Retrieves and aligns daily metrics for timeseries, correlation, and comparisons.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.repositories.demo_data import DEMO_REGIONS, generate_region_timeseries
from app.services.risk_engine import ClimateRiskEngine

risk_engine = ClimateRiskEngine()


class AnalyticsRepository:
    def __init__(self):
        self._demo_regions = DEMO_REGIONS

    def get_aligned_metric_series(
        self, region_id: int, metric: str, days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Extract daily aligned observations for a specific metric in a region.
        Supported metrics: 'rainfall', 'tide', 'risk' (or 'risk_score').
        """
        reg = next((r for r in self._demo_regions if r["id"] == region_id), None)
        if not reg:
            return []

        timeseries = generate_region_timeseries(reg, days=days)
        aligned = []

        for item in timeseries:
            ts = item["timestamp"]
            rain = item["rainfall_mm"]
            tide = item["tide_height_m"]

            if metric == "rainfall":
                val = rain
            elif metric in ("tide", "tide_height"):
                val = tide
            elif metric in ("risk", "risk_score", "ccri"):
                risk_res = risk_engine.calculate(
                    region_id=reg["id"],
                    timestamp=datetime.fromisoformat(ts),
                    rainfall_mm=rain,
                    tide_m=tide,
                    elevation_m=reg["elevation_m"],
                    flood_severity=reg["flood_severity"],
                )
                val = risk_res.final_score if risk_res.final_score is not None else 0.0
            else:
                val = 0.0

            aligned.append({
                "timestamp": ts,
                "date": item["date"],
                "value": round(float(val), 2),
            })

        return aligned

    def get_paired_observations(
        self, region_id: int, var_x: str, var_y: str, days: int = 30
    ) -> List[Tuple[float, float]]:
        """
        Extract complete paired daily observations (x, y) for correlation calculation.
        Per Phase 6 spec: only complete paired observations are kept.
        """
        series_x = self.get_aligned_metric_series(region_id, var_x, days=days)
        series_y = self.get_aligned_metric_series(region_id, var_y, days=days)

        map_y = {item["date"]: item["value"] for item in series_y}
        pairs = []

        for item_x in series_x:
            date_key = item_x["date"]
            if date_key in map_y:
                val_x = item_x["value"]
                val_y = map_y[date_key]
                pairs.append((val_x, val_y))

        return pairs


analytics_repo = AnalyticsRepository()

