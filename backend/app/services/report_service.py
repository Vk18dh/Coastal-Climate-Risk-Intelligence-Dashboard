from app.config.logging import logger

class ReportService:
    """Service layer boundary for report generation and export."""
    
    async def generate_report(self):
        logger.info("ReportService initialized.")
        return {"status": "service_ready"}

report_service = ReportService()
