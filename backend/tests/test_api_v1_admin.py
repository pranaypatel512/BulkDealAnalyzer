"""Tests for admin API endpoints (admin role required)."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

USER_ID = "123e4567-e89b-12d3-a456-426614174000"
USER_EMAIL = "admin@example.com"


def _mock_auth_user():
    mock_user = MagicMock()
    mock_user.id = USER_ID
    mock_user.email = USER_EMAIL
    mock_user.user_metadata = {}
    return mock_user


def _auth_patch():
    mock_user = _mock_auth_user()
    mock_response = MagicMock()
    mock_response.user = mock_user
    return patch(
        "app.core.auth._get_supabase_client",
        return_value=MagicMock(
            auth=MagicMock(get_user=MagicMock(return_value=mock_response)),
        ),
    )


def test_admin_status_unauthenticated():
    """GET /admin/status without token returns 401."""
    response = client.get("/api/v1/admin/status")
    assert response.status_code == 401


def test_admin_status_forbidden_when_not_admin():
    """GET /admin/status with valid user but role != admin returns 403."""
    with _auth_patch(), patch(
        "app.services.profile_service.ProfileService.get_by_user_id",
        return_value={"user_id": USER_ID, "email": USER_EMAIL, "role": "user"},
    ):
        response = client.get(
            "/api/v1/admin/status",
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 403
    assert "admin" in response.json().get("detail", "").lower() or "Admin" in str(response.json())


def test_admin_status_success_when_admin():
    """GET /admin/status with admin role returns 200 and admin: true."""
    with _auth_patch(), patch(
        "app.services.profile_service.ProfileService.get_by_user_id",
        return_value={"user_id": USER_ID, "email": USER_EMAIL, "role": "admin"},
    ):
        response = client.get(
            "/api/v1/admin/status",
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data.get("data", {}).get("admin") is True
