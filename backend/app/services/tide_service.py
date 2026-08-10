from app.config.logging import logger

class TideService:
    """Service layer boundary for oceanographic tide data processing."""
    
    async def get_tides(self):
        logger.info("TideService initialized.")
        return {"status": "service_ready"}

tide_service = TideService()
