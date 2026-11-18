"""
Custom exception hierarchy for the application.

All application-specific exceptions inherit from AppBaseException.
The global exception handler in middleware/error_handler.py converts
these into consistent JSON responses without leaking internal details.
"""
from typing import Optional


class AppBaseException(Exception):
    """
    Base class for all application-specific exceptions.

    Attributes:
        message:     Human-readable error message returned to the client.
        status_code: HTTP status code for the response.
        detail:      Optional internal detail — logged but NOT returned to client.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        detail: Optional[str] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class DatabaseException(AppBaseException):
    """Raised when a database operation fails unexpectedly."""

    def __init__(self, message: str = "A database error occurred.") -> None:
        super().__init__(message=message, status_code=503)


class ExternalAPIException(AppBaseException):
    """Raised when an external data provider is unreachable or returns an error."""

    def __init__(self, message: str = "External API request failed.") -> None:
        super().__init__(message=message, status_code=502)


class ResourceNotFoundException(AppBaseException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            message=f"{resource} not found.",
            status_code=404,
        )


class ValidationException(AppBaseException):
    """Raised when input data fails domain-level validation (distinct from Pydantic errors)."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=422)
