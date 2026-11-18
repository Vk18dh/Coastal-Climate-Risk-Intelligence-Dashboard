"""
Global exception handlers — produce consistent JSON error responses.

All handlers follow the standard response envelope:
    { "success": false, "message": "...", "data": null }

Stack traces are never included in responses — they are only logged.
"""
import logging
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppBaseException

logger = logging.getLogger(__name__)


def _error_envelope(message: str, status_code: int) -> JSONResponse:
    """Build a standard error JSON response."""
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message, "data": None},
    )


async def app_exception_handler(request: Request, exc: Any) -> JSONResponse:
    """Handle all AppBaseException subclasses (DatabaseException, etc.)."""
    assert isinstance(exc, AppBaseException)

    logger.warning(
        "Application error [%s %s] status=%d: %s",
        request.method,
        request.url.path,
        exc.status_code,
        exc.message,
    )

    if exc.detail:
        logger.debug("Exception detail: %s", exc.detail)

    return _error_envelope(exc.message, exc.status_code)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic request validation errors (invalid input)."""
    errors = exc.errors()
    first_msg = errors[0]["msg"] if errors else "Invalid request."
    message = f"Validation error: {first_msg}"

    logger.warning(
        "Validation error [%s %s]: %s",
        request.method,
        request.url.path,
        errors,
    )
    return _error_envelope(message, 422)


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Catch-all for any exception not handled by a more specific handler.

    Logs the full traceback internally.
    Returns a generic 500 response — no stack trace is exposed to the client.
    """
    logger.error(
        "Unhandled exception [%s %s]: %s",
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )
    return _error_envelope("An internal server error occurred.", 500)
