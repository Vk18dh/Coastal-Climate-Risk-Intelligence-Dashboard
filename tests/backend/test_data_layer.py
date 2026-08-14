import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "backend"))

from app.services.region_service import region_service
from app.services.weather_service import weather_service
from app.services.tide_service import tide_service
from app.services.risk_service import risk_service
from app.services.analytics_service import analytics_service
from app.services.ai_service import ai_service
from app.services.report_service import report_service

def test_regions_dataset():
    """Verify all 13 coastal regions across all 10 coastal states are loaded."""
    regions = region_service.get_all_regions()
    assert len(regions) == 13
    
    states = set(r["state"] for r in regions)
    assert "Karnataka" in states
    assert "Maharashtra" in states
    assert "Gujarat" in states
    assert "Tamil Nadu" in states
    assert "Kerala" in states
    assert "Andhra Pradesh" in states
    assert "Odisha" in states
    assert "West Bengal" in states
    assert "Goa" in states
    assert "Puducherry" in states

def test_geojson_feature_collection():
    """Verify GeoJSON FeatureCollection generation."""
    geojson = region_service.get_geojson_feature_collection()
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) == 13
    
    first_feat = geojson["features"][0]
    assert first_feat["type"] == "Feature"
    assert "geometry" in first_feat
    assert first_feat["geometry"]["type"] == "Polygon"

def test_karnataka_regions():
    """Verify Karnataka specific coastal regions."""
    karnataka_regions = [r for r in region_service.get_all_regions() if r["state"] == "Karnataka"]
    assert len(karnataka_regions) == 3
    
    codes = [r["code"] for r in karnataka_regions]
    assert "MNG-P" in codes # Mangaluru
    assert "UDP-M" in codes # Udupi
    assert "KRW-U" in codes # Karwar

def test_weather_service():
    """Verify weather service returns valid meteorological data."""
    weather = weather_service.get_weather_for_region(7) # Mangaluru
    assert "temperature_c" in weather
    assert "rainfall_mm" in weather
    assert "humidity_pct" in weather
    assert "wind_speed_kmh" in weather
    assert "pressure_hpa" in weather
    assert "condition" in weather

def test_tide_service():
    """Verify tide service returns valid oceanographic metrics."""
    tide = tide_service.get_tides_for_region(7) # Mangaluru
    assert "tide_height_m" in tide
    assert "wave_height_m" in tide
    assert tide["tide_height_m"] > 0.0

def test_risk_engine():
    """Verify Composite Climate Risk Index calculation."""
    risk = risk_service.compute_risk_for_region(7) # Mangaluru
    assert "composite_risk_score" in risk
    assert "risk_level" in risk
    assert risk["risk_level"] in ["Low", "Moderate", "High", "Critical"]
    assert 0.0 <= risk["composite_risk_score"] <= 100.0

def test_analytics_summary():
    """Verify statistical analytics summary."""
    summary = analytics_service.get_analytics_summary()
    assert "overview" in summary
    assert summary["overview"]["total_monitored_regions"] == 13
    assert summary["overview"]["total_historical_events"] >= 9

def test_ai_advisory():
    """Verify AI Executive Summary & Climate Advisory generation."""
    report = ai_service.generate_ai_report(7)
    assert "ai_executive_summary" in report
    assert "risk_level" in report
    assert "confidence_score" in report

def test_full_report_generation():
    """Verify full downloadable report generation."""
    report = report_service.generate_full_report(7)
    assert "report_id" in report
    assert "region" in report
    assert "weather" in report
    assert "tides" in report
    assert "risk_assessment" in report
    assert "ai_executive_advisory" in report
