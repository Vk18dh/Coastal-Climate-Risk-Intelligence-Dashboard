from fastapi import APIRouter
from app.database.connection import check_db_connection
from app.config.settings import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def get_health_status():
    """
    Health check endpoint returning system infrastructure connectivity status.
    """
    db_ok = check_db_connection()
    return {
        "success": True,
        "message": "Coastal Climate Risk Intelligence Platform API is active",
        "data": {
            "status": "healthy",
            "environment": "development" if settings.DEBUG else "production",
            "database_connected": db_ok,
            "version": "1.0.0"
        }
    }
