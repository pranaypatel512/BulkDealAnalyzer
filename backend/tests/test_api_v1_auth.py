"""Tests for authentication API endpoints."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_auth_status_unauthenticated():
    """Test auth status without token returns not authenticated."""
    response = client.get("/api/v1/auth/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["authenticated"] is False


def test_auth_me_no_token():
    """Test /me endpoint without token returns 401."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_auth_me_invalid_token():
    """Test /me endpoint with invalid token returns 401."""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


def test_auth_me_bad_format():
    """Test /me endpoint with non-Bearer format returns 401."""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Basic some-creds"},
    )
    assert response.status_code == 401


def test_auth_me_with_valid_user():
    """Test /me endpoint with a mocked valid user."""
    mock_user = MagicMock()
    mock_user.id = "123e4567-e89b-12d3-a456-426614174000"
    mock_user.email = "test@example.com"
    mock_user.user_metadata = {"display_name": "Test User", "avatar_url": ""}
    mock_user.email_confirmed_at = "2026-01-01T00:00:00Z"
    mock_user.created_at = "2026-01-01T00:00:00Z"
    mock_user.last_sign_in_at = "2026-02-16T00:00:00Z"

    mock_response = MagicMock()
    mock_response.user = mock_user

    with patch("app.core.auth._get_supabase_client") as mock_client:
        mock_client.return_value.auth.get_user.return_value = mock_response
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer valid-mock-token"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == "123e4567-e89b-12d3-a456-426614174000"
    assert data["data"]["email"] == "test@example.com"
    assert data["data"]["display_name"] == "Test User"
    assert data["data"]["email_confirmed"] is True


def test_auth_status_with_valid_user():
    """Test auth status with a mocked valid user."""
    mock_user = MagicMock()
    mock_user.id = "123e4567-e89b-12d3-a456-426614174000"
    mock_user.email = "test@example.com"

    mock_response = MagicMock()
    mock_response.user = mock_user

    with patch("app.core.auth._get_supabase_client") as mock_client:
        mock_client.return_value.auth.get_user.return_value = mock_response
        response = client.get(
            "/api/v1/auth/status",
            headers={"Authorization": "Bearer valid-mock-token"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["authenticated"] is True
    assert data["data"]["user_id"] == "123e4567-e89b-12d3-a456-426614174000"
