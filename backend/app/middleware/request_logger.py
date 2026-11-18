"""
HTTP request/response logging middleware.

Logs every handled request with:
  - HTTP method
  - Path
  - Response status code
  - Response time in milliseconds

Registered on the FastAPI application in main.py.
Runs after CORS middleware but before route handlers.
"""
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log each inbound HTTP request and its response status/duration."""

    async def dispatch(self, request: Request, call_next: object) -> Response:
        start_time = time.perf_counter()

        response: Response = await call_next(request)  # type: ignore[operator]

        duration_ms = (time.perf_counter() - start_time) * 1_000

        logger.info(
            "%s %s -> %d  (%.1f ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response
