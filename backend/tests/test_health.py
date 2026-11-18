"""
Health endpoint smoke tests.

Tests verify the response structure and status code of GET /api/v1/health.
The individual dependency fields ("database", "redis") can be "ok" or "error"
depending on whether services are running in the test environment — this is
intentional so these tests pass in CI without requiring live services.
"""
from httpx import AsyncClient


async def test_health_returns_200(client: AsyncClient) -> None:
    """Health endpoint must always return HTTP 200."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


async def test_health_success_flag(client: AsyncClient) -> None:
    """Response envelope must have success=true."""
    response = await client.get("/api/v1/health")
    body = response.json()
    assert body["success"] is True


async def test_health_response_structure(client: AsyncClient) -> None:
    """Response must conform to the standard APIResponse envelope."""
    response = await client.get("/api/v1/health")
    body = response.json()

    assert "success" in body
    assert "message" in body
    assert "data" in body

    data = body["data"]
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    # Dependency status is "ok" or "error" — not hardcoded to "ok"
    # so tests pass whether or not Docker services are running
    assert data["database"] in ("ok", "error")
    assert data["redis"] in ("ok", "error")


async def test_health_message(client: AsyncClient) -> None:
    """Response message should confirm service health."""
    response = await client.get("/api/v1/health")
    body = response.json()
    assert body["message"] == "Service healthy"
