import datetime
from typing import Dict, Any
from app.services.region_service import region_service
from app.services.risk_service import risk_service
from app.services.weather_service import weather_service
from app.services.tide_service import tide_service
from app.services.ai_service import ai_service

class ReportService:
    """Service layer boundary for generating comprehensive downloadable climate risk intelligence reports."""

    def generate_full_report(self, region_id: int) -> Dict[str, Any]:
        region = region_service.get_region_by_id(region_id) or {"id": region_id, "name": f"Region {region_id}"}
        weather = weather_service.get_weather_for_region(region_id)
        tides = tide_service.get_tides_for_region(region_id)
        risk = risk_service.compute_risk_for_region(region_id)
        ai_advisory = ai_service.generate_ai_report(region_id)

        return {
            "report_id": f"REP-{region_id}-{int(datetime.datetime.now().timestamp())}",
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "region": region,
            "weather": weather,
            "tides": tides,
            "risk_assessment": risk,
            "ai_executive_advisory": ai_advisory
        }

report_service = ReportService()
