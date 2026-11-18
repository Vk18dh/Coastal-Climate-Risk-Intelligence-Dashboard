import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

from app.models.region import Region
from app.providers.exceptions import ProviderConnectionError
from app.providers.weather.mock import MockWeatherProvider
from app.providers.tide.mock import MockTideProvider
from app.services.ingestion import IngestionService


class FailingWeatherProvider(MockWeatherProvider):
    def __init__(self):
        self.attempts = 0

    async def fetch_weather(self, region, start_time, end_time):
        self.attempts += 1
        raise ProviderConnectionError("Failed to connect to weather API")


class RecoveringWeatherProvider(MockWeatherProvider):
    def __init__(self):
        self.attempts = 0

    async def fetch_weather(self, region, start_time, end_time):
        self.attempts += 1
        if self.attempts < 3:
            raise ProviderConnectionError("Temporary failure")
        return await super().fetch_weather(region, start_time, end_time)


@pytest.fixture
def sample_region():
    return Region(
        id=1,
        name="Test Region for Ingestion",
        district="Test District",
        geometry="MULTIPOLYGON(((80.0 13.0, 80.5 13.0, 80.5 13.5, 80.0 13.5, 80.0 13.0)))"
    )


async def test_successful_weather_ingestion(sample_region):
    with patch("app.services.ingestion.weather_repo.bulk_upsert", new_callable=AsyncMock) as mock_upsert:
        mock_upsert.side_effect = lambda db, records: len(records)
        service = IngestionService(MockWeatherProvider(), MockTideProvider())
        start = datetime.utcnow()
        end = start + timedelta(hours=3)
        
        upserted = await service.ingest_weather_for_region(None, sample_region, start, end)
        
        assert upserted == 4
        mock_upsert.assert_called_once()


async def test_successful_tide_ingestion(sample_region):
    with patch("app.services.ingestion.tide_repo.bulk_upsert", new_callable=AsyncMock) as mock_upsert:
        mock_upsert.side_effect = lambda db, records: len(records)
        service = IngestionService(MockWeatherProvider(), MockTideProvider())
        start = datetime.utcnow()
        end = start + timedelta(hours=2)
        
        upserted = await service.ingest_tides_for_region(None, sample_region, start, end)
        
        assert upserted == 3
        mock_upsert.assert_called_once()


async def test_weather_ingestion_retry_failure(sample_region):
    failing_provider = FailingWeatherProvider()
    service = IngestionService(failing_provider, MockTideProvider())
    
    start = datetime.utcnow()
    end = start + timedelta(hours=1)
    
    with pytest.raises(ProviderConnectionError):
        await service.ingest_weather_for_region(None, sample_region, start, end)
        
    assert failing_provider.attempts == 3


async def test_weather_ingestion_retry_success(sample_region):
    with patch("app.services.ingestion.weather_repo.bulk_upsert", new_callable=AsyncMock) as mock_upsert:
        mock_upsert.side_effect = lambda db, records: len(records)
        recovering_provider = RecoveringWeatherProvider()
        service = IngestionService(recovering_provider, MockTideProvider())
        
        start = datetime.utcnow()
        end = start + timedelta(hours=1)
        
        upserted = await service.ingest_weather_for_region(None, sample_region, start, end)
        
        assert upserted == 2
    assert recovering_provider.attempts == 3
