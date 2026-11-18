"""
Application settings — loaded from environment variables via pydantic-settings.

All configuration values must come from environment variables or a .env file.
No secrets are hardcoded here. See .env.example for the full variable list.
"""
from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ───────────────────────────────────────────────────────────
    APP_NAME: str = "Coastal Climate Risk Intelligence Dashboard"
    APP_ENV: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value: object) -> bool:
        """Safely parse DEBUG whether passed as boolean or string like 'true', 'release', etc."""
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "yes", "t", "dev", "development", "debug")
        return bool(value)

    # ── API ───────────────────────────────────────────────────────────────────
    API_V1_PREFIX: str = "/api/v1"

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = (
        "postgresql+asyncpg://coastal_user:coastal_pass@localhost:5432/coastal_climate_db"
    )

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── CORS ──────────────────────────────────────────────────────────────────
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> List[str]:
        """Accept CORS_ORIGINS as a comma-separated string from the environment."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value  # type: ignore[return-value]

    # ── External API placeholders (activated in Phase 4) ─────────────────────
    IMD_API_KEY: str = ""
    INCOIS_API_KEY: str = ""
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"


# Single shared settings instance — import this everywhere
settings = Settings()
