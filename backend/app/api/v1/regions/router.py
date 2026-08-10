from fastapi import APIRouter

router = APIRouter(prefix="/regions", tags=["Regions"])


@router.get("")
async def get_regions_data():
    """
    GET /api/v1/regions
    Returns coastal administrative region boundaries and geospatial polygons.
    (Structural route boundary - PostGIS spatial queries deferred to Sprint 2)
    """
    return {
        "success": True,
        "message": "Regions API endpoint registered. Regional PostGIS spatial query module prepared.",
        "data": {
            "status": "route_registered",
            "module": "app.services.region_service"
        }
    }
