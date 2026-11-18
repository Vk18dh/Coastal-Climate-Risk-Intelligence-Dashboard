"""
Region service layer.
"""
from typing import Any, Dict, List, Optional

from app.repositories.region_repository import region_repo
from app.schemas.region import RegionDetail, RegionSummary


class RegionService:
    def __init__(self):
        self.repo = region_repo

    def list_regions(self) -> List[RegionSummary]:
        data = self.repo.get_all_regions_data()
        return [RegionSummary(**item) for item in data]

    def get_region(self, region_id: int) -> Optional[RegionDetail]:
        data = self.repo.get_region_by_id(region_id)
        if not data:
            return None
        return RegionDetail(**data)

    def get_geojson(self) -> Dict[str, Any]:
        return self.repo.get_geojson_feature_collection()


region_service = RegionService()

