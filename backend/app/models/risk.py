"""
RiskScore, ElevationData, and HistoricalFlood models.

Tables: risk_scores, elevation_data, historical_floods

Documents: BACKEND.md §Database Tables

RiskScore is the primary output of the Climate Risk Engine (Phase 5).
ElevationData and HistoricalFlood are referenced as FK targets by risk_scores
(elevation_score, flood_score) and must exist in the database schema.

[DEMO ONLY - NOT SCIENTIFICALLY VALIDATED]
The score field names (rainfall_score, tide_score, elevation_score, flood_score)
match the BACKEND.md schema exactly. The weights and computation that produce
these values are deferred to Phase 5 and are not present in this model.
"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.region import Region


# ── ElevationData ─────────────────────────────────────────────────────────────

class ElevationData(Base):
    """
    Terrain elevation information for a region.

    Table: elevation_data
    Documents: BACKEND.md §elevation_data
    ERD: REGIONS ||--o{ ELEVATION_DATA : contains
    """

    __tablename__ = "elevation_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # BACKEND.md: elevation, slope
    elevation: Mapped[float | None] = mapped_column(Float, nullable=True)  # metres
    slope: Mapped[float | None] = mapped_column(Float, nullable=True)      # degrees

    # ── Relationships ──────────────────────────────────────────────────────────
    region: Mapped["Region"] = relationship(
        "Region", back_populates="elevation_data"
    )

    def __repr__(self) -> str:
        return f"<ElevationData id={self.id} region_id={self.region_id}>"


# ── HistoricalFlood ───────────────────────────────────────────────────────────

class HistoricalFlood(Base):
    """
    Historical flood event for a region.

    Table: historical_floods
    Documents: BACKEND.md §historical_floods
    ERD: REGIONS ||--o{ HISTORICAL_FLOODS : contains
    """

    __tablename__ = "historical_floods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # BACKEND.md: year, severity
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    severity: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g. "low", "moderate", "high", "extreme"

    # ── Relationships ──────────────────────────────────────────────────────────
    region: Mapped["Region"] = relationship(
        "Region", back_populates="historical_floods"
    )

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_historical_floods_region_year", "region_id", "year"),
    )

    def __repr__(self) -> str:
        return (
            f"<HistoricalFlood id={self.id} region_id={self.region_id} "
            f"year={self.year} severity={self.severity!r}>"
        )


# ── RiskScore ─────────────────────────────────────────────────────────────────

class RiskScore(Base):
    """
    Climate risk assessment result for a region at a point in time.

    Table: risk_scores
    Documents: BACKEND.md §risk_scores
    ERD: REGIONS ||--o{ RISK_SCORES : generates

    This is the OUTPUT of the Climate Risk Engine (Phase 5).
    Score fields are populated by the engine — this model defines only
    the storage schema, not the computation logic.

    [DEMO ONLY - NOT SCIENTIFICALLY VALIDATED]
    Individual score fields (rainfall_score, tide_score, etc.) represent
    normalised component scores. The weights applied by the risk engine
    are configured in Phase 5 and are explicitly labelled as demo values.
    """

    __tablename__ = "risk_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # When the risk assessment was computed  (BACKEND.md: timestamp)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    # ── Component scores (BACKEND.md) — range 0.0–1.0 ────────────────────────
    rainfall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    tide_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    elevation_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    flood_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # ── Composite result (BACKEND.md) — range 0.0–100.0 ─────────────────────
    final_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Risk classification label  (BACKEND.md: risk_level)
    # e.g. "Low", "Moderate", "High", "Critical"
    risk_level: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    region: Mapped["Region"] = relationship(
        "Region", back_populates="risk_scores"
    )

    # ── Indexes & Constraints ──────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_risk_scores_region_timestamp", "region_id", "timestamp", unique=True),
        CheckConstraint(
            "final_score IS NULL OR (final_score >= 0.0 AND final_score <= 100.0)",
            name="ck_risk_scores_final_score_range",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<RiskScore id={self.id} region_id={self.region_id} "
            f"final_score={self.final_score} risk_level={self.risk_level!r}>"
        )
