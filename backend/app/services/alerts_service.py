"""
Alerts Service

List and update user alerts (triggered notifications from watchlist).
"""

from __future__ import annotations

from typing import Any

from app.core.exceptions import DatabaseError, NotFoundError


class AlertsService:
    """Service for alerts table operations scoped by user_id."""

    TABLE = "alerts"

    def __init__(self) -> None:
        from app.core.database import get_supabase_admin_client

        self._client = get_supabase_admin_client()

    @property
    def table(self):
        return self._client.table(self.TABLE)

    @staticmethod
    def _is_table_missing(error: Exception) -> bool:
        """Check if the error is due to the table not existing in Supabase."""
        msg = str(error)
        return "PGRST205" in msg or "schema cache" in msg or "does not exist" in msg.lower()

    def list(
        self,
        user_id: str,
        *,
        limit: int = 50,
        is_read: bool | None = None,
    ) -> list[dict[str, Any]]:
        """List alerts for a user, newest first."""
        try:
            query = (
                self.table.select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .limit(limit)
            )
            if is_read is not None:
                query = query.eq("is_read", is_read)
            result = query.execute()
            return list(result.data or [])
        except Exception as e:
            if self._is_table_missing(e):
                return []
            raise DatabaseError(f"Failed to list alerts: {e!s}") from e

    def get(self, user_id: str, alert_id: str) -> dict[str, Any]:
        """Get a single alert by id."""
        try:
            result = (
                self.table.select("*")
                .eq("id", alert_id)
                .eq("user_id", user_id)
                .maybe_single()
                .execute()
            )
            if not result.data:
                raise NotFoundError("Alert")
            return result.data
        except NotFoundError:
            raise
        except Exception as e:
            if self._is_table_missing(e):
                raise NotFoundError("Alert") from e
            raise DatabaseError(f"Failed to get alert: {e!s}") from e

    def mark_read(self, user_id: str, alert_id: str) -> dict[str, Any]:
        """Mark an alert as read."""
        self.get(user_id, alert_id)
        try:
            result = (
                self.table.update({"is_read": True})
                .eq("id", alert_id)
                .eq("user_id", user_id)
                .execute()
            )
            if not result.data:
                raise NotFoundError("Alert")
            return result.data[0]
        except NotFoundError:
            raise
        except Exception as e:
            if self._is_table_missing(e):
                raise NotFoundError("Alert") from e
            raise DatabaseError(f"Failed to mark alert read: {e!s}") from e

    def mark_all_read(self, user_id: str) -> int:
        """Mark all alerts for the user as read. Returns count updated."""
        try:
            result = (
                self.table.update({"is_read": True})
                .eq("user_id", user_id)
                .eq("is_read", False)
                .execute()
            )
            return len(result.data or [])
        except Exception as e:
            if self._is_table_missing(e):
                return 0
            raise DatabaseError(f"Failed to mark all alerts read: {e!s}") from e

    def unread_count(self, user_id: str) -> int:
        """Return count of unread alerts."""
        try:
            result = (
                self.table.select("id", count="exact")
                .eq("user_id", user_id)
                .eq("is_read", False)
                .execute()
            )
            return result.count or 0
        except Exception as e:
            if self._is_table_missing(e):
                return 0
            raise DatabaseError(f"Failed to count unread alerts: {e!s}") from e
