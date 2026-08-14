import json
import os
from typing import Dict, Any, List, Optional
from app.config.logging import logger
from app.database.connection import check_db_connection
from app.database.session import SessionLocal
from app.models.region import Region

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PROCESSED_REGIONS_FILE = os.path.join(BASE_DIR, "data", "processed", "regions_cleaned.json")
RAW_GEOJSON_FILE = os.path.join(BASE_DIR, "data", "gis", "coastal_regions.geojson")

class RegionService:
    """Service layer boundary for coastal region spatial & demographic data processing."""

    def _get_fallback_regions(self) -> List[Dict[str, Any]]:
        """Loads regions from processed JSON or raw GeoJSON seed file."""
        if os.path.exists(PROCESSED_REGIONS_FILE):
            try:
                with open(PROCESSED_REGIONS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error loading processed regions JSON: {e}")

        if os.path.exists(RAW_GEOJSON_FILE):
            try:
                with open(RAW_GEOJSON_FILE, "r", encoding="utf-8") as f:
                    geojson = json.load(f)
                    regions = []
                    for idx, feat in enumerate(geojson.get("features", []), start=1):
                        props = feat.get("properties", {})
                        regions.append({
                            "id": props.get("id", idx),
                            "code": props.get("code", f"REG-{idx}"),
                            "name": props.get("name"),
                            "district": props.get("district"),
                            "state": props.get("state"),
                            "country": props.get("country", "India"),
                            "latitude": props.get("latitude"),
                            "longitude": props.get("longitude"),
                            "area_sqkm": props.get("area_sqkm"),
                            "population": props.get("population"),
                            "vulnerability_tier": props.get("vulnerability_tier", "Medium"),
                            "geometry": feat.get("geometry")
                        })
                    return regions
            except Exception as e:
                logger.error(f"Error parsing raw GeoJSON: {e}")

        return []

    def get_all_regions(self) -> List[Dict[str, Any]]:
        """Retrieves list of all coastal regions."""
        if check_db_connection():
            db = SessionLocal()
            try:
                regions = db.query(Region).all()
                if regions:
                    return [r.to_dict() for r in regions]
            except Exception as e:
                logger.warning(f"DB region query failed: {e}. Switching to JSON fallback.")
            finally:
                db.close()
        
        return self._get_fallback_regions()

    def get_region_by_id(self, region_id: int) -> Optional[Dict[str, Any]]:
        """Finds a coastal region by ID."""
        regions = self.get_all_regions()
        for r in regions:
            if r.get("id") == region_id:
                return r
        return None

    def get_geojson_feature_collection(self) -> Dict[str, Any]:
        """Returns standard GeoJSON FeatureCollection for MapLibre / Leaflet visualization."""
        regions = self.get_all_regions()
        features = []
        for r in regions:
            features.append({
                "type": "Feature",
                "properties": {
                    "id": r.get("id"),
                    "code": r.get("code"),
                    "name": r.get("name"),
                    "district": r.get("district"),
                    "state": r.get("state"),
                    "vulnerability_tier": r.get("vulnerability_tier"),
                    "population": r.get("population"),
                    "area_sqkm": r.get("area_sqkm"),
                    "latitude": r.get("latitude"),
                    "longitude": r.get("longitude")
                },
                "geometry": r.get("geometry")
            })
        
        return {
            "type": "FeatureCollection",
            "name": "Coastal_Climate_Risk_Regions",
            "features": features
        }

region_service = RegionService()
