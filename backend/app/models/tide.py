"""
TideData model — ocean / tide observations.

Table: tide_data

Documents: BACKEND.md §Database Tables > tide_data
ERD: REGIONS ||--o{ TIDE_DATA : contains

Schema decision:
    Same as WeatherData — BACKEND.md omits region_id from the field list
    but the ERD requires the relationship. Added: region_id FK.
"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.region import Region


class TideData(Base):
    """
    A single tide / ocean observation record.

    Fields match BACKEND.md exactly plus the required region_id FK.
    All measurement columns are nullable to accommodate partial
    observations from different sources (INCOIS).
    """

    __tablename__ = "tide_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # FK to regions (required by ERD relationship)
    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Observation timestamp  (BACKEND.md: timestamp)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    
    # Data source provider (e.g. incois-mock)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, server_default='unknown')

    # ── Measurement fields (BACKEND.md) ───────────────────────────────────────
    tide_height: Mapped[float | None] = mapped_column(Float, nullable=True)             # m
    wave_height: Mapped[float | None] = mapped_column(Float, nullable=True)             # m
    sea_surface_temperature: Mapped[float | None] = mapped_column(Float, nullable=True) # °C

    # ── Relationships ──────────────────────────────────────────────────────────
    region: Mapped["Region"] = relationship("Region", back_populates="tide_data")

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_tide_data_region_timestamp", "region_id", "timestamp", unique=True),
    )

    def __repr__(self) -> str:
        return (
            f"<TideData id={self.id} region_id={self.region_id} "
            f"timestamp={self.timestamp!r}>"
        )
