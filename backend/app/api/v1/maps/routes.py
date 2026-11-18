"""
GIS & Maps API endpoints.
"""
from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Path

from app.services.region_service import region_service

router = APIRouter()


@router.get("/geojson", summary="Get GeoJSON FeatureCollection of coastal risk zones")
async def get_coastal_geojson() -> Dict[str, Any]:
    """
    Returns valid GeoJSON FeatureCollection containing all monitored coastal regions,
    their boundary polygons, current CCRI scores, and risk classifications for GIS map rendering.
    """
    return region_service.get_geojson()


@router.get("/regions/{region_id}/polygon", summary="Get single region GeoJSON boundary")
async def get_region_polygon(
    region_id: int = Path(..., description="Region ID")
) -> Dict[str, Any]:
    """Retrieve GeoJSON polygon and properties for a specific coastal region."""
    region = region_service.get_region(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
    return {
        "type": "Feature",
        "id": region.id,
        "properties": {
            "name": region.name,
            "district": region.district,
            "risk_score": region.latest_risk.final_score if region.latest_risk else 0.0,
            "risk_level": region.latest_risk.risk_level if region.latest_risk else "Low",
        },
        "geometry": region.geojson_polygon,
    }

