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
        from app.core.database import get_supabase_admin_client, get_supabase_client

        try:
            self._client = get_supabase_admin_client()
        except ValueError:
            self._client = get_supabase_client()

    @property
    def table(self):
        return self._client.table(self.TABLE)

    @staticmethod
    def _empty_list(page: int = 1, page_size: int = 20) -> dict[str, Any]:
        """Return an empty paginated result."""
        return {
            "deals": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "total_pages": 0,
        }

    @staticmethod
    def _is_table_missing(error: Exception) -> bool:
        """Check if the error is due to the table not existing in Supabase."""
        msg = str(error)
        return "PGRST205" in msg or "schema cache" in msg

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
            if self._is_table_missing(e):
                return self._empty_list(page, page_size)
            raise DatabaseError(f"Failed to list deals: {e!s}") from e

    def export_deals(
        self,
        *,
        symbol: str | None = None,
        deal_type: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        sort_by: str = "date",
        sort_order: str = "desc",
        max_rows: int = 10_000,
        batch_size: int = 1_000,
    ) -> dict[str, Any]:
        """
        Export deals matching filters, fetching in batches until complete or max_rows is reached.

        Returns dict with deals, total count (if available), and whether results were truncated.
        """
        if max_rows <= 0:
            return {"deals": [], "total": 0, "truncated": False}

        page = 1
        collected: list[dict[str, Any]] = []
        total = 0
        truncated = False

        while True:
            result = self.list_deals(
                page=page,
                page_size=batch_size,
                symbol=symbol,
                deal_type=deal_type,
                date_from=date_from,
                date_to=date_to,
                sort_by=sort_by,
                sort_order=sort_order,
            )

            if page == 1:
                total = int(result.get("total") or 0)

            deals = result.get("deals") or []
            if not deals:
                break

            remaining = max_rows - len(collected)
            if remaining <= 0:
                truncated = True
                break

            collected.extend(deals[:remaining])

            if len(collected) >= max_rows:
                truncated = total > max_rows if total else True
                break

            total_pages = int(result.get("total_pages") or 0)
            if total_pages and page >= total_pages:
                break

            page += 1

        return {"deals": collected, "total": total, "truncated": truncated}

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
            if result is None or not result.data:
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
            if self._is_table_missing(e):
                return {"total_deals": 0, "buy_deals": 0, "sell_deals": 0}
            raise DatabaseError(f"Failed to get stats: {e!s}") from e

    def get_top_symbols(
        self,
        *,
        limit: int = 10,
        deal_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get top symbols by deal volume."""
        try:
            query = self.table.select("symbol,quantity,deal_type")
            if deal_type:
                query = query.eq("deal_type", deal_type.upper())
            result = query.execute()

            if not result.data:
                return []

            totals: dict[str, dict[str, Any]] = {}
            for row in result.data:
                sym = row["symbol"]
                if sym not in totals:
                    totals[sym] = {
                        "symbol": sym,
                        "total_quantity": 0,
                        "deal_count": 0,
                        "buy_count": 0,
                        "sell_count": 0,
                    }
                totals[sym]["total_quantity"] += row.get("quantity", 0)
                totals[sym]["deal_count"] += 1
                if row.get("deal_type") == "BUY":
                    totals[sym]["buy_count"] += 1
                else:
                    totals[sym]["sell_count"] += 1

            ranked = sorted(
                totals.values(),
                key=lambda x: x["deal_count"],
                reverse=True,
            )
            return ranked[:limit]
        except Exception as e:
            if self._is_table_missing(e):
                return []
            raise DatabaseError(
                f"Failed to get top symbols: {e!s}",
            ) from e

    def get_daily_trend(
        self,
        *,
        days: int = 30,
    ) -> list[dict[str, Any]]:
        """Get daily deal counts and volume for trending chart."""
        try:
            from datetime import datetime, timedelta

            end = datetime.now()
            start = end - timedelta(days=days)
            start_str = start.strftime("%Y-%m-%d")

            result = (
                self.table
                .select("date,deal_type,quantity,price")
                .gte("date", start_str)
                .order("date", desc=False)
                .execute()
            )

            if not result.data:
                return []

            daily: dict[str, dict[str, Any]] = {}
            for row in result.data:
                dt = row["date"]
                if dt not in daily:
                    daily[dt] = {
                        "date": dt,
                        "total_deals": 0,
                        "buy_deals": 0,
                        "sell_deals": 0,
                        "total_quantity": 0,
                        "total_value": 0.0,
                    }
                daily[dt]["total_deals"] += 1
                qty = row.get("quantity", 0)
                price = row.get("price", 0)
                daily[dt]["total_quantity"] += qty
                daily[dt]["total_value"] += qty * price
                if row.get("deal_type") == "BUY":
                    daily[dt]["buy_deals"] += 1
                else:
                    daily[dt]["sell_deals"] += 1

            return sorted(
                daily.values(),
                key=lambda x: x["date"],
            )
        except Exception as e:
            if self._is_table_missing(e):
                return []
            raise DatabaseError(
                f"Failed to get daily trend: {e!s}",
            ) from e

    def get_price_distribution(self) -> list[dict[str, Any]]:
        """Get price range distribution for histogram."""
        try:
            result = self.table.select("price").execute()
            if not result.data:
                return []

            prices = [r["price"] for r in result.data if r.get("price")]
            if not prices:
                return []

            buckets = [
                ("0-50", 0, 50),
                ("50-100", 50, 100),
                ("100-500", 100, 500),
                ("500-1000", 500, 1000),
                ("1000-2500", 1000, 2500),
                ("2500-5000", 2500, 5000),
                ("5000+", 5000, float("inf")),
            ]

            distribution = []
            for label, low, high in buckets:
                count = sum(1 for p in prices if low <= p < high)
                distribution.append({"range": label, "count": count})
            return distribution
        except Exception as e:
            if self._is_table_missing(e):
                return []
            raise DatabaseError(
                f"Failed to get price distribution: {e!s}",
            ) from e
