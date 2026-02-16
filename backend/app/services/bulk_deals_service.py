"""
Bulk Deals Service

Handles CRUD operations and querying for bulk deals in the Supabase database.
"""

from __future__ import annotations

import math
from typing import Any

from app.core.exceptions import DatabaseError, NotFoundError


class BulkDealsService:
    """Service for bulk deals database operations."""

    TABLE = "bulk_deals"

    def __init__(self) -> None:
        from app.core.database import get_supabase_client

        self._client = get_supabase_client()

    @property
    def table(self):
        return self._client.table(self.TABLE)

    def list_deals(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        symbol: str | None = None,
        deal_type: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        sort_by: str = "date",
        sort_order: str = "desc",
    ) -> dict[str, Any]:
        """
        List bulk deals with filtering, sorting, and pagination.

        Returns dict with deals, total count, and pagination info.
        """
        try:
            query = self.table.select("*", count="exact")

            if symbol:
                query = query.ilike("symbol", f"%{symbol}%")
            if deal_type:
                query = query.eq("deal_type", deal_type.upper())
            if date_from:
                query = query.gte("date", date_from)
            if date_to:
                query = query.lte("date", date_to)

            # Sorting
            desc = sort_order.lower() == "desc"
            if sort_by in ("date", "symbol", "quantity", "price", "client_name"):
                query = query.order(sort_by, desc=desc)
            else:
                query = query.order("date", desc=True)

            # Pagination
            offset = (page - 1) * page_size
            query = query.range(offset, offset + page_size - 1)

            result = query.execute()
            total = result.count if result.count is not None else 0

            return {
                "deals": result.data or [],
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": math.ceil(total / page_size) if page_size > 0 else 0,
            }
        except Exception as e:
            raise DatabaseError(f"Failed to list deals: {e!s}") from e

    def get_by_id(self, deal_id: str) -> dict[str, Any]:
        """Get a single bulk deal by ID."""
        try:
            result = (
                self.table
                .select("*")
                .eq("id", deal_id)
                .maybe_single()
                .execute()
            )
            if not result.data:
                raise NotFoundError("Bulk deal")
            return result.data
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to fetch deal: {e!s}") from e

    def create(self, deal_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new bulk deal record."""
        try:
            result = self.table.insert(deal_data).execute()
            if not result.data:
                raise DatabaseError("Deal creation returned no data")
            return result.data[0]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to create deal: {e!s}") from e

    def bulk_insert(self, deals: list[dict[str, Any]]) -> dict[str, Any]:
        """Insert multiple deals at once. Returns count of inserted records."""
        if not deals:
            return {"inserted": 0, "deals": []}
        try:
            result = self.table.insert(deals).execute()
            return {
                "inserted": len(result.data) if result.data else 0,
                "deals": result.data or [],
            }
        except Exception as e:
            raise DatabaseError(f"Failed to bulk insert deals: {e!s}") from e

    def delete(self, deal_id: str) -> bool:
        """Delete a deal by ID."""
        try:
            result = self.table.delete().eq("id", deal_id).execute()
            return bool(result.data)
        except Exception as e:
            raise DatabaseError(f"Failed to delete deal: {e!s}") from e

    def get_stats(self) -> dict[str, Any]:
        """Get summary stats for bulk deals."""
        try:
            total_result = self.table.select("*", count="exact").execute()
            total = total_result.count if total_result.count is not None else 0

            buy_result = (
                self.table
                .select("*", count="exact")
                .eq("deal_type", "BUY")
                .execute()
            )
            buy_count = buy_result.count if buy_result.count is not None else 0

            sell_count = total - buy_count

            return {
                "total_deals": total,
                "buy_deals": buy_count,
                "sell_deals": sell_count,
            }
        except Exception as e:
            raise DatabaseError(f"Failed to get stats: {e!s}") from e
