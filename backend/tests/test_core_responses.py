"""
Tests for Core Response Module
"""

from app.core.responses import (
    APIResponse,
    ErrorResponse,
    SuccessResponse,
    error_response,
    success_response,
)


def test_success_response():
    """Test success response creation."""
    response = success_response(data={"key": "value"}, message="Success")
    assert response.success is True
    assert response.data == {"key": "value"}
    assert response.message == "Success"
    assert response.errors is None


def test_success_response_defaults():
    """Test success response with defaults."""
    response = success_response()
    assert response.success is True
    assert response.message == "Success"
    assert response.data is None


def test_error_response():
    """Test error response creation."""
    errors = [{"field": "email", "message": "Invalid email"}]
    response = error_response(message="Validation failed", errors=errors)
    assert response.success is False
    assert response.message == "Validation failed"
    assert response.errors == errors


def test_error_response_no_errors():
    """Test error response with no errors (should return None)."""
    response = error_response(message="Something went wrong")
    assert response.success is False
    assert response.message == "Something went wrong"
    assert response.errors is None


def test_api_response_inheritance():
    """Test APIResponse inheritance."""
    success = SuccessResponse(data={"test": "data"})
    error = ErrorResponse(message="Error occurred")

    assert isinstance(success, APIResponse)
    assert isinstance(error, APIResponse)
    assert success.success is True
    assert error.success is False

