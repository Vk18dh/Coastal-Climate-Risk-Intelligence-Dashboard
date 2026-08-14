#!/usr/bin/env python3
"""
Database Seeder Script for Coastal Climate Risk Intelligence Platform.
Imports GeoJSON region boundaries, elevation data, historical flood events, and sample climate metrics into PostgreSQL/PostGIS.
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from app.database.connection import check_db_connection, engine
from app.database.session import SessionLocal
from app.database.base import Base
from app.models import Region, WeatherData, TideData, ElevationData, RiskScore, HistoricalFlood, AIReport

def seed():
    print("[*] Starting database seed process...")
    is_connected = check_db_connection()
    if not is_connected:
        print("[!] PostgreSQL database is not accessible currently. Skipping live DB insertion.")
        print("[+] Processed JSON seed files in data/processed/ are ready for Dual-Mode fallback.")
        return False

    print("[*] Creating database tables if not existing...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Load cleaned regions
        regions_path = os.path.join(BASE_DIR, "data", "processed", "regions_cleaned.json")
        if os.path.exists(regions_path):
            with open(regions_path, "r", encoding="utf-8") as f:
                regions_data = json.load(f)

            for item in regions_data:
                existing = db.query(Region).filter(Region.code == item["code"]).first()
                if not existing:
                    reg = Region(
                        code=item["code"],
                        name=item["name"],
                        district=item["district"],
                        state=item["state"],
                        country=item.get("country", "India"),
                        latitude=item["latitude"],
                        longitude=item["longitude"],
                        area_sqkm=item.get("area_sqkm"),
                        population=item.get("population"),
                        vulnerability_tier=item.get("vulnerability_tier", "Medium"),
                        geometry=item.get("geometry")
                    )
                    db.add(reg)
            db.commit()
            print(f"[+] Seeded {len(regions_data)} coastal regions into PostgreSQL.")

        # Load historical floods
        floods_path = os.path.join(BASE_DIR, "data", "processed", "historical_floods.json")
        if os.path.exists(floods_path):
            with open(floods_path, "r", encoding="utf-8") as f:
                floods_data = json.load(f)

            for item in floods_data:
                existing_flood = db.query(HistoricalFlood).filter(
                    HistoricalFlood.region_id == item["region_id"],
                    HistoricalFlood.year == item["year"]
                ).first()
                if not existing_flood:
                    flood = HistoricalFlood(
                        region_id=item["region_id"],
                        year=item["year"],
                        event_name=item.get("event_name"),
                        flood_height_m=item["flood_height_m"],
                        rainfall_24h_mm=item["rainfall_24h_mm"],
                        damage_severity=item["damage_severity"],
                        affected_population=item.get("affected_population"),
                        economic_loss_usd_m=item.get("economic_loss_usd_m")
                    )
                    db.add(flood)
            db.commit()
            print(f"[+] Seeded {len(floods_data)} historical flood records into PostgreSQL.")

    except Exception as e:
        db.rollback()
        print(f"[!] Error during database seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
