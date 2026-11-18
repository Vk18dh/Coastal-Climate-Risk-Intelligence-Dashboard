"""
Database seeding — sample data infrastructure.

PURPOSE: This module provides the seeding framework for development/testing.
         It does NOT contain real climate data or production datasets.

SCOPE (Phase 3):
  - Creates the seed() entry point
  - Creates one sample Region record (no real geographic boundary)
  - Sample geometry is a placeholder WKT box — NOT real coastal data.

STRICTLY NOT:
  - Real weather API data
  - Real tide data
  - Climate risk calculations
  - Real geographic boundaries
  - Any external data integration

Real data ingestion is Phase 4.

Usage:
    python -c "import asyncio; from app.database.seed import seed; asyncio.run(seed())"
"""
import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.region import Region

logger = logging.getLogger(__name__)

# ── Sample data constants ─────────────────────────────────────────────────────
# [DEMO ONLY - NOT REAL GEOGRAPHIC DATA]
# A simple WKT bounding box used only to verify PostGIS geometry storage.
# Real region boundaries are loaded in Phase 4 via GIS data ingestion.
_SAMPLE_GEOMETRY_WKT = (
    "MULTIPOLYGON(((80.0 13.0, 80.5 13.0, 80.5 13.5, 80.0 13.5, 80.0 13.0)))"
)

_SAMPLE_REGIONS = [
    {
        "name": "Sample Coastal Zone A",
        "district": "Demo District",
        "description": (
            "[DEMO ONLY] Placeholder region for development and testing. "
            "Geometry is a bounding box, not a real administrative boundary."
        ),
        "geometry_wkt": _SAMPLE_GEOMETRY_WKT,
    },
]


async def seed() -> None:
    """
    Populate the database with minimum sample data for development.

    Idempotent — skips insertion if sample records already exist.
    """
    logger.info("Starting database seed...")

    async for session in get_db():
        await _seed_regions(session)

    logger.info("Database seed complete.")


async def _seed_regions(session: AsyncSession) -> None:
    """Insert sample Region records if not already present."""
    for data in _SAMPLE_REGIONS:
        # Check for existing record by name
        existing = await session.execute(
            text("SELECT id FROM regions WHERE name = :name LIMIT 1"),
            {"name": data["name"]},
        )
        if existing.fetchone() is not None:
            logger.info("Region %r already exists, skipping.", data["name"])
            continue

        # Insert with PostGIS geometry via ST_GeomFromText
        await session.execute(
            text(
                """
                INSERT INTO regions (name, district, description, geometry)
                VALUES (
                    :name,
                    :district,
                    :description,
                    ST_GeomFromText(:wkt, 4326)
                )
                """
            ),
            {
                "name": data["name"],
                "district": data["district"],
                "description": data["description"],
                "wkt": data["geometry_wkt"],
            },
        )
        await session.commit()
        logger.info("Inserted sample region: %r", data["name"])
