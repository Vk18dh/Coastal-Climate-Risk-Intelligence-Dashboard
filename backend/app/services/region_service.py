from app.config.logging import logger

class RegionService:
    """Service layer boundary for coastal region spatial queries."""
    
    async def get_regions(self):
        logger.info("RegionService initialized.")
        return {"status": "service_ready"}

region_service = RegionService()
