from fastapi import APIRouter
from app.api.v1.health.router import router as health_router
from app.api.v1.weather.router import router as weather_router
from app.api.v1.tides.router import router as tides_router
from app.api.v1.regions.router import router as regions_router
from app.api.v1.risk.router import router as risk_router
from app.api.v1.analytics.router import router as analytics_router
from app.api.v1.ai.router import router as ai_report_router
from app.api.v1.reports.router import router as reports_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(weather_router)
api_router.include_router(tides_router)
api_router.include_router(regions_router)
api_router.include_router(risk_router)
api_router.include_router(analytics_router)
api_router.include_router(ai_report_router)
api_router.include_router(reports_router)
