from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base

class ElevationData(Base):
    """
    SQLAlchemy ORM model for Digital Elevation Model (DEM) regional metrics.
    """
    __tablename__ = "elevation_data"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, unique=True, index=True)
    
    mean_elevation_m = Column(Float, nullable=False)
    min_elevation_m = Column(Float, nullable=False)
    max_elevation_m = Column(Float, nullable=False)
    slope_degrees = Column(Float, nullable=False)
    coastal_distance_km = Column(Float, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "region_id": self.region_id,
            "mean_elevation_m": self.mean_elevation_m,
            "min_elevation_m": self.min_elevation_m,
            "max_elevation_m": self.max_elevation_m,
            "slope_degrees": self.slope_degrees,
            "coastal_distance_km": self.coastal_distance_km,
        }


class RiskScore(Base):
    """
    SQLAlchemy ORM model for calculated Composite Climate Risk Index.
    """
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    rainfall_score = Column(Float, nullable=False)
    tide_score = Column(Float, nullable=False)
    elevation_score = Column(Float, nullable=False)
    flood_score = Column(Float, nullable=False)
    
    final_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False) # Low, Moderate, High, Critical
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "region_id": self.region_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "rainfall_score": self.rainfall_score,
            "tide_score": self.tide_score,
            "elevation_score": self.elevation_score,
            "flood_score": self.flood_score,
            "final_score": self.final_score,
            "risk_level": self.risk_level,
        }
