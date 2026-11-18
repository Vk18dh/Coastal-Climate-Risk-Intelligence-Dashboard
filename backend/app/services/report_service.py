"""
Report generation service — creates structured, printable, and downloadable
climate risk assessment reports for coastal regions.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.schemas.report import ClimateRiskReport, GenerateReportRequest
from app.services.ai_service import ai_service
from app.services.analytics_service import analytics_service
from app.services.region_service import region_service


class ReportService:
    def __init__(self):
        self.region_service = region_service
        self.analytics_service = analytics_service
        self.ai_service = ai_service
        self._generated_reports: Dict[str, ClimateRiskReport] = {}

    async def generate_report(self, request: GenerateReportRequest) -> ClimateRiskReport:
        region = self.region_service.get_region(request.region_id)
        if not region:
            raise ValueError(f"Region {request.region_id} not found.")

        now = datetime.now(timezone.utc)
        report_id = f"CCRI-REP-{uuid.uuid4().hex[:8].upper()}"

        # 1. Analytics & Timeseries
        rain_ts = self.analytics_service.get_timeseries(request.region_id, "rainfall", days=30)
        tide_ts = self.analytics_service.get_timeseries(request.region_id, "tide", days=30)
        risk_ts = self.analytics_service.get_timeseries(request.region_id, "risk", days=30)

        statistical_summary = {
            "rainfall_30d": rain_ts.statistics.model_dump(),
            "tide_30d": tide_ts.statistics.model_dump(),
            "risk_30d": risk_ts.statistics.model_dump(),
        }

        # 2. AI insights
        ai_data = await self.ai_service.get_insights(request.region_id)

        # 3. Environmental overview
        environmental_overview = {
            "mean_elevation_meters": region.elevation_m,
            "historical_flood_severity": region.flood_severity,
            "latest_rainfall_mm": region.latest_rainfall_mm,
            "latest_tide_meters": region.latest_tide_m,
            "coastal_orientation": region.coast or "Coastal Zone",
        }

        # 4. Executive summary
        exec_summary = (
            f"Comprehensive coastal climate risk assessment for {region.name} ({region.district}, {region.state}). "
            f"Evaluated on {now.strftime('%d %B %Y')} with an overall Composite Climate Risk Index (CCRI) of "
            f"{region.latest_risk.final_score:.1f}/100, placing the region in the {region.latest_risk.risk_level.upper()} risk category. "
            f"The primary risk contributors are low topographic elevation ({region.elevation_m}m) combined with "
            f"high tidal vulnerability."
        )

        report = ClimateRiskReport(
            report_id=report_id,
            title=f"Coastal Climate Risk Assessment: {region.name}",
            generated_at=now,
            region_id=region.id,
            region_name=region.name,
            district=region.district,
            state=region.state or "India",
            elevation_m=region.elevation_m,
            current_ccri=region.latest_risk,
            environmental_overview=environmental_overview,
            statistical_summary=statistical_summary,
            ai_interpretation=ai_data,
            recommended_actions=ai_data["recommended_actions"],
            provenance={
                "weather": "Open-Meteo baseline observational records (DEMO SEED)",
                "tide": "Mock Tidal Engine (DEMO MOCK - NOT INCOIS)",
                "elevation": "Topographic Coastal DEM Reference (DEMO DATA)",
                "risk_engine": "Phase 5 CCRI Deterministic Model",
            },
            disclaimer=(
                "DISCLAIMER & LIMITATIONS: This report was compiled by the Coastal Climate Risk Intelligence "
                "Dashboard prototype. Weights, thresholds, and calculations represent Phase 5 demo parameters "
                "and have not been scientifically validated or certified by governmental disaster management agencies. "
                "Do not use for emergency operational life-safety decisions."
            ),
            executive_summary=exec_summary,
        )

        self._generated_reports[report_id] = report
        return report

    def get_report(self, report_id: str) -> Optional[ClimateRiskReport]:
        return self._generated_reports.get(report_id)

    def list_reports(self) -> List[ClimateRiskReport]:
        return list(self._generated_reports.values())


report_service = ReportService()

