from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database.base import Base

class Region(Base):
    """
    SQLAlchemy ORM model for coastal administrative regions.
    Stores spatial properties, coordinates, and demographic metadata.
    """
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), default="India")
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    area_sqkm = Column(Float, nullable=True)
    population = Column(Integer, nullable=True)
    vulnerability_tier = Column(String(20), default="Medium")
    
    # GeoJSON Feature geometry representation (stored as JSON for compatibility, upgradeable to Geometry column in PostGIS)
    geometry = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "district": self.district,
            "state": self.state,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "area_sqkm": self.area_sqkm,
            "population": self.population,
            "vulnerability_tier": self.vulnerability_tier,
            "geometry": self.geometry,
        }
