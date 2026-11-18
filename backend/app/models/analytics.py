"""
AnalyticsResult model — stored outputs of the Analytics Engine.

Table: analytics_results

Documents: BACKEND.md §Analytics Module (responsibilities: trend analysis,
           correlation analysis, historical analytics)

Schema decision:
    BACKEND.md describes the Analytics Module's responsibilities but does
    NOT specify an analytics_results table or its fields. Phase 3 scope
    requires this model. The schema below is strictly derived from the
    documented module responsibilities — no domain logic is added.

    Fields chosen:
      - region_id        — FK anchor (all analytics is per-region)
      - computed_at      — when the analytics run completed
      - analysis_type    — discriminator: "trend", "correlation", "historical"
      - period_start     — start of the time window analysed
      - period_end       — end of the time window analysed
      - result_json      — JSONB output from the Analytics Engine
                           (structured differently per analysis_type;
                           schema defined in Phase 6)

    JSONB is used instead of individual columns because analytics outputs
    vary in structure depending on analysis_type and would otherwise require
    either: (a) many nullable columns or (b) separate tables per type.
    JSONB is the standard PostgreSQL approach for heterogeneous analytics results.
"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.region import Region

# ── Valid analysis_type values (informational — enforced at service layer) ────
ANALYSIS_TYPES = frozenset({"trend", "correlation", "historical"})


class AnalyticsResult(Base):
    """
    Stored output of a completed analytics computation for a region.

    Table: analytics_results

    This model stores the serialised result of the Analytics Engine.
    The Analytics Engine itself (computation logic) is implemented in Phase 6.
    """

    __tablename__ = "analytics_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # When the analytics computation completed
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    # Discriminator — one of ANALYSIS_TYPES
    analysis_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )

    # Time window of the data analysed
    period_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Serialised analytics output — schema defined in Phase 6
    result_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Optional human-readable summary (for API responses without deserialising JSON)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    region: Mapped["Region"] = relationship(
        "Region", back_populates="analytics_results"
    )

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index(
            "ix_analytics_results_region_type_computed",
            "region_id",
            "analysis_type",
            "computed_at",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<AnalyticsResult id={self.id} region_id={self.region_id} "
            f"type={self.analysis_type!r} computed_at={self.computed_at!r}>"
        )
