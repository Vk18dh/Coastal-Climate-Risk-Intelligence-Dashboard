"""
WeatherData model — surface weather observations.

Table: weather_data

Documents: BACKEND.md §Database Tables > weather_data
ERD: REGIONS ||--o{ WEATHER_DATA : contains

Schema decision:
    BACKEND.md lists no region_id for weather_data, but the ERD
    explicitly shows REGIONS contains WEATHER_DATA. A foreign key
    to regions.id is required for the relationship to be meaningful.
    Added: region_id FK.
"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.region import Region


class WeatherData(Base):
    """
    A single weather observation record.

    Fields match BACKEND.md exactly plus the required region_id FK.
    All measurement columns are nullable to accommodate partial observations
    from different data sources (IMD, Open-Meteo).
    """

    __tablename__ = "weather_data"

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
    
    # Data source provider (e.g. open-meteo, mock)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, server_default='unknown')

    # ── Measurement fields (BACKEND.md) ───────────────────────────────────────
    rainfall: Mapped[float | None] = mapped_column(Float, nullable=True)       # mm
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)    # °C
    humidity: Mapped[float | None] = mapped_column(Float, nullable=True)       # %
    wind_speed: Mapped[float | None] = mapped_column(Float, nullable=True)     # km/h
    pressure: Mapped[float | None] = mapped_column(Float, nullable=True)       # hPa

    # ── Relationships ──────────────────────────────────────────────────────────
    region: Mapped["Region"] = relationship("Region", back_populates="weather_data")

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_weather_data_region_timestamp", "region_id", "timestamp", unique=True),
    )

    def __repr__(self) -> str:
        return (
            f"<WeatherData id={self.id} region_id={self.region_id} "
            f"timestamp={self.timestamp!r}>"
        )
