"""
Health check endpoint.

GET /api/v1/health

Returns the operational status of the API and its backing services.
Designed to degrade gracefully: if a dependency is down, the endpoint
still returns 200 with that dependency's status marked as "error".

This allows monitoring tools to distinguish between:
  - API completely down (no response)
  - API running, dependency down (200 + "error" field)
"""
import logging

from fastapi import APIRouter

from app.config.constants import API_VERSION
from app.database.connection import check_db_connection, check_redis_connection

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "",
    summary="System health check",
    response_description="Service and dependency health status",
)
async def health_check() -> dict:
    """
    Verify that the API and its dependencies are operational.

    **Dependencies checked:**
    - `database`: PostgreSQL + PostGIS (primary data store)
    - `redis`: Redis cache

    A `200 OK` response indicates the API process is running.
    Check individual dependency fields for their specific status.
    """
    db_status = await check_db_connection()
    redis_status = await check_redis_connection()

    logger.info(
        "Health check: db=%s redis=%s",
        "ok" if db_status else "error",
        "ok" if redis_status else "error",
    )

    return {
        "success": True,
        "message": "Service healthy",
        "data": {
            "status": "ok",
            "version": API_VERSION,
            "database": "ok" if db_status else "error",
            "redis": "ok" if redis_status else "error",
        },
    }
