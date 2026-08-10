from app.config.logging import logger

class DashboardService:
    """Service layer boundary for dashboard overview aggregated metadata."""
    
    async def get_dashboard_overview(self):
        logger.info("DashboardService initialized.")
        return {"status": "service_ready"}

dashboard_service = DashboardService()
