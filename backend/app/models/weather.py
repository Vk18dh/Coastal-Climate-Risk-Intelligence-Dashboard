from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base

class WeatherData(Base):
    """
    SQLAlchemy ORM model for meteorological weather observations.
    """
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    temperature_c = Column(Float, nullable=False)
    rainfall_mm = Column(Float, nullable=False, default=0.0)
    humidity_pct = Column(Float, nullable=False)
    wind_speed_kmh = Column(Float, nullable=False)
    pressure_hpa = Column(Float, nullable=False)
    condition = Column(String(50), nullable=False, default="Clear")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "region_id": self.region_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "temperature_c": self.temperature_c,
            "rainfall_mm": self.rainfall_mm,
            "humidity_pct": self.humidity_pct,
            "wind_speed_kmh": self.wind_speed_kmh,
            "pressure_hpa": self.pressure_hpa,
            "condition": self.condition,
        }
