from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database.base import Base

class AIReport(Base):
    """
    SQLAlchemy ORM model for generated AI Executive Summaries & Climate Advisories.
    """
    __tablename__ = "ai_reports"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    risk_level = Column(String(20), nullable=False)
    summary = Column(Text, nullable=False)
    key_threats = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    confidence_score = Column(Float, default=0.92)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "region_id": self.region_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "risk_level": self.risk_level,
            "summary": self.summary,
            "key_threats": self.key_threats,
            "recommendations": self.recommendations,
            "confidence_score": self.confidence_score,
        }
