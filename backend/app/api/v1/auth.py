"""
Authentication Endpoints

API endpoints for auth status and user profile.
Actual login/signup is handled client-side via Supabase Auth SDK.
"""

from fastapi import APIRouter

from app.core.auth import CurrentUser, OptionalUser
from app.core.responses import success_response

router = APIRouter()


@router.get("/me")
async def get_current_user_profile(user: CurrentUser):
    """
    Get the authenticated user's profile.

    Requires a valid Supabase JWT in the Authorization header.
    """
    user_metadata = user.user_metadata or {}
    return success_response(
        data={
            "id": str(user.id),
            "email": user.email,
            "display_name": user_metadata.get("display_name", user_metadata.get("full_name", "")),
            "avatar_url": user_metadata.get("avatar_url", ""),
            "email_confirmed": user.email_confirmed_at is not None,
            "created_at": str(user.created_at) if user.created_at else None,
            "last_sign_in": str(user.last_sign_in_at) if user.last_sign_in_at else None,
        },
        message="User profile retrieved",
    )


@router.get("/status")
async def get_auth_status(user: OptionalUser):
    """
    Check authentication status.

    Returns whether the user is authenticated and basic info.
    Works with or without a token.
    """
    if user:
        return success_response(
            data={
                "authenticated": True,
                "user_id": str(user.id),
                "email": user.email,
            },
            message="Authenticated",
        )

    return success_response(
        data={"authenticated": False},
        message="Not authenticated",
    )
