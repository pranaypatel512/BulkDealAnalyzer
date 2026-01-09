"""
Standardized API Responses

Provides consistent response formats for the API.
"""

from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard API response format."""

    success: bool
    message: str | None = None
    data: Any = None
    errors: list[dict[str, Any]] | None = None


class SuccessResponse(APIResponse):
    """Success response."""

    success: bool = True


class ErrorResponse(APIResponse):
    """Error response."""

    success: bool = False


def success_response(
    data: Any = None,
    message: str | None = None,
) -> SuccessResponse:
    """
    Create a success response.

    Args:
        data: Response data
        message: Success message

    Returns:
        SuccessResponse instance
    """
    return SuccessResponse(data=data, message=message or "Success")


def error_response(
    message: str,
    errors: list[dict[str, Any]] | None = None,
) -> ErrorResponse:
    """
    Create an error response.

    Args:
        message: Error message
        errors: List of error details

    Returns:
        ErrorResponse instance
    """
    return ErrorResponse(message=message, errors=errors or [])

