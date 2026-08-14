from fastapi import APIRouter, HTTPException, Query
from app.services.region_service import region_service

router = APIRouter(prefix="/regions", tags=["Regions"])


@router.get("")
async def get_regions():
    """
    GET /api/v1/regions
    Returns list of all coastal administrative regions.
    """
    regions = region_service.get_all_regions()
    return {
        "success": True,
        "message": f"Successfully retrieved {len(regions)} coastal regions.",
        "data": regions
    }


@router.get("/geojson")
async def get_regions_geojson():
    """
    GET /api/v1/regions/geojson
    Returns GeoJSON FeatureCollection for MapLibre GL / Leaflet map layer rendering.
    """
    feature_collection = region_service.get_geojson_feature_collection()
    return {
        "success": True,
        "message": "Successfully generated GIS GeoJSON FeatureCollection.",
        "data": feature_collection
    }


@router.get("/{region_id}")
async def get_region_by_id(region_id: int):
    """
    GET /api/v1/regions/{region_id}
    Returns detailed spatial and demographic metrics for a specific region.
    """
    region = region_service.get_region_by_id(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=f"Coastal region with ID {region_id} not found.")
    return {
        "success": True,
        "message": "Region details retrieved successfully.",
        "data": region
    }
