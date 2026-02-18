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
        from app.core.database import get_supabase_admin_client, get_supabase_client

        try:
            self._client = get_supabase_admin_client()
        except ValueError:
            self._client = get_supabase_client()

    @property
    def table(self):
        return self._client.table(self.TABLE)

    @staticmethod
    def _is_table_missing(error: Exception) -> bool:
        """Check if the error is due to the table not existing in Supabase."""
        msg = str(error)
        return "PGRST205" in msg or "schema cache" in msg

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
            if result is None:
                return None
            return result.data
        except Exception as e:
            if self._is_table_missing(e):
                return None
            raise DatabaseError(f"Failed to fetch profile: {e!s}") from e

    def create(self, user_id: str, email: str, full_name: str | None = None) -> dict[str, Any]:
        """
        Create a new user profile.

        If a profile already exists for this user, returns the existing one.
        If the table doesn't exist yet, returns a synthetic profile dict.
        """
        existing = self.get_by_user_id(user_id)
        if existing:
            return existing

        fallback = {
            "id": None,
            "user_id": user_id,
            "email": email,
            "full_name": full_name,
            "subscription_tier": "free",
            "role": "user",
            "created_at": None,
            "updated_at": None,
        }
        try:
            data: dict[str, Any] = {
                "user_id": user_id,
                "email": email,
            }
            if full_name:
                data["full_name"] = full_name

            result = self.table.insert(data).execute()
            if not result.data:
                # RLS may have silently blocked the insert (anon key has no auth.uid)
                return fallback
            return result.data[0]
        except Exception as e:
            if self._is_table_missing(e):
                return fallback
            # Log but don't crash -- return synthetic profile
            import logging

            logging.getLogger(__name__).warning("Profile insert failed: %s", e)
            return fallback

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
