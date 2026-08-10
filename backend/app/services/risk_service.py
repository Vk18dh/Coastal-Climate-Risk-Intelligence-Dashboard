from app.config.logging import logger

class RiskService:
    """Service layer boundary for climate risk index computation."""
    
    async def calculate_risk(self):
        logger.info("RiskService initialized.")
        return {"status": "service_ready"}

risk_service = RiskService()
