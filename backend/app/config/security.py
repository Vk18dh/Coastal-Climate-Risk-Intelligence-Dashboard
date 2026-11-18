"""CORS and HTTP security configuration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings


def configure_cors(app: FastAPI) -> None:
    """
    Attach the CORS middleware to the FastAPI application.

    Origins are loaded from the CORS_ORIGINS environment variable.
    Additional security headers (CSP, HSTS, etc.) will be added
    via Nginx in Phase 12.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
