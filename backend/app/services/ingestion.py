"""
Ingestion service orchestrating external data fetch, validation, and storage.
"""
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from app.models.region import Region
from app.providers.base import WeatherProvider, TideProvider
from app.providers.exceptions import ProviderError, ProviderConnectionError
from app.repositories.weather import weather_repo
from app.repositories.tide import tide_repo

logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(
        self,
        weather_provider: WeatherProvider,
        tide_provider: TideProvider,
    ):
        self.weather_provider = weather_provider
        self.tide_provider = tide_provider

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ProviderConnectionError, TimeoutError)),
        reraise=True,
    )
    async def fetch_weather_with_retry(
        self, region: Region, start: datetime, end: datetime
    ):
        """Fetch weather with exponential backoff for transient network errors."""
        return await self.weather_provider.fetch_weather(region, start, end)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ProviderConnectionError, TimeoutError)),
        reraise=True,
    )
    async def fetch_tides_with_retry(
        self, region: Region, start: datetime, end: datetime
    ):
        """Fetch tides with exponential backoff for transient network errors."""
        return await self.tide_provider.fetch_tides(region, start, end)

    async def ingest_weather_for_region(
        self, db: AsyncSession, region: Region, start: datetime, end: datetime
    ) -> int:
        """
        Ingest weather data for a region over a specific time window.
        Returns the number of records upserted.
        """
        logger.info(f"Ingesting weather for region {region.name} ({start} to {end})")
        try:
            records = await self.fetch_weather_with_retry(region, start, end)
            if records:
                upserted_count = await weather_repo.bulk_upsert(db, records)
                logger.info(f"Successfully upserted {upserted_count} weather records.")
                return upserted_count
            return 0
        except ProviderError as e:
            logger.error(f"Weather provider error for {region.name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error ingesting weather for {region.name}: {e}")
            raise

    async def ingest_tides_for_region(
        self, db: AsyncSession, region: Region, start: datetime, end: datetime
    ) -> int:
        """
        Ingest tide data for a region over a specific time window.
        Returns the number of records upserted.
        """
        logger.info(f"Ingesting tides for region {region.name} ({start} to {end})")
        try:
            records = await self.fetch_tides_with_retry(region, start, end)
            if records:
                upserted_count = await tide_repo.bulk_upsert(db, records)
                logger.info(f"Successfully upserted {upserted_count} tide records.")
                return upserted_count
            return 0
        except ProviderError as e:
            logger.error(f"Tide provider error for {region.name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error ingesting tides for {region.name}: {e}")
            raise
