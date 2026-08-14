import datetime
from typing import Dict, Any, List
from app.services.region_service import region_service
from app.services.weather_service import weather_service
from app.services.tide_service import tide_service

class RiskService:
    """
    Climate Risk Engine Service.
    Computes Composite Climate Risk Index based on weighted multi-hazard parameters:
    Risk = (0.35 * RainfallScore) + (0.30 * TideScore) + (0.20 * ElevationScore) + (0.15 * FloodHistoryScore)
    """

    def compute_risk_for_region(self, region_id: int) -> Dict[str, Any]:
        region = region_service.get_region_by_id(region_id)
        if not region:
            region = {"id": 1, "name": "Mumbai South Coast & Harbor", "vulnerability_tier": "High"}

        weather = weather_service.get_weather_for_region(region_id)
        tide = tide_service.get_tides_for_region(region_id)

        # 1. Rainfall Score (0-100)
        rainfall_mm = weather.get("rainfall_mm", 0.0)
        rainfall_score = min(100.0, (rainfall_mm / 150.0) * 100.0)

        # 2. Tide Score (0-100)
        tide_height_m = tide.get("tide_height_m", 1.0)
        tide_score = min(100.0, (tide_height_m / 4.0) * 100.0)

        # 3. Elevation Vulnerability Score (0-100, lower elevation = higher score)
        elev_data = region.get("elevation", {})
        mean_elev = elev_data.get("mean_m", 5.0)
        elevation_score = max(0.0, min(100.0, (15.0 - mean_elev) * 6.66))

        # 4. Historical Flood Vulnerability Score (0-100)
        vulnerability_tier = region.get("vulnerability_tier", "Medium")
        tier_scores = {"Low": 25.0, "Moderate": 50.0, "High": 75.0, "Critical": 95.0}
        flood_score = tier_scores.get(vulnerability_tier, 50.0)

        # Calculate composite weighted risk score
        final_score = round(
            (0.35 * rainfall_score) +
            (0.30 * tide_score) +
            (0.20 * elevation_score) +
            (0.15 * flood_score),
            1
        )

        # Determine Risk Classification Level
        if final_score >= 75.0:
            risk_level = "Critical"
        elif final_score >= 55.0:
            risk_level = "High"
        elif final_score >= 35.0:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        return {
            "region_id": region.get("id"),
            "region_name": region.get("name"),
            "district": region.get("district"),
            "state": region.get("state"),
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "composite_risk_score": final_score,
            "risk_level": risk_level,
            "component_scores": {
                "rainfall_score": round(rainfall_score, 1),
                "tide_score": round(tide_score, 1),
                "elevation_vulnerability_score": round(elevation_score, 1),
                "historical_flood_score": round(flood_score, 1),
            },
            "contributing_factors": {
                "current_rainfall_mm": rainfall_mm,
                "current_tide_height_m": tide_height_m,
                "mean_elevation_m": mean_elev,
                "vulnerability_tier": vulnerability_tier
            }
        }

    def get_all_region_risks(self) -> List[Dict[str, Any]]:
        """Computes climate risk index for all registered coastal regions."""
        regions = region_service.get_all_regions()
        risks = []
        for r in regions:
            risks.append(self.compute_risk_for_region(r["id"]))
        return sorted(risks, key=lambda x: x["composite_risk_score"], reverse=True)

risk_service = RiskService()
