import os
from typing import List

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    USE_PYDANTIC_V2_SETTINGS = True
except ImportError:
    from pydantic import BaseSettings
    USE_PYDANTIC_V2_SETTINGS = False


if USE_PYDANTIC_V2_SETTINGS:
    class Settings(BaseSettings):
        PROJECT_NAME: str = "Coastal Climate Risk Intelligence Platform"
        API_V1_STR: str = "/api/v1"
        DEBUG: bool = True
        HOST: str = "0.0.0.0"
        PORT: int = 8000

        # CORS
        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
        ]

        # Database
        POSTGRES_SERVER: str = "localhost"
        POSTGRES_PORT: int = 5432
        POSTGRES_USER: str = "postgres"
        POSTGRES_PASSWORD: str = "postgres"
        POSTGRES_DB: str = "coastal_risk_db"
        DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/coastal_risk_db"

        # Redis
        REDIS_HOST: str = "localhost"
        REDIS_PORT: int = 6379
        REDIS_DB: int = 0
        REDIS_URL: str = "redis://localhost:6379/0"
        CACHE_EXPIRE_SECONDS: int = 900

        # AI / LLM Configuration (100% Free - Groq & Local Embeddings)
        AI_PROVIDER: str = "groq"
        GROQ_API_KEY: str = ""
        AI_MODEL_NAME: str = "llama-3.3-70b-versatile"
        AI_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
        AI_TEMPERATURE: float = 0.2

        # Map Engine & Tile Services (100% Free - OpenFreeMap / Leaflet)
        MAP_ENGINE: str = "leaflet"
        MAP_TILE_PROVIDER: str = "openfreemap"
        MAP_TILE_URL: str = "https://tiles.openfreemap.org/styles/bright"

        # Weather & Ocean Data APIs (100% Free - Open-Meteo)
        WEATHER_API_PROVIDER: str = "open-meteo"
        WEATHER_API_URL: str = "https://api.open-meteo.com/v1/forecast"
        MARINE_API_URL: str = "https://marine-api.open-meteo.com/v1/marine"

        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore"
        )
else:
    class Settings(BaseSettings):
        PROJECT_NAME: str = "Coastal Climate Risk Intelligence Platform"
        API_V1_STR: str = "/api/v1"
        DEBUG: bool = True
        HOST: str = "0.0.0.0"
        PORT: int = 8000

        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
        ]

        POSTGRES_SERVER: str = "localhost"
        POSTGRES_PORT: int = 5432
        POSTGRES_USER: str = "postgres"
        POSTGRES_PASSWORD: str = "postgres"
        POSTGRES_DB: str = "coastal_risk_db"
        DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/coastal_risk_db"

        REDIS_HOST: str = "localhost"
        REDIS_PORT: int = 6379
        REDIS_DB: int = 0
        REDIS_URL: str = "redis://localhost:6379/0"
        CACHE_EXPIRE_SECONDS: int = 900

        AI_PROVIDER: str = "groq"
        GROQ_API_KEY: str = ""
        AI_MODEL_NAME: str = "llama-3.3-70b-versatile"
        AI_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
        AI_TEMPERATURE: float = 0.2

        MAP_ENGINE: str = "leaflet"
        MAP_TILE_PROVIDER: str = "openfreemap"
        MAP_TILE_URL: str = "https://tiles.openfreemap.org/styles/bright"

        WEATHER_API_PROVIDER: str = "open-meteo"
        WEATHER_API_URL: str = "https://api.open-meteo.com/v1/forecast"
        MARINE_API_URL: str = "https://marine-api.open-meteo.com/v1/marine"

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            extra = "ignore"


settings = Settings()
