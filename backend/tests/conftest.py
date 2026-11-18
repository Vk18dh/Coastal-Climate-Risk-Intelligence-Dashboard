"""
pytest configuration and shared fixtures.

All fixtures are async-compatible via pytest-asyncio (asyncio_mode = "auto"
in pyproject.toml, so no @pytest.mark.asyncio decorator is required).
"""
import asyncio
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from main import app
from app.config.settings import settings


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP test client backed by the FastAPI ASGI application.

    Uses httpx.AsyncClient with ASGITransport — no real TCP server is started.
    The application lifespan events (startup/shutdown) run normally, so the
    DB/Redis health checks execute but failures are non-fatal (logged only).
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac


@pytest.fixture
async def db_session() -> AsyncGenerator:
    """
    Async database session fixture for tests.
    """
    # Create the engine inside the fixture so it binds to the test's event loop
    test_engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    
    async with TestSessionLocal() as session:
        yield session
        
    await test_engine.dispose()
