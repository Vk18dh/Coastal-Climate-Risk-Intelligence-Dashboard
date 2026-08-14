from sqlalchemy import create_engine, text
from app.config.settings import settings
from app.config.logging import logger

# Create SQLAlchemy engine with PostGIS capabilities
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False,
)

def check_db_connection() -> bool:
    """Verifies database connection availability."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.warning(f"Database connection warning: {e}")
        return False

