from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.config.settings import settings
from app.config.logging import setup_logging, logger
from app.middleware.cors import setup_cors
from app.middleware.errors import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)
from app.api.v1.router import api_router

# Setup logging foundation
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.PROJECT_NAME} API backend...")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME} API backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Geospatial Decision Support System for Coastal Climate Risk Assessment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Setup CORS
setup_cors(app)

# Exception Handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Register V1 API Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
async def root():
    return {
        "success": True,
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "data": {
            "version": "1.0.0",
            "docs": "/docs",
            "health": f"{settings.API_V1_STR}/health"
        }
    }
