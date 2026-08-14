import json
import os
from typing import Dict, Any, List
from app.config.logging import logger
from app.services.risk_service import risk_service

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FLOODS_FILE = os.path.join(BASE_DIR, "data", "processed", "historical_floods.json")

class AnalyticsService:
    """
    Service layer for statistical climate analytics, historical flood trends, and risk distribution analysis.
    """

    def get_historical_floods(self) -> List[Dict[str, Any]]:
        """Loads historical flood events dataset."""
        if os.path.exists(FLOODS_FILE):
            try:
                with open(FLOODS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading historical floods JSON: {e}")
        return []

    def get_analytics_summary(self) -> Dict[str, Any]:
        """Generates statistical analytics summary across all coastal regions."""
        risks = risk_service.get_all_region_risks()
        floods = self.get_historical_floods()

        total_regions = len(risks)
        risk_levels = {"Critical": 0, "High": 0, "Moderate": 0, "Low": 0}
        for r in risks:
            lvl = r.get("risk_level", "Moderate")
            risk_levels[lvl] = risk_levels.get(lvl, 0) + 1

        avg_score = round(sum(r["composite_risk_score"] for r in risks) / max(1, total_regions), 1)

        # Year-by-year flood frequency breakdown
        year_counts = {}
        total_economic_loss = 0.0
        total_affected = 0
        for f in floods:
            y = f.get("year")
            year_counts[y] = year_counts.get(y, 0) + 1
            total_economic_loss += f.get("economic_loss_usd_m", 0.0)
            total_affected += f.get("affected_population", 0)

        historical_trends = [{"year": k, "event_count": v} for k, v in sorted(year_counts.items())]

        return {
            "overview": {
                "total_monitored_regions": total_regions,
                "average_risk_score": avg_score,
                "total_historical_events": len(floods),
                "total_economic_loss_usd_m": round(total_economic_loss, 1),
                "total_affected_population": total_affected
            },
            "risk_distribution": risk_levels,
            "top_high_risk_regions": risks[:3],
            "historical_trends": historical_trends,
            "historical_events": floods
        }

analytics_service = AnalyticsService()
