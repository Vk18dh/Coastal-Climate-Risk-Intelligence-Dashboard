from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base

class HistoricalFlood(Base):
    """
    SQLAlchemy ORM model for historical flood events and disaster records.
    """
    __tablename__ = "historical_floods"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    event_name = Column(String(100), nullable=True)
    
    flood_height_m = Column(Float, nullable=False)
    rainfall_24h_mm = Column(Float, nullable=False)
    damage_severity = Column(String(20), nullable=False) # Minor, Moderate, Severe, Catastrophic
    affected_population = Column(Integer, nullable=True)
    economic_loss_usd_m = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "region_id": self.region_id,
            "year": self.year,
            "event_name": self.event_name,
            "flood_height_m": self.flood_height_m,
            "rainfall_24h_mm": self.rainfall_24h_mm,
            "damage_severity": self.damage_severity,
            "affected_population": self.affected_population,
            "economic_loss_usd_m": self.economic_loss_usd_m,
        }
