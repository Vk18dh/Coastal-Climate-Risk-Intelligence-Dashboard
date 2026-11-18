"""
Master API v1 router.

All domain sub-routers are registered here with their path prefix and tags.
Mounted onto the FastAPI app in main.py under API_V1_PREFIX.
"""
from fastapi import APIRouter

from app.api.v1.health.routes import router as health_router
from app.api.v1.risk.routes import router as risk_router
from app.api.v1.regions.routes import router as regions_router
from app.api.v1.dashboard.routes import router as dashboard_router
from app.api.v1.maps.routes import router as maps_router
from app.api.v1.analytics.routes import router as analytics_router
from app.api.v1.ai.routes import router as ai_router
from app.api.v1.reports.routes import router as reports_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(risk_router, prefix="/risk", tags=["Climate Risk Engine"])
api_router.include_router(regions_router, prefix="/regions", tags=["Regions"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(maps_router, prefix="/maps", tags=["GIS & Maps"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["Statistical Analytics"])
api_router.include_router(ai_router, prefix="/ai", tags=["AI Insights"])
api_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
