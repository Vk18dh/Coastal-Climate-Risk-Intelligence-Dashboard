"""
Database engine creation and connectivity health checks.

Exports:
  engine              — Shared async SQLAlchemy engine (used by session.py)
  check_db_connection — Async health check function (used by health endpoint)
  get_redis_client    — Returns (or lazily creates) the shared Redis client
  check_redis_connection — Async Redis health check
"""
import asyncio
import logging

import redis.asyncio as aioredis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config.constants import HEALTH_CHECK_TIMEOUT_SECONDS
from app.config.settings import settings

logger = logging.getLogger(__name__)

# ── SQLAlchemy async engine ────────────────────────────────────────────────────
# pool_pre_ping=True: validates connections before use (handles idle timeouts)
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


async def check_db_connection() -> bool:
    """
    Run a lightweight query to verify PostgreSQL/PostGIS connectivity.

    Returns True if the database is reachable, False otherwise.
    Failure is logged but never raised — callers decide how to handle it.
    """
    try:
        async def _ping() -> bool:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True

        return await asyncio.wait_for(_ping(), timeout=float(HEALTH_CHECK_TIMEOUT_SECONDS))
    except Exception as exc:  # noqa: BLE001
        logger.error("Database health check failed: %s", exc)
        return False


# ── Redis async client ────────────────────────────────────────────────────────
_redis_client: aioredis.Redis | None = None  # type: ignore[type-arg]


def get_redis_client() -> aioredis.Redis:  # type: ignore[type-arg]
    """Return (or lazily create) the shared async Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_timeout=HEALTH_CHECK_TIMEOUT_SECONDS,
            socket_connect_timeout=HEALTH_CHECK_TIMEOUT_SECONDS,
        )
    return _redis_client


async def check_redis_connection() -> bool:
    """
    Send a PING command to verify Redis connectivity.

    Returns True if Redis is reachable, False otherwise.
    """
    try:
        client = get_redis_client()
        pong = await asyncio.wait_for(client.ping(), timeout=float(HEALTH_CHECK_TIMEOUT_SECONDS))
        return bool(pong)
    except Exception as exc:  # noqa: BLE001
        logger.error("Redis health check failed: %s", exc)
        return False
