"""
Comprehensive test suite for prototype API endpoints:
- Regions
- Dashboard Overview & KPIs
- GIS Maps & GeoJSON
- Statistical Analytics (Phase 6)
- AI Insights
- Report Generation
"""
import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture
async def api_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_regions_endpoint(api_client: AsyncClient):
    resp = await api_client.get("/api/v1/regions")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    region_1 = next(r for r in data if r["id"] == 1)
    assert region_1["name"] == "Chennai Coastal Zone"
    assert "latest_risk" in region_1
    assert region_1["latest_risk"]["status"] == "success"
    assert region_1["latest_risk"]["final_score"] is not None


@pytest.mark.asyncio
async def test_region_detail_endpoint(api_client: AsyncClient):
    resp = await api_client.get("/api/v1/regions/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert "geojson_polygon" in data
    assert data["geojson_polygon"]["type"] == "Polygon"


@pytest.mark.asyncio
async def test_dashboard_endpoint(api_client: AsyncClient):
    resp = await api_client.get("/api/v1/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert "kpis" in data
    assert "today_situation" in data
    assert "regions" in data
    assert "overall_risk_score" in data["kpis"]
    assert "high_risk_regions" in data["kpis"]


@pytest.mark.asyncio
async def test_maps_geojson_endpoint(api_client: AsyncClient):
    resp = await api_client.get("/api/v1/maps/geojson")
    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) >= 5
    feat = data["features"][0]
    assert feat["type"] == "Feature"
    assert "ccri_score" in feat["properties"]
    assert "risk_level" in feat["properties"]


@pytest.mark.asyncio
async def test_analytics_timeseries(api_client: AsyncClient):
    resp = await api_client.get("/api/v1/analytics/timeseries?region_id=1&metric=rainfall&days=14")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["metric"] == "rainfall"
    assert len(data["observations"]) == 14
    stats = data["statistics"]
    assert stats["count"] == 14
    assert stats["sample_stddev"] is not None
    assert "trend" in stats
    assert stats["trend"]["first_value"] is not None


@pytest.mark.asyncio
async def test_analytics_correlation(api_client: AsyncClient):
    resp = await api_client.get("/api/v1/analytics/correlation?region_id=1&variable_x=rainfall&variable_y=risk&days=30")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["paired_observation_count"] == 30
    assert data["correlation"] is not None
    assert -1.0 <= data["correlation"] <= 1.0


@pytest.mark.asyncio
async def test_analytics_distribution(api_client: AsyncClient):
    resp = await api_client.get("/api/v1/analytics/distribution?region_id=1&days=30")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "distribution" in data
    assert sum(data["distribution"].values()) == pytest.approx(100.0, rel=1e-1)


@pytest.mark.asyncio
async def test_analytics_comparison(api_client: AsyncClient):
    resp = await api_client.get("/api/v1/analytics/comparison?metric=risk&days=10")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert len(data["regions"]) >= 5


@pytest.mark.asyncio
async def test_ai_insights_endpoint(api_client: AsyncClient):
    resp = await api_client.get("/api/v1/ai/regions/1/insights")
    assert resp.status_code == 200
    data = resp.json()
    assert "overall_situation" in data
    assert len(data["main_contributors"]) > 0
    assert len(data["recommended_actions"]) > 0
    assert "data_limitations" in data
    assert data["is_llm_generated"] in (True, False)


@pytest.mark.asyncio
async def test_ai_ask_endpoint(api_client: AsyncClient):
    resp = await api_client.post("/api/v1/ai/ask", json={"region_id": 1, "question": "Why is this region at risk?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "Chennai" in data["answer"]


@pytest.mark.asyncio
async def test_report_generation(api_client: AsyncClient):
    payload = {"region_id": 1, "include_ai_insights": True}
    resp = await api_client.post("/api/v1/reports/generate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["report_id"].startswith("CCRI-REP-")
    assert data["region_name"] == "Chennai Coastal Zone"
    assert "current_ccri" in data
    assert "statistical_summary" in data
    assert "recommended_actions" in data

