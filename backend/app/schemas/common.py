"""
Common Pydantic schemas used across all API endpoints.

Formalises the standard response envelope documented in BACKEND.md:
    { "success": true, "message": "...", "data": {} }

Usage in route handlers:
    from app.schemas.common import APIResponse

    @router.get("/example")
    async def example() -> APIResponse[MyDataSchema]:
        return APIResponse(success=True, message="OK", data=my_data)
"""
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    Standard success response envelope.

    All endpoints return this structure so the frontend can rely on a
    consistent shape regardless of the domain.
    """

    success: bool = True
    message: str = "Success"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """
    Standard error response envelope.

    Produced by the global exception handlers in middleware/error_handler.py.
    Typed separately to make OpenAPI schema generation accurate.
    """

    success: bool = False
    message: str
    data: None = None
