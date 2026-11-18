"""
Coastal Climate Risk Intelligence Dashboard — FastAPI Application Entry Point

Creates and configures the FastAPI application, registers middleware,
exception handlers, and API routers, and manages the application lifecycle.
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.v1.router import api_router
from app.config.logging import configure_logging
from app.config.security import configure_cors
from app.config.settings import settings
from app.core.exceptions import AppBaseException
from app.database.connection import check_db_connection, check_redis_connection
from app.middleware.request_logger import RequestLoggingMiddleware
from app.middleware.error_handler import (
    app_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)

# Configure logging before any other imports produce log output
configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifecycle."""
    # ── Startup ──────────────────────────────────────────────────────────────
    logger.info(
        "Starting '%s' [env=%s, debug=%s]",
        settings.APP_NAME,
        settings.APP_ENV,
        settings.DEBUG,
    )

    db_ok = await check_db_connection()
    redis_ok = await check_redis_connection()

    logger.info("Database (PostgreSQL/PostGIS): %s", "OK" if db_ok else "UNAVAILABLE")
    logger.info("Cache (Redis): %s", "OK" if redis_ok else "UNAVAILABLE")

    if not db_ok:
        logger.warning(
            "Database is unavailable. Endpoints requiring persistence will fail. "
            "Verify DATABASE_URL in .env."
        )

    yield

    # ── Shutdown ─────────────────────────────────────────────────────────────
    logger.info("Shutting down '%s'", settings.APP_NAME)


def create_application() -> FastAPI:
    """Application factory — constructs and configures the FastAPI instance."""
    application = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description=(
            "AI-powered geospatial decision support system "
            "for coastal climate risk assessment."
        ),
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    # CORS — must be registered before routers
    configure_cors(application)

    # Request/response logger — registered after CORS
    application.add_middleware(RequestLoggingMiddleware)

    # Exception handlers
    application.add_exception_handler(AppBaseException, app_exception_handler)  # type: ignore[arg-type]
    application.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    application.add_exception_handler(Exception, unhandled_exception_handler)

    # API routers
    application.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return application


app = create_application()
