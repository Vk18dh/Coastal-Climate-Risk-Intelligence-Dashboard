from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base

class TideData(Base):
    """
    SQLAlchemy ORM model for oceanographic tide & wave data.
    """
    __tablename__ = "tide_data"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    tide_height_m = Column(Float, nullable=False)
    wave_height_m = Column(Float, nullable=False)
    sea_surface_temp_c = Column(Float, nullable=True)
    sea_level_anomaly_m = Column(Float, nullable=True, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "region_id": self.region_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "tide_height_m": self.tide_height_m,
            "wave_height_m": self.wave_height_m,
            "sea_surface_temp_c": self.sea_surface_temp_c,
            "sea_level_anomaly_m": self.sea_level_anomaly_m,
        }
