"""
User Profile Endpoints

CRUD API endpoints for user profile management.
Profiles are stored in the user_profiles table in Supabase.
"""

from fastapi import APIRouter

from app.core.auth import CurrentUser
from app.core.models import UserProfileCreate, UserProfileResponse, UserProfileUpdate
from app.core.responses import success_response
from app.services.profile_service import ProfileService

router = APIRouter()


def _get_service() -> ProfileService:
    return ProfileService()


@router.get("/", response_model=None)
async def get_profile(user: CurrentUser):
    """
    Get the current user's profile.

    Fetches from user_profiles table. If no profile exists yet,
    automatically creates one from the auth user data.
    """
    service = _get_service()
    user_metadata = user.user_metadata or {}
    profile = service.get_or_create(
        user_id=str(user.id),
        email=user.email,
        full_name=user_metadata.get("full_name"),
    )
    return success_response(
        data=UserProfileResponse(**profile).model_dump(mode="json"),
        message="Profile retrieved",
    )


@router.post("/", response_model=None, status_code=201)
async def create_profile(user: CurrentUser, body: UserProfileCreate):
    """
    Explicitly create a user profile.

    If a profile already exists, the existing profile is returned.
    """
    service = _get_service()
    profile = service.create(
        user_id=str(user.id),
        email=user.email,
        full_name=body.full_name,
    )
    return success_response(
        data=UserProfileResponse(**profile).model_dump(mode="json"),
        message="Profile created",
    )


@router.put("/", response_model=None)
async def update_profile(user: CurrentUser, body: UserProfileUpdate):
    """
    Update the current user's profile.

    Only provided (non-null) fields are updated.
    """
    service = _get_service()

    # Ensure profile exists first
    service.get_or_create(
        user_id=str(user.id),
        email=user.email,
    )

    updates = body.model_dump(exclude_none=True)
    profile = service.update(user_id=str(user.id), updates=updates)
    return success_response(
        data=UserProfileResponse(**profile).model_dump(mode="json"),
        message="Profile updated",
    )


@router.delete("/", response_model=None)
async def delete_profile(user: CurrentUser):
    """Delete the current user's profile."""
    service = _get_service()
    deleted = service.delete(user_id=str(user.id))
    if not deleted:
        return success_response(message="No profile to delete")
    return success_response(message="Profile deleted")
