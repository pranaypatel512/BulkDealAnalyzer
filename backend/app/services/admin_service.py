"""
Admin Service

Admin-only operations: list users (from user_profiles), update role, dashboard stats.
Uses Supabase admin client (bypasses RLS).
"""

from __future__ import annotations

from typing import Any

from app.core.exceptions import DatabaseError, NotFoundError


class AdminService:
    """Service for admin-only database operations."""

    def __init__(self) -> None:
        from app.core.database import get_supabase_admin_client

        self._client = get_supabase_admin_client()

    def list_users(
        self,
        page: int = 1,
        page_size: int = 20,
        role: str | None = None,
    ) -> dict[str, Any]:
        """
        List user profiles with pagination (admin only).

        Returns items, total count (approximate), page, page_size.
        """
        try:
            table = self._client.table("user_profiles")
            query = table.select("id,user_id,email,full_name,role,created_at", count="exact").order(
                "created_at", desc=True
            )
            if role and role in ("user", "admin"):
                query = query.eq("role", role)
            page_size = max(1, min(100, page_size))
            page = max(1, page)
            lo = (page - 1) * page_size
            hi = lo + page_size - 1
            result = query.range(lo, hi).execute()
            items = result.data or []
            total = result.count if result.count is not None else len(items)
            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
            }
        except Exception as e:
            raise DatabaseError(f"Failed to list users: {e!s}") from e

    def update_user_role(self, user_id: str, role: str) -> dict[str, Any]:
        """Update a user's role (admin only). role must be 'user' or 'admin'."""
        if role not in ("user", "admin"):
            raise ValueError("role must be 'user' or 'admin'")
        try:
            table = self._client.table("user_profiles")
            result = table.update({"role": role}).eq("user_id", user_id).execute()
            if not result.data:
                raise NotFoundError("User profile")
            return result.data[0]
        except (NotFoundError, ValueError):
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to update role: {e!s}") from e

    def get_stats(self) -> dict[str, Any]:
        """Return simple counts for admin dashboard (users, bulk_deals, etc.)."""
        stats: dict[str, Any] = {}
        try:
            up = self._client.table("user_profiles").select("id", count="exact").execute()
            stats["users"] = up.count if up.count is not None else len(up.data or [])
        except Exception:
            stats["users"] = 0
        try:
            bd = self._client.table("bulk_deals").select("id", count="exact").execute()
            stats["bulk_deals"] = bd.count if bd.count is not None else len(bd.data or [])
        except Exception:
            stats["bulk_deals"] = 0
        try:
            bl = self._client.table("block_deals").select("id", count="exact").execute()
            stats["block_deals"] = bl.count if bl.count is not None else len(bl.data or [])
        except Exception:
            stats["block_deals"] = 0
        return stats
