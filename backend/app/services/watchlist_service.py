"""
Watchlist Service

CRUD for user watchlist (symbols to track). Uses admin client with user_id filter.
"""

from __future__ import annotations

from typing import Any

from app.core.exceptions import DatabaseError, NotFoundError


class WatchlistService:
    """Service for watchlist table operations scoped by user_id."""

    TABLE = "watchlist"

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

    def list(self, user_id: str) -> list[dict[str, Any]]:
        """List all watchlist items for a user."""
        try:
            result = (
                self.table.select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )
            return list(result.data or [])
        except Exception as e:
            if self._is_table_missing(e):
                return []
            raise DatabaseError(f"Failed to list watchlist: {e!s}") from e

    def add(
        self,
        user_id: str,
        symbol: str,
        *,
        notes: str | None = None,
        alert_on_buy: bool = True,
        alert_on_sell: bool = True,
        min_quantity: int | None = None,
        min_value: float | None = None,
    ) -> dict[str, Any]:
        """Add a symbol to watchlist. Upserts on (user_id, symbol)."""
        symbol = symbol.strip().upper()
        if not symbol:
            raise ValueError("Symbol is required")
        try:
            row = {
                "user_id": user_id,
                "symbol": symbol,
                "alert_on_buy": alert_on_buy,
                "alert_on_sell": alert_on_sell,
            }
            if notes is not None:
                row["notes"] = notes
            if min_quantity is not None:
                row["min_quantity"] = min_quantity
            if min_value is not None:
                row["min_value"] = min_value
            result = self.table.upsert(row, on_conflict="user_id,symbol").execute()
            data = result.data
            if not data:
                raise DatabaseError("Upsert returned no data")
            return data[0]
        except ValueError:
            raise
        except Exception as e:
            if self._is_table_missing(e):
                raise DatabaseError(
                    "Watchlist table is not set up. Please run the Supabase migration: "
                    "supabase/migrations/20250216000001_watchlist.sql"
                ) from e
            raise DatabaseError(f"Failed to add watchlist item: {e!s}") from e

    def get(self, user_id: str, item_id: str) -> dict[str, Any]:
        """Get a single watchlist item by id, ensuring it belongs to user."""
        try:
            result = (
                self.table.select("*")
                .eq("id", item_id)
                .eq("user_id", user_id)
                .maybe_single()
                .execute()
            )
            if not result.data:
                raise NotFoundError("Watchlist item")
            return result.data
        except NotFoundError:
            raise
        except Exception as e:
            if self._is_table_missing(e):
                raise NotFoundError("Watchlist item") from e
            raise DatabaseError(f"Failed to get watchlist item: {e!s}") from e

    def update(
        self,
        user_id: str,
        item_id: str,
        *,
        notes: str | None = None,
        alert_on_buy: bool | None = None,
        alert_on_sell: bool | None = None,
        min_quantity: int | None = None,
        min_value: float | None = None,
    ) -> dict[str, Any]:
        """Update a watchlist item."""
        self.get(user_id, item_id)
        updates: dict[str, Any] = {}
        if notes is not None:
            updates["notes"] = notes
        if alert_on_buy is not None:
            updates["alert_on_buy"] = alert_on_buy
        if alert_on_sell is not None:
            updates["alert_on_sell"] = alert_on_sell
        if min_quantity is not None:
            updates["min_quantity"] = min_quantity
        if min_value is not None:
            updates["min_value"] = min_value
        if not updates:
            return self.get(user_id, item_id)
        try:
            result = (
                self.table.update(updates)
                .eq("id", item_id)
                .eq("user_id", user_id)
                .execute()
            )
            if not result.data:
                raise NotFoundError("Watchlist item")
            return result.data[0]
        except NotFoundError:
            raise
        except Exception as e:
            if self._is_table_missing(e):
                raise NotFoundError("Watchlist item") from e
            raise DatabaseError(f"Failed to update watchlist item: {e!s}") from e

    def remove(self, user_id: str, item_id: str) -> None:
        """Remove a watchlist item."""
        self.get(user_id, item_id)
        try:
            self.table.delete().eq("id", item_id).eq("user_id", user_id).execute()
        except Exception as e:
            if self._is_table_missing(e):
                raise NotFoundError("Watchlist item") from e
            raise DatabaseError(f"Failed to remove watchlist item: {e!s}") from e

    def remove_by_symbol(self, user_id: str, symbol: str) -> None:
        """Remove watchlist item by symbol."""
        symbol = symbol.strip().upper()
        try:
            result = (
                self.table.delete()
                .eq("user_id", user_id)
                .eq("symbol", symbol)
                .execute()
            )
            if result.data is None and not result.count:
                raise NotFoundError("Watchlist item")
        except NotFoundError:
            raise
        except Exception as e:
            if self._is_table_missing(e):
                raise NotFoundError("Watchlist item") from e
            raise DatabaseError(f"Failed to remove watchlist item: {e!s}") from e
