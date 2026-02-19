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


def _admin_auth_patch():
    """Patch auth + profile so current user is admin. Returns (auth_cm, profile_cm)."""
    return (
        _auth_patch(),
        patch(
            "app.services.profile_service.ProfileService.get_by_user_id",
            return_value={"user_id": USER_ID, "email": USER_EMAIL, "role": "admin"},
        ),
    )


def test_admin_list_users_requires_admin():
    """GET /admin/users without admin returns 403."""
    with _auth_patch(), patch(
        "app.services.profile_service.ProfileService.get_by_user_id",
        return_value={"user_id": USER_ID, "email": USER_EMAIL, "role": "user"},
    ):
        response = client.get(
            "/api/v1/admin/users",
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 403


def test_admin_list_users_success():
    """GET /admin/users with admin returns 200 and items."""
    auth_cm, profile_cm = _admin_auth_patch()
    with auth_cm, profile_cm, patch(
        "app.api.v1.admin._get_admin_service",
    ) as mock_svc:
        mock_svc.return_value.list_users.return_value = {
            "items": [{"user_id": USER_ID, "email": USER_EMAIL, "role": "admin"}],
            "total": 1,
            "page": 1,
            "page_size": 20,
        }
        response = client.get(
            "/api/v1/admin/users",
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 200
    assert response.json().get("data", {}).get("items") is not None


def test_admin_update_role_requires_admin():
    """PATCH /admin/users/{id}/role without admin returns 403."""
    with _auth_patch(), patch(
        "app.services.profile_service.ProfileService.get_by_user_id",
        return_value={"user_id": USER_ID, "email": USER_EMAIL, "role": "user"},
    ):
        response = client.patch(
            "/api/v1/admin/users/another-uuid/role",
            json={"role": "admin"},
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 403


def test_admin_update_role_success():
    """PATCH /admin/users/{id}/role with admin returns 200."""
    auth_cm, profile_cm = _admin_auth_patch()
    with auth_cm, profile_cm, patch(
        "app.api.v1.admin._get_admin_service",
    ) as mock_svc:
        mock_svc.return_value.update_user_role.return_value = {
            "user_id": "other-uuid",
            "email": "u@example.com",
            "role": "user",
        }
        response = client.patch(
            "/api/v1/admin/users/other-uuid/role",
            json={"role": "user"},
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 200


def test_admin_stats_requires_admin():
    """GET /admin/stats without admin returns 403."""
    with _auth_patch(), patch(
        "app.services.profile_service.ProfileService.get_by_user_id",
        return_value={"user_id": USER_ID, "email": USER_EMAIL, "role": "user"},
    ):
        response = client.get(
            "/api/v1/admin/stats",
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 403


def test_admin_stats_success():
    """GET /admin/stats with admin returns 200 and counts."""
    auth_cm, profile_cm = _admin_auth_patch()
    with auth_cm, profile_cm, patch(
        "app.api.v1.admin._get_admin_service",
    ) as mock_svc:
        mock_svc.return_value.get_stats.return_value = {
            "users": 5,
            "bulk_deals": 100,
            "block_deals": 20,
        }
        response = client.get(
            "/api/v1/admin/stats",
            headers={"Authorization": "Bearer fake-token"},
        )
    assert response.status_code == 200
    data = response.json().get("data", {})
    assert data.get("users") == 5
    assert data.get("bulk_deals") == 100
