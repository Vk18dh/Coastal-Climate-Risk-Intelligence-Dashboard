"""
AIReport model — AI-generated executive reports and advisory content.

Table: ai_reports

Documents: BACKEND.md §Database Tables > ai_reports
ERD: REGIONS ||--o{ AI_REPORTS : generates

This model stores the OUTPUT of the AI Service (Phase 9 — Qwen 3 Instruct).
It does NOT contain any AI invocation logic — that belongs to app/ai/.
"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.region import Region


class AIReport(Base):
    """
    Stores an AI-generated climate advisory report for a region.

    Fields match BACKEND.md ai_reports table exactly.
    The 'recommendations' column uses Text (not JSON) to store free-form
    AI-generated text. Phase 9 may migrate this to JSONB if structured
    recommendations are needed.
    """

    __tablename__ = "ai_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # When the report was generated  (BACKEND.md: timestamp)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    # ── AI output fields (BACKEND.md) ─────────────────────────────────────────
    # Free-text executive summary produced by Qwen 3 Instruct
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Free-text recommendations produced by Qwen 3 Instruct
    recommendations: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Model confidence / certainty score  (BACKEND.md: confidence)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    # ── Optional metadata not in BACKEND.md but needed for traceability ────────
    # Model name used to generate the report (e.g. "qwen3:8b-instruct-q4_K_M")
    model_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    region: Mapped["Region"] = relationship("Region", back_populates="ai_reports")

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_ai_reports_region_timestamp", "region_id", "timestamp"),
    )

    def __repr__(self) -> str:
        return (
            f"<AIReport id={self.id} region_id={self.region_id} "
            f"timestamp={self.timestamp!r}>"
        )
