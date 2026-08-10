from app.config.logging import logger

class WeatherService:
    """Service layer boundary for weather observations processing."""
    
    async def get_weather(self):
        logger.info("WeatherService initialized.")
        return {"status": "service_ready"}

weather_service = WeatherService()
