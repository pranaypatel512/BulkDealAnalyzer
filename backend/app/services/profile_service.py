"""
User Profile Service

Handles CRUD operations for user profiles in the Supabase database.
"""

from __future__ import annotations

from typing import Any

from app.core.exceptions import DatabaseError, NotFoundError


class ProfileService:
    """Service for user profile database operations."""

    TABLE = "user_profiles"

    def __init__(self) -> None:
        from app.core.database import get_supabase_client

        self._client = get_supabase_client()

    @property
    def table(self):
        return self._client.table(self.TABLE)

    def get_by_user_id(self, user_id: str) -> dict[str, Any] | None:
        """
        Get a user profile by Supabase auth user ID.

        Returns None if no profile exists.
        """
        try:
            result = (
                self.table
                .select("*")
                .eq("user_id", user_id)
                .maybe_single()
                .execute()
            )
            return result.data
        except Exception as e:
            raise DatabaseError(f"Failed to fetch profile: {e!s}") from e

    def create(self, user_id: str, email: str, full_name: str | None = None) -> dict[str, Any]:
        """
        Create a new user profile.

        If a profile already exists for this user, returns the existing one.
        """
        existing = self.get_by_user_id(user_id)
        if existing:
            return existing

        try:
            data: dict[str, Any] = {
                "user_id": user_id,
                "email": email,
            }
            if full_name:
                data["full_name"] = full_name

            result = self.table.insert(data).execute()
            if not result.data:
                raise DatabaseError("Profile creation returned no data")
            return result.data[0]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to create profile: {e!s}") from e

    def update(self, user_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        """
        Update a user profile.

        Only non-None fields in updates are applied.
        """
        clean = {k: v for k, v in updates.items() if v is not None}
        if not clean:
            profile = self.get_by_user_id(user_id)
            if not profile:
                raise NotFoundError("User profile")
            return profile

        try:
            result = (
                self.table
                .update(clean)
                .eq("user_id", user_id)
                .execute()
            )
            if not result.data:
                raise NotFoundError("User profile")
            return result.data[0]
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to update profile: {e!s}") from e

    def delete(self, user_id: str) -> bool:
        """Delete a user profile. Returns True if deleted."""
        try:
            result = (
                self.table
                .delete()
                .eq("user_id", user_id)
                .execute()
            )
            return bool(result.data)
        except Exception as e:
            raise DatabaseError(f"Failed to delete profile: {e!s}") from e

    def get_or_create(
        self, user_id: str, email: str, full_name: str | None = None,
    ) -> dict[str, Any]:
        """Get existing profile or create a new one."""
        profile = self.get_by_user_id(user_id)
        if profile:
            return profile
        return self.create(user_id, email, full_name)
