from app.config.logging import logger

class AIService:
    """Service layer boundary for Groq LLM executive summaries and advisories."""
    
    async def generate_advisory(self):
        logger.info("AIService initialized.")
        return {"status": "service_ready"}

ai_service = AIService()
