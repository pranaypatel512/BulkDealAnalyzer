"""Tests for user profile API endpoints."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Shared mock user fixture
USER_ID = "123e4567-e89b-12d3-a456-426614174000"
USER_EMAIL = "test@example.com"

SAMPLE_PROFILE = {
    "id": "aaaa-bbbb-cccc-dddd",
    "user_id": USER_ID,
    "email": USER_EMAIL,
    "full_name": "Test User",
    "subscription_tier": "free",
    "created_at": "2026-01-01T00:00:00+00:00",
    "updated_at": "2026-01-01T00:00:00+00:00",
}


def _mock_auth_user(*, full_name: str | None = "Test User"):
    """Create a mock Supabase auth user."""
    mock_user = MagicMock()
    mock_user.id = USER_ID
    mock_user.email = USER_EMAIL
    mock_user.user_metadata = {"full_name": full_name} if full_name else {}
    mock_user.email_confirmed_at = "2026-01-01T00:00:00Z"
    mock_user.created_at = "2026-01-01T00:00:00Z"
    mock_user.last_sign_in_at = "2026-02-16T00:00:00Z"
    return mock_user


def _auth_patch():
    """Patch auth to return a valid mock user."""
    mock_user = _mock_auth_user()
    mock_response = MagicMock()
    mock_response.user = mock_user
    return patch(
        "app.core.auth._get_supabase_client",
        return_value=MagicMock(
            auth=MagicMock(get_user=MagicMock(return_value=mock_response)),
        ),
    )


# ---- Unauthenticated ----


def test_get_profile_unauthenticated():
    """GET /profile without token returns 401."""
    response = client.get("/api/v1/profile/")
    assert response.status_code == 401


def test_create_profile_unauthenticated():
    """POST /profile without token returns 401."""
    response = client.post("/api/v1/profile/", json={"full_name": "Test"})
    assert response.status_code == 401


def test_update_profile_unauthenticated():
    """PUT /profile without token returns 401."""
    response = client.put("/api/v1/profile/", json={"full_name": "Updated"})
    assert response.status_code == 401


def test_delete_profile_unauthenticated():
    """DELETE /profile without token returns 401."""
    response = client.delete("/api/v1/profile/")
    assert response.status_code == 401


# ---- GET /profile ----


def test_get_profile_creates_if_missing():
    """GET /profile auto-creates profile from auth user data if none exists."""
    with _auth_patch(), patch(
        "app.api.v1.profile._get_service"
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.get_or_create.return_value = SAMPLE_PROFILE
        mock_svc_factory.return_value = mock_svc

        response = client.get(
            "/api/v1/profile/",
            headers={"Authorization": "Bearer valid-token"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user_id"] == USER_ID
    assert data["data"]["email"] == USER_EMAIL
    assert data["data"]["full_name"] == "Test User"
    mock_svc.get_or_create.assert_called_once_with(
        user_id=USER_ID,
        email=USER_EMAIL,
        full_name="Test User",
    )


# ---- POST /profile ----


def test_create_profile_success():
    """POST /profile creates a new profile."""
    with _auth_patch(), patch(
        "app.api.v1.profile._get_service"
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.create.return_value = SAMPLE_PROFILE
        mock_svc_factory.return_value = mock_svc

        response = client.post(
            "/api/v1/profile/",
            headers={"Authorization": "Bearer valid-token"},
            json={"full_name": "Test User"},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["full_name"] == "Test User"
    assert data["message"] == "Profile created"


def test_create_profile_no_name():
    """POST /profile with no full_name still succeeds."""
    profile_no_name = {**SAMPLE_PROFILE, "full_name": None}
    with _auth_patch(), patch(
        "app.api.v1.profile._get_service"
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.create.return_value = profile_no_name
        mock_svc_factory.return_value = mock_svc

        response = client.post(
            "/api/v1/profile/",
            headers={"Authorization": "Bearer valid-token"},
            json={},
        )

    assert response.status_code == 201


# ---- PUT /profile ----


def test_update_profile_success():
    """PUT /profile updates fields."""
    updated = {**SAMPLE_PROFILE, "full_name": "Updated Name"}
    with _auth_patch(), patch(
        "app.api.v1.profile._get_service"
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.get_or_create.return_value = SAMPLE_PROFILE
        mock_svc.update.return_value = updated
        mock_svc_factory.return_value = mock_svc

        response = client.put(
            "/api/v1/profile/",
            headers={"Authorization": "Bearer valid-token"},
            json={"full_name": "Updated Name"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["full_name"] == "Updated Name"
    assert data["message"] == "Profile updated"


def test_update_profile_subscription():
    """PUT /profile can update subscription tier."""
    updated = {**SAMPLE_PROFILE, "subscription_tier": "premium"}
    with _auth_patch(), patch(
        "app.api.v1.profile._get_service"
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.get_or_create.return_value = SAMPLE_PROFILE
        mock_svc.update.return_value = updated
        mock_svc_factory.return_value = mock_svc

        response = client.put(
            "/api/v1/profile/",
            headers={"Authorization": "Bearer valid-token"},
            json={"subscription_tier": "premium"},
        )

    assert response.status_code == 200
    assert response.json()["data"]["subscription_tier"] == "premium"


def test_update_profile_invalid_tier():
    """PUT /profile rejects invalid subscription tier."""
    with _auth_patch():
        response = client.put(
            "/api/v1/profile/",
            headers={"Authorization": "Bearer valid-token"},
            json={"subscription_tier": "invalid_tier"},
        )

    assert response.status_code == 422


# ---- DELETE /profile ----


def test_delete_profile_success():
    """DELETE /profile deletes the profile."""
    with _auth_patch(), patch(
        "app.api.v1.profile._get_service"
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.delete.return_value = True
        mock_svc_factory.return_value = mock_svc

        response = client.delete(
            "/api/v1/profile/",
            headers={"Authorization": "Bearer valid-token"},
        )

    assert response.status_code == 200
    assert response.json()["message"] == "Profile deleted"


def test_delete_profile_not_found():
    """DELETE /profile when no profile exists returns success message."""
    with _auth_patch(), patch(
        "app.api.v1.profile._get_service"
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.delete.return_value = False
        mock_svc_factory.return_value = mock_svc

        response = client.delete(
            "/api/v1/profile/",
            headers={"Authorization": "Bearer valid-token"},
        )

    assert response.status_code == 200
    assert response.json()["message"] == "No profile to delete"
