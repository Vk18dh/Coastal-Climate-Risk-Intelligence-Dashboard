"""
Alembic migration environment — async SQLAlchemy configuration.

This file is executed by Alembic when generating or running migrations.

Key design decisions:
  - Uses async engine (asyncpg) consistent with the application runtime.
  - DATABASE_URL is read from the application settings (not alembic.ini)
    so credentials come from the environment variable, never from a file.
  - target_metadata points to Base.metadata so autogenerate works once
    Phase 3 models are imported via app/database/base.py.

To add a model to Alembic's awareness (Phase 3+):
    Import the model module anywhere *before* the `target_metadata` line,
    or import it in app/database/base.py. SQLAlchemy will discover it
    automatically because it inherits from Base.
"""
import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

# Ensure the backend/ root is on sys.path so 'app' is importable when
# Alembic is invoked from any working directory (e.g. project root or CI).
_BACKEND_DIR = Path(__file__).resolve().parent.parent  # backend/
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# ── Alembic Config ────────────────────────────────────────────────────────────
config = context.config

# Logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── Application imports ───────────────────────────────────────────────────────
# Import Base so autogenerate can detect schema changes.
# Phase 3+: import model modules here (or in app/database/base.py) to
# register them with Base.metadata before autogenerate runs.
from app.database.base import Base  # noqa: E402
from app.config.settings import settings  # noqa: E402

# Import all models so their tables are registered with Base.metadata.
# Alembic autogenerate compares Base.metadata against the live DB schema.
import app.models  # noqa: E402, F401

target_metadata = Base.metadata


# ── Schema filter ─────────────────────────────────────────────────────────────
# Exclude PostGIS internal tables (tiger, topology) from autogenerate.
# The postgis/postgis Docker image installs these into the public schema,
# so schema-level filtering is insufficient; we also filter by table name.
_POSTGIS_INTERNAL_PREFIXES = (
    # Tiger geocoder tables
    "addr", "addrfeat", "bg", "county", "cousub", "direction_lookup",
    "edges", "faces", "featnames", "geocode_settings", "layer",
    "loader_lookuptables", "loader_platform", "loader_variables",
    "pagc_gaz", "pagc_lex", "pagc_rules", "place", "place_lookup",
    "secondary_unit_lookup", "spatial_ref_sys", "state", "state_lookup",
    "street_type_lookup", "tabblock", "tabblock20", "topology", "tract",
    "zcta5", "zip_lookup", "zip_lookup_all", "zip_lookup_base",
    "zip_state", "zip_state_loc", "countysub_lookup", "county_lookup",
    "geocode_settings_default",
)


def _include_name(name: str, type_: str, parent_names: dict) -> bool:
    """Return False for PostGIS internal schema objects."""
    if type_ == "schema":
        return name in (None, "public")
    if type_ == "table":
        return name not in _POSTGIS_INTERNAL_PREFIXES
    return True


# ── Offline migrations ────────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    """
    Run migrations without a live database connection.
    Produces SQL statements only — useful for review before applying.
    """
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_schemas=True,
        include_name=_include_name,
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Online migrations (async) ─────────────────────────────────────────────────
def do_run_migrations(connection: object) -> None:
    """Run migrations on a synchronous connection (called from async context)."""
    context.configure(
        connection=connection,  # type: ignore[arg-type]
        target_metadata=target_metadata,
        compare_type=True,
        include_schemas=True,
        include_name=_include_name,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Create an async engine and run migrations within a connection."""
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations)

    await engine.dispose()


# ── Entry point ───────────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
