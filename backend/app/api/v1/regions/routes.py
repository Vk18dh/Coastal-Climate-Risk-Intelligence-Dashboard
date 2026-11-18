"""
Regions API endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Path

from app.schemas.region import RegionDetail, RegionSummary
from app.services.region_service import region_service

router = APIRouter()


@router.get("", response_model=List[RegionSummary], summary="List all coastal regions")
async def list_regions() -> List[RegionSummary]:
    """Retrieve all monitored coastal regions with latest environmental conditions and risk scores."""
    return region_service.list_regions()


@router.get("/{region_id}", response_model=RegionDetail, summary="Get coastal region details")
async def get_region(
    region_id: int = Path(..., description="Unique ID of the coastal region")
) -> RegionDetail:
    """Retrieve in-depth parameters, polygon boundaries, and risk scores for a single region."""
    region = region_service.get_region(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
    return region

