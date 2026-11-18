"""
Region model — coastal administrative boundaries.

Table: regions

Documents: BACKEND.md §Database Tables > regions
ERD: BACKEND.md — REGIONS is the parent of all environmental data tables.
"""
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.analytics import AnalyticsResult
    from app.models.risk import ElevationData, HistoricalFlood, RiskScore
    from app.models.tide import TideData
    from app.models.weather import WeatherData
    from app.models.report import AIReport


class Region(Base):
    """
    Coastal region / administrative boundary.

    Acts as the geographic anchor for all environmental data.
    Every WeatherData, TideData, RiskScore, and AIReport row
    is associated with a Region.

    Geometry:
        MULTIPOLYGON EPSG:4326 — chosen over POLYGON to support
        non-contiguous coastal zones (e.g. islands, estuaries).
        BACKEND.md specifies 'Polygon'; MULTIPOLYGON is a strict superset.
    """

    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Human-readable name  (BACKEND.md: name)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # Administrative district  (BACKEND.md: district)
    district: Mapped[str] = mapped_column(String(255), nullable=False)

    # Optional free-text description — not in BACKEND.md but required for UI
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # PostGIS geometry — MULTIPOLYGON, WGS-84 (BACKEND.md: geometry Polygon)
    geometry: Mapped[object] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326),
        nullable=True,  # Nullable during seeding before geometry is loaded
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    weather_data: Mapped[list["WeatherData"]] = relationship(
        "WeatherData", back_populates="region", cascade="all, delete-orphan"
    )
    tide_data: Mapped[list["TideData"]] = relationship(
        "TideData", back_populates="region", cascade="all, delete-orphan"
    )
    elevation_data: Mapped[list["ElevationData"]] = relationship(
        "ElevationData", back_populates="region", cascade="all, delete-orphan"
    )
    historical_floods: Mapped[list["HistoricalFlood"]] = relationship(
        "HistoricalFlood", back_populates="region", cascade="all, delete-orphan"
    )
    risk_scores: Mapped[list["RiskScore"]] = relationship(
        "RiskScore", back_populates="region", cascade="all, delete-orphan"
    )
    ai_reports: Mapped[list["AIReport"]] = relationship(
        "AIReport", back_populates="region", cascade="all, delete-orphan"
    )
    analytics_results: Mapped[list["AnalyticsResult"]] = relationship(
        "AnalyticsResult", back_populates="region", cascade="all, delete-orphan"
    )

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_regions_name_district", "name", "district"),
    )

    def __repr__(self) -> str:
        return f"<Region id={self.id} name={self.name!r} district={self.district!r}>"
