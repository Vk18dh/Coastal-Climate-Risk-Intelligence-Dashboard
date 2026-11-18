"""
Dashboard service — aggregates KPI cards and today's situation summary.
"""
from datetime import datetime, timezone
from typing import List

from app.schemas.dashboard import (
    DashboardKPIs,
    DashboardOverviewResponse,
    KPICard,
    TodaySituation,
)
from app.services.region_service import region_service


class DashboardService:
    def __init__(self):
        self.region_service = region_service

    def get_overview(self) -> DashboardOverviewResponse:
        regions = self.region_service.list_regions()
        now = datetime.now(timezone.utc)

        # Aggregate stats
        scores = [r.latest_risk.final_score for r in regions if r.latest_risk and r.latest_risk.final_score is not None]
        rainfalls = [r.latest_rainfall_mm for r in regions if r.latest_rainfall_mm is not None]
        tides = [r.latest_tide_m for r in regions if r.latest_tide_m is not None]

        avg_score = sum(scores) / len(scores) if scores else 0.0
        avg_rain = sum(rainfalls) / len(rainfalls) if rainfalls else 0.0
        avg_tide = sum(tides) / len(tides) if tides else 0.0

        high_risk_count = sum(
            1 for r in regions if r.latest_risk and r.latest_risk.risk_level in ("High", "Critical")
        )
        active_alerts_count = sum(
            1 for r in regions if r.latest_risk and (r.latest_risk.final_score or 0.0) >= 50.0
        )

        # Classify overall score
        if avg_score >= 75.0:
            overall_class = "Critical"
            overall_status = "critical"
        elif avg_score >= 50.0:
            overall_class = "High"
            overall_status = "warning"
        elif avg_score >= 25.0:
            overall_class = "Moderate"
            overall_status = "warning"
        else:
            overall_class = "Low"
            overall_status = "normal"

        kpis = DashboardKPIs(
            overall_risk_score=KPICard(
                title="Overall Climate Risk",
                value=f"{avg_score:.1f}",
                numeric_value=round(avg_score, 1),
                unit="CCRI",
                status=overall_status,
                subtext=f"{overall_class} Risk across {len(regions)} coastal zones",
                icon="ShieldAlert",
            ),
            high_risk_regions=KPICard(
                title="Elevated Risk Zones",
                value=str(high_risk_count),
                numeric_value=float(high_risk_count),
                unit="regions",
                status="critical" if high_risk_count > 0 else "normal",
                subtext=f"{high_risk_count} of {len(regions)} require active monitoring",
                icon="AlertTriangle",
            ),
            active_alerts=KPICard(
                title="Active Risk Alerts",
                value=str(active_alerts_count),
                numeric_value=float(active_alerts_count),
                unit="active",
                status="warning" if active_alerts_count > 0 else "normal",
                subtext="Tidal surge & precipitation thresholds exceeded",
                icon="BellRing",
            ),
            average_rainfall=KPICard(
                title="Mean Precipitation",
                value=f"{avg_rain:.1f}",
                numeric_value=round(avg_rain, 1),
                unit="mm/24h",
                status="warning" if avg_rain > 60 else "normal",
                subtext="Open-Meteo observational baseline",
                icon="CloudRain",
            ),
            average_tide=KPICard(
                title="Mean Tidal Height",
                value=f"{avg_tide:.2f}",
                numeric_value=round(avg_tide, 2),
                unit="meters",
                status="warning" if avg_tide > 2.0 else "normal",
                subtext="Mock tidal hydrodynamic model",
                icon="Waves",
            ),
            timestamp=now,
        )

        today_situation = TodaySituation(
            timestamp=now,
            overall_classification=overall_class,
            overall_score=round(avg_score, 1),
            headline=f"Coastal Risk Level: {overall_class} ({avg_score:.1f} CCRI)",
            summary_text=(
                f"Currently monitoring 5 major coastal regions across India. "
                f"{high_risk_count} region(s) exhibit elevated vulnerability due to high spring tide "
                f"fluctuations coupled with low estuarine elevations."
            ),
            main_contributors=[
                "High tidal surge in deltaic and low-lying coastal zones (Sundarbans & Kochi)",
                "Severe elevation vulnerability in estuarine backwaters (< 3m above sea level)",
                "Precipitation runoff and drainage saturation in coastal urban clusters",
            ],
            active_alerts_count=active_alerts_count,
            data_freshness="Current Demo Baseline (Refreshed hourly)",
            provenance={
                "weather": "Open-Meteo baseline patterns (DEMO SEED)",
                "tide": "Mock Tidal Engine (DEMO MOCK - NOT INCOIS)",
                "risk_engine": "CCRI Phase 5 Deterministic Engine",
            },
        )

        return DashboardOverviewResponse(
            kpis=kpis,
            today_situation=today_situation,
            regions=regions,
        )


dashboard_service = DashboardService()

