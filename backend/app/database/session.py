"""
Async SQLAlchemy session factory and FastAPI dependency.

Usage in route handlers:
    async def my_route(db: AsyncSession = Depends(get_db)):
        ...
"""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.connection import engine

# Session factory — all sessions are created from this
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a scoped async database session.

    The session is closed automatically after the request completes,
    regardless of whether an exception was raised.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
