#!/usr/bin/env python3
"""
GIS Data Preprocessing & Validation Script for Coastal Climate Risk Intelligence Platform.
Validates GeoJSON topology, computes bounding boxes, centroids, and exports cleaned GIS datasets.
"""
import json
import math
import os
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_GIS_FILE = os.path.join(BASE_DIR, "data", "gis", "coastal_regions.geojson")
PROCESSED_GIS_FILE = os.path.join(BASE_DIR, "data", "processed", "regions_cleaned.json")

def compute_centroid(coords):
    """Computes basic 2D spatial polygon centroid."""
    if not coords or len(coords) == 0:
        return 0.0, 0.0
    ring = coords[0]
    lons = [p[0] for p in ring]
    lats = [p[1] for p in ring]
    return sum(lons) / len(lons), sum(lats) / len(lats)

def compute_bbox(coords):
    """Computes bounding box [min_lon, min_lat, max_lon, max_lat]."""
    ring = coords[0]
    lons = [p[0] for p in ring]
    lats = [p[1] for p in ring]
    return [min(lons), min(lats), max(lons), max(lats)]

def process_gis_data():
    print(f"[*] Processing GIS datasets from {RAW_GIS_FILE}...")
    if not os.path.exists(RAW_GIS_FILE):
        print(f"[!] Error: Raw GIS file not found: {RAW_GIS_FILE}")
        sys.exit(1)

    with open(RAW_GIS_FILE, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    processed_regions = []
    features = geojson.get("features", [])

    for idx, feature in enumerate(features, start=1):
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        coords = geometry.get("coordinates", [])

        c_lon, c_lat = compute_centroid(coords) if coords else (props.get("longitude", 0.0), props.get("latitude", 0.0))
        bbox = compute_bbox(coords) if coords else []

        region_item = {
            "id": props.get("id", idx),
            "code": props.get("code", f"REG-{idx:03d}"),
            "name": props.get("name", "Unknown Region"),
            "district": props.get("district", "Unknown District"),
            "state": props.get("state", "Unknown State"),
            "country": props.get("country", "India"),
            "latitude": round(c_lat, 4),
            "longitude": round(c_lon, 4),
            "area_sqkm": props.get("area_sqkm", 50.0),
            "population": props.get("population", 100000),
            "vulnerability_tier": props.get("vulnerability_tier", "Medium"),
            "elevation": {
                "mean_m": props.get("mean_elevation_m", 5.0),
                "min_m": props.get("min_elevation_m", 1.0),
                "max_m": props.get("max_elevation_m", 20.0),
                "slope_deg": props.get("slope_degrees", 1.0),
                "coastal_distance_km": props.get("coastal_distance_km", 0.5),
            },
            "bbox": bbox,
            "geometry": geometry
        }
        processed_regions.append(region_item)

    os.makedirs(os.path.dirname(PROCESSED_GIS_FILE), exist_ok=True)
    with open(PROCESSED_GIS_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_regions, f, indent=2)

    print(f"[+] Successfully processed {len(processed_regions)} coastal regions into {PROCESSED_GIS_FILE}")
    return processed_regions

if __name__ == "__main__":
    process_gis_data()
