"""
Analytics service implementing Phase 6 Statistical Analytics.
Calculates descriptive statistics, sample standard deviation, Pearson correlation,
historical trends, and risk distributions.
"""
import math
import statistics
from typing import Dict, List, Optional

from app.repositories.analytics_repository import analytics_repo
from app.repositories.region_repository import region_repo
from app.schemas.analytics import (
    ComparisonResult,
    CorrelationResult,
    DescriptiveStats,
    Observation,
    RegionComparison,
    RiskDistributionResult,
    TimeSeriesResult,
    Trend,
)


class AnalyticsService:
    def __init__(self):
        self.repo = analytics_repo
        self.region_repo = region_repo

    def _compute_stats(self, values: List[float]) -> DescriptiveStats:
        """Compute descriptive statistics including sample standard deviation (n-1)."""
        count = len(values)
        if count == 0:
            return DescriptiveStats(
                count=0,
                min=None,
                max=None,
                mean=None,
                median=None,
                sample_stddev=None,
                trend=None,
            )

        min_val = round(min(values), 2)
        max_val = round(max(values), 2)
        mean_val = round(statistics.mean(values), 2)
        median_val = round(statistics.median(values), 2)

        # Sample standard deviation (n-1 degrees of freedom) per Phase 6 spec
        sample_stddev = None
        if count >= 2:
            sample_stddev = round(statistics.stdev(values), 2)

        # Trend (first vs last)
        first_val = values[0]
        last_val = values[-1]
        abs_change = round(last_val - first_val, 2)
        pct_change = None
        if abs(first_val) > 1e-6:
            pct_change = round((abs_change / first_val) * 100.0, 1)

        trend = Trend(
            first_value=round(first_val, 2),
            last_value=round(last_val, 2),
            absolute_change=abs_change,
            percentage_change=pct_change,
        )

        return DescriptiveStats(
            count=count,
            min=min_val,
            max=max_val,
            mean=mean_val,
            median=median_val,
            sample_stddev=sample_stddev,
            trend=trend,
        )

    def get_timeseries(
        self, region_id: int, metric: str, days: int = 30
    ) -> TimeSeriesResult:
        """Fetch timeseries observations and aggregated statistics."""
        metric_normalized = metric.lower().strip()
        data = self.repo.get_aligned_metric_series(region_id, metric_normalized, days=days)

        if not data:
            return TimeSeriesResult(
                metric=metric_normalized,
                observations=[],
                statistics=DescriptiveStats(count=0),
                provenance={metric_normalized: "unknown"},
                status="insufficient_data",
            )

        values = [item["value"] for item in data]
        stats = self._compute_stats(values)

        observations = [
            Observation(timestamp=item["timestamp"], value=item["value"])
            for item in data
        ]

        # Metric-level provenance
        prov_map = {
            "rainfall": "open-meteo (DEMO SEED)",
            "tide": "mock-tide-engine (DEMO MOCK - NOT INCOIS)",
            "risk": "climate-risk-engine (CCRI Phase 5)",
        }
        provenance = {metric_normalized: prov_map.get(metric_normalized, "coastal-risk-system")}

        return TimeSeriesResult(
            metric=metric_normalized,
            observations=observations,
            statistics=stats,
            provenance=provenance,
            status="success",
        )

    def get_correlation(
        self, region_id: int, var_x: str, var_y: str, days: int = 30
    ) -> CorrelationResult:
        """
        Calculate Pearson correlation on strictly paired observations.
        Labels: statistical association, not causation.
        """
        norm_x = var_x.lower().strip()
        norm_y = var_y.lower().strip()

        pairs = self.repo.get_paired_observations(region_id, norm_x, norm_y, days=days)
        count = len(pairs)

        prov_map = {
            "rainfall": "open-meteo (DEMO SEED)",
            "tide": "mock-tide-engine (DEMO MOCK - NOT INCOIS)",
            "risk": "climate-risk-engine (CCRI Phase 5)",
        }
        provenance = {
            norm_x: prov_map.get(norm_x, "sensor-data"),
            norm_y: prov_map.get(norm_y, "sensor-data"),
        }

        if count < 2:
            return CorrelationResult(
                variable_x=norm_x,
                variable_y=norm_y,
                correlation=None,
                paired_observation_count=count,
                provenance=provenance,
                status="insufficient_data",
            )

        xs = [p[0] for p in pairs]
        ys = [p[1] for p in pairs]

        mean_x = statistics.mean(xs)
        mean_y = statistics.mean(ys)

        cov = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
        var_x = sum((x - mean_x) ** 2 for x in xs)
        var_y = sum((y - mean_y) ** 2 for y in ys)

        if var_x < 1e-9 or var_y < 1e-9:
            correlation = 0.0
        else:
            correlation = round(cov / math.sqrt(var_x * var_y), 4)

        return CorrelationResult(
            variable_x=norm_x,
            variable_y=norm_y,
            correlation=correlation,
            paired_observation_count=count,
            provenance=provenance,
            status="success",
        )

    def get_risk_distribution(
        self, region_id: int, days: int = 30
    ) -> RiskDistributionResult:
        """Calculate historical percentage distribution of risk classifications."""
        data = self.repo.get_aligned_metric_series(region_id, "risk", days=days)
        if not data:
            return RiskDistributionResult(
                region_id=region_id,
                distribution={},
                count=0,
                provenance={"risk": "climate-risk-engine"},
                status="insufficient_data",
            )

        counts = {"Low": 0, "Moderate": 0, "High": 0, "Critical": 0}
        total = len(data)

        for item in data:
            score = item["value"]
            if score >= 75.0:
                counts["Critical"] += 1
            elif score >= 50.0:
                counts["High"] += 1
            elif score >= 25.0:
                counts["Moderate"] += 1
            else:
                counts["Low"] += 1

        dist = {
            level: round((c / total) * 100.0, 1)
            for level, c in counts.items()
        }

        return RiskDistributionResult(
            region_id=region_id,
            distribution=dist,
            count=total,
            provenance={"risk": "climate-risk-engine (CCRI Phase 5)"},
            status="success",
        )

    def get_comparison(self, metric: str, days: int = 30) -> ComparisonResult:
        """Compare a metric across all coastal regions."""
        norm_metric = metric.lower().strip()
        all_regions = self.region_repo.get_all_regions_data()
        comparisons = []

        for reg in all_regions:
            reg_id = reg["id"]
            data = self.repo.get_aligned_metric_series(reg_id, norm_metric, days=days)
            values = [d["value"] for d in data]
            stats = self._compute_stats(values)

            prov_map = {
                "rainfall": "open-meteo (DEMO SEED)",
                "tide": "mock-tide-engine (DEMO MOCK - NOT INCOIS)",
                "risk": "climate-risk-engine (CCRI Phase 5)",
            }
            provenance = {norm_metric: prov_map.get(norm_metric, "coastal-system")}

            comparisons.append(
                RegionComparison(
                    region_id=reg_id,
                    statistics=stats,
                    provenance=provenance,
                )
            )

        return ComparisonResult(
            metric=norm_metric,
            regions=comparisons,
            status="success" if comparisons else "insufficient_data",
        )


analytics_service = AnalyticsService()

