import pytest
from datetime import datetime, timezone
import os

from app.config.engine import RiskEngineConfig
from app.services.risk_engine import ClimateRiskEngine
from app.repositories.risk import RiskRepository
from app.models.region import Region
from app.models.risk import RiskScore

@pytest.fixture
def engine():
    return ClimateRiskEngine()

@pytest.fixture
def default_time():
    return datetime.now(timezone.utc)


def test_normalization_bounds(engine):
    # Rainfall
    assert engine._normalize_rainfall(-10.0) == 0.0
    assert engine._normalize_rainfall(0.0) == 0.0
    assert engine._normalize_rainfall(100.0) == 0.5
    assert engine._normalize_rainfall(200.0) == 1.0
    assert engine._normalize_rainfall(500.0) == 1.0

    # Tide
    assert engine._normalize_tide(-1.0) == 0.0
    assert engine._normalize_tide(0.0) == 0.0
    assert engine._normalize_tide(1.5) == 0.5
    assert engine._normalize_tide(3.0) == 1.0
    assert engine._normalize_tide(5.0) == 1.0

    # Elevation (Inverted)
    assert engine._normalize_elevation(-5.0) == 1.0
    assert engine._normalize_elevation(0.0) == 1.0
    assert engine._normalize_elevation(10.0) == 0.5
    assert engine._normalize_elevation(20.0) == 0.0
    assert engine._normalize_elevation(100.0) == 0.0

    # Flood
    assert engine._normalize_flood("none") == 0.0
    assert engine._normalize_flood("low") == 0.25
    assert engine._normalize_flood("extreme") == 1.0
    assert engine._normalize_flood("INVALID") == 0.0


def test_deterministic_full_calculation(engine, default_time):
    # Perfect storm: Max rainfall, Max tide, Min elevation, Extreme flood
    result = engine.calculate(
        region_id=1,
        timestamp=default_time,
        rainfall_mm=200.0,
        tide_m=3.0,
        elevation_m=0.0,
        flood_severity="extreme"
    )
    
    assert result.status == "success"
    assert result.data_completeness == 1.0
    assert not result.missing_components
    assert result.final_score == pytest.approx(100.0)
    assert result.risk_level == "Critical"
    
    # Mild conditions: No rain, no tide, high elevation, no flood
    result2 = engine.calculate(
        region_id=1,
        timestamp=default_time,
        rainfall_mm=0.0,
        tide_m=0.0,
        elevation_m=20.0,
        flood_severity="none"
    )
    assert result2.final_score == pytest.approx(0.0)
    assert result2.risk_level == "Low"


def test_renormalize_missing_data(engine, default_time, monkeypatch):
    monkeypatch.setattr(RiskEngineConfig, "MISSING_DATA_MODE", "RENORMALIZE")
    
    # Missing rainfall and flood. Only tide (0.3 weight) and elevation (0.2 weight) available.
    # Total available weight = 0.5
    # Max tide (score 1.0), Max risk elevation (score 1.0)
    # Effective weights should be 0.6 for tide and 0.4 for elevation.
    result = engine.calculate(
        region_id=1,
        timestamp=default_time,
        rainfall_mm=None,
        tide_m=3.0,
        elevation_m=0.0,
        flood_severity=None
    )
    
    assert result.status == "success"
    assert result.data_completeness == 0.5
    assert "rainfall_score" in result.missing_components
    assert "flood_score" in result.missing_components
    
    assert result.effective_weights["tide_score"] == pytest.approx(0.6)
    assert result.effective_weights["elevation_score"] == pytest.approx(0.4)
    assert result.effective_weights["rainfall_score"] == 0.0
    
    # Final score should still be 100 since available metrics are maxed out
    assert result.final_score == pytest.approx(100.0)
    assert len(result.warnings) > 0


def test_strict_missing_data(engine, default_time, monkeypatch):
    monkeypatch.setattr(RiskEngineConfig, "MISSING_DATA_MODE", "STRICT")
    
    result = engine.calculate(
        region_id=1,
        timestamp=default_time,
        rainfall_mm=100.0,
        tide_m=None, # Missing
        elevation_m=10.0,
        flood_severity="moderate"
    )
    
    assert result.status == "insufficient_data"
    assert result.final_score is None
    assert result.risk_level is None
    assert "tide_score" in result.missing_components


@pytest.mark.asyncio
async def test_persistence_upsert(db_session, engine, default_time):
    # 1. Setup a test region
    region = Region(name="Test Region", district="Test District", geometry="MULTIPOLYGON(((0 0, 1 0, 1 1, 0 1, 0 0)))")
    db_session.add(region)
    await db_session.commit()
    
    # 2. Calculate score
    result = engine.calculate(
        region_id=region.id,
        timestamp=default_time,
        rainfall_mm=100.0,
        tide_m=1.5,
        elevation_m=10.0,
        flood_severity="moderate"
    )
    
    # 3. Upsert
    repo = RiskRepository()
    db_record = await repo.upsert_score(db_session, result)
    
    assert db_record.id is not None
    assert db_record.region_id == region.id
    assert db_record.final_score == pytest.approx(50.0)
    assert db_record.risk_level == "Moderate"
    
    # 4. Verify idempotent upsert
    result2 = engine.calculate(
        region_id=region.id,
        timestamp=default_time,
        rainfall_mm=200.0, # changed
        tide_m=3.0,
        elevation_m=0.0,
        flood_severity="extreme"
    )
    db_record_updated = await repo.upsert_score(db_session, result2)
    await db_session.refresh(db_record_updated)
    
    assert db_record_updated.id == db_record.id # Same row
    assert db_record_updated.final_score == pytest.approx(100.0)
    assert db_record_updated.risk_level == "Critical"
