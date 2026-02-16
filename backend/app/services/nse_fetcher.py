"""
NSE Bulk Deals Fetcher

Fetches bulk deals data from NSE India website and imports into the database.
Uses session-based cookies to authenticate with NSE's API.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.exceptions import DatabaseError
from app.core.parser import parse_csv_content

logger = logging.getLogger(__name__)

NSE_BASE_URL = "https://www.nseindia.com"
NSE_BULK_DEALS_API = f"{NSE_BASE_URL}/api/snapshot-capital-market-largedeal"

NSE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": f"{NSE_BASE_URL}/report-detail/display-bulk-and-block-deals",
}


class NSEFetcher:
    """Fetches bulk deals from NSE India and imports into the database."""

    def __init__(self) -> None:
        from app.core.database import get_supabase_admin_client, get_supabase_client

        try:
            self._client = get_supabase_admin_client()
        except ValueError:
            self._client = get_supabase_client()

    @property
    def deals_table(self):
        return self._client.table("bulk_deals")

    @property
    def history_table(self):
        return self._client.table("fetch_history")

    async def _get_nse_session(self) -> httpx.AsyncClient:
        """Create an httpx session with NSE cookies."""
        client = httpx.AsyncClient(
            headers=NSE_HEADERS,
            follow_redirects=True,
            timeout=30.0,
        )
        # Visit NSE homepage first to get session cookies
        try:
            await client.get(NSE_BASE_URL)
        except httpx.HTTPError:
            logger.warning("Failed to initialize NSE session from homepage")
        return client

    async def fetch_bulk_deals_json(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch bulk deals from NSE API as JSON.

        The NSE snapshot API returns today's bulk deals.
        For historical data, use the archives endpoint.
        """
        client = await self._get_nse_session()
        try:
            # Try the snapshot API first (today's data)
            resp = await client.get(
                NSE_BULK_DEALS_API,
                headers={"Accept": "application/json"},
            )
            resp.raise_for_status()
            data = resp.json()

            # NSE returns {"BLOCK_DEALS_DATA": [...], "BULK_DEALS_DATA": [...]}
            bulk_deals = data.get("BULK_DEALS_DATA", [])
            logger.info("Fetched %d bulk deals from NSE snapshot API", len(bulk_deals))
            return bulk_deals
        except httpx.HTTPStatusError as e:
            logger.error("NSE API HTTP error %s: %s", e.response.status_code, e)
            raise
        except Exception as e:
            logger.error("NSE API error: %s", e)
            raise
        finally:
            await client.aclose()

    def _nse_json_to_csv(self, deals: list[dict[str, Any]]) -> str:
        """
        Convert NSE JSON response to CSV format compatible with our parser.

        NSE JSON fields: BD_DT_DATE, BD_SYMBOL, BD_SCRIP_NAME,
                         BD_CLIENT_NAME, BD_BUY_SELL, BD_QTY_TRD, BD_TP_WATP,
                         BD_REMARKS
        """
        if not deals:
            return ""

        lines = [
            "Date,Symbol,Security Name,Client Name,"
            "Buy/Sell,Quantity Traded,Trade Price,Remarks"
        ]
        for deal in deals:
            date_str = deal.get("BD_DT_DATE", deal.get("mTIMESTAMP", ""))
            symbol = deal.get("BD_SYMBOL", "")
            security_name = deal.get("BD_SCRIP_NAME", "")
            client_name = deal.get("BD_CLIENT_NAME", "")
            buy_sell = deal.get("BD_BUY_SELL", "")
            quantity = deal.get("BD_QTY_TRD", "0")
            price = deal.get("BD_TP_WATP", "0")
            remarks = deal.get("BD_REMARKS", "")

            # Escape commas in fields
            def esc(v: Any) -> str:
                s = str(v).strip()
                return f'"{s}"' if "," in s else s

            lines.append(
                f"{esc(date_str)},{esc(symbol)},{esc(security_name)},"
                f"{esc(client_name)},{esc(buy_sell)},{esc(quantity)},"
                f"{esc(price)},{esc(remarks)}"
            )
        return "\n".join(lines)

    def _get_existing_keys(
        self,
        date_str: str,
        symbols: list[str],
    ) -> set[str]:
        """
        Get existing deal keys for dedup.

        Key = date|symbol|client_name|deal_type|quantity
        """
        if not symbols:
            return set()

        try:
            result = (
                self.deals_table
                .select("date,symbol,client_name,deal_type,quantity")
                .eq("date", date_str)
                .in_("symbol", symbols)
                .execute()
            )
            if result is None or not result.data:
                return set()
            return {
                f"{r['date']}|{r['symbol']}|{r['client_name']}|{r['deal_type']}|{r['quantity']}"
                for r in result.data
            }
        except Exception as e:
            logger.warning("Failed to check existing deals: %s", e)
            return set()

    def _dedup_deals(
        self,
        deals_data: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Remove deals that already exist in the database."""
        if not deals_data:
            return []

        # Group by date for efficient querying
        dates = {d["date"] for d in deals_data}
        symbols = list({d["symbol"] for d in deals_data})

        existing_keys: set[str] = set()
        for date_str in dates:
            existing_keys |= self._get_existing_keys(date_str, symbols)

        new_deals = []
        for deal in deals_data:
            key = (
                f"{deal['date']}|{deal['symbol']}|{deal['client_name']}"
                f"|{deal['deal_type']}|{deal['quantity']}"
            )
            if key not in existing_keys:
                new_deals.append(deal)

        dupes = len(deals_data) - len(new_deals)
        if dupes > 0:
            logger.info("Dedup: skipped %d existing deals, %d new", dupes, len(new_deals))
        return new_deals

    def _record_fetch(
        self,
        *,
        source: str,
        status: str,
        deals_fetched: int = 0,
        deals_imported: int = 0,
        deals_skipped: int = 0,
        error_message: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> None:
        """Record a fetch attempt in the fetch_history table."""
        record = {
            "source": source,
            "status": status,
            "deals_fetched": deals_fetched,
            "deals_imported": deals_imported,
            "deals_skipped": deals_skipped,
            "error_message": error_message,
            "date_from": date_from,
            "date_to": date_to,
        }
        try:
            self.history_table.insert(record).execute()
        except Exception as e:
            logger.warning("Failed to record fetch history: %s", e)

    async def fetch_and_import(
        self,
        *,
        user_id: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict[str, Any]:
        """
        Fetch bulk deals from NSE and import into the database.

        Returns summary of the fetch operation.
        """
        source = "nse_api"
        try:
            # Step 1: Fetch from NSE
            raw_deals = await self.fetch_bulk_deals_json(
                date_from=date_from,
                date_to=date_to,
            )
            if not raw_deals:
                self._record_fetch(
                    source=source,
                    status="success",
                    deals_fetched=0,
                    date_from=date_from,
                    date_to=date_to,
                )
                return {
                    "status": "success",
                    "fetched": 0,
                    "imported": 0,
                    "skipped": 0,
                    "errors": [],
                    "message": "No bulk deals found for the requested period",
                }

            # Step 2: Convert to CSV and parse
            csv_content = self._nse_json_to_csv(raw_deals)
            parse_result = parse_csv_content(csv_content)

            if not parse_result.deals:
                self._record_fetch(
                    source=source,
                    status="success",
                    deals_fetched=len(raw_deals),
                    deals_imported=0,
                    error_message="; ".join(parse_result.errors) if parse_result.errors else None,
                    date_from=date_from,
                    date_to=date_to,
                )
                return {
                    "status": "success",
                    "fetched": len(raw_deals),
                    "imported": 0,
                    "skipped": 0,
                    "errors": parse_result.errors,
                    "message": "Fetched data but no valid deals to import",
                }

            # Step 3: Prepare deal records
            deals_data = [
                {
                    "date": deal.date.strftime("%Y-%m-%d"),
                    "symbol": deal.symbol,
                    "security_name": deal.security_name,
                    "client_name": deal.client_name,
                    "deal_type": deal.deal_type,
                    "quantity": deal.quantity,
                    "price": float(deal.price),
                    "remarks": deal.remarks,
                    **({"user_id": user_id} if user_id else {}),
                }
                for deal in parse_result.deals
            ]

            # Step 4: Dedup
            new_deals = self._dedup_deals(deals_data)
            skipped = len(deals_data) - len(new_deals)

            # Step 5: Bulk insert
            imported = 0
            if new_deals:
                try:
                    result = self.deals_table.insert(new_deals).execute()
                    imported = len(result.data) if result and result.data else 0
                except Exception as e:
                    logger.error("Bulk insert failed: %s", e)
                    self._record_fetch(
                        source=source,
                        status="error",
                        deals_fetched=len(raw_deals),
                        error_message=str(e),
                        date_from=date_from,
                        date_to=date_to,
                    )
                    raise DatabaseError(f"Failed to import deals: {e!s}") from e

            # Step 6: Record success
            self._record_fetch(
                source=source,
                status="success",
                deals_fetched=len(raw_deals),
                deals_imported=imported,
                deals_skipped=skipped,
                date_from=date_from,
                date_to=date_to,
            )

            return {
                "status": "success",
                "fetched": len(raw_deals),
                "imported": imported,
                "skipped": skipped,
                "errors": parse_result.errors,
                "message": f"Imported {imported} deals ({skipped} duplicates skipped)",
            }

        except DatabaseError:
            raise
        except Exception as e:
            self._record_fetch(
                source=source,
                status="error",
                error_message=str(e),
                date_from=date_from,
                date_to=date_to,
            )
            return {
                "status": "error",
                "fetched": 0,
                "imported": 0,
                "skipped": 0,
                "errors": [str(e)],
                "message": f"Failed to fetch from NSE: {e!s}",
            }

    def import_from_csv(
        self,
        csv_content: str,
        *,
        user_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Import bulk deals from raw CSV content (manual upload fallback).

        Parses the CSV, deduplicates, and inserts new deals.
        """
        source = "csv_upload"
        try:
            parse_result = parse_csv_content(csv_content)

            if not parse_result.deals:
                self._record_fetch(
                    source=source,
                    status="success",
                    deals_fetched=parse_result.total_rows,
                    deals_imported=0,
                    error_message="; ".join(parse_result.errors) if parse_result.errors else None,
                )
                return {
                    "status": "success",
                    "fetched": parse_result.total_rows,
                    "imported": 0,
                    "skipped": 0,
                    "errors": parse_result.errors,
                    "message": "No valid deals found in CSV",
                }

            deals_data = [
                {
                    "date": deal.date.strftime("%Y-%m-%d"),
                    "symbol": deal.symbol,
                    "security_name": deal.security_name,
                    "client_name": deal.client_name,
                    "deal_type": deal.deal_type,
                    "quantity": deal.quantity,
                    "price": float(deal.price),
                    "remarks": deal.remarks,
                    **({"user_id": user_id} if user_id else {}),
                }
                for deal in parse_result.deals
            ]

            new_deals = self._dedup_deals(deals_data)
            skipped = len(deals_data) - len(new_deals)

            imported = 0
            if new_deals:
                result = self.deals_table.insert(new_deals).execute()
                imported = len(result.data) if result and result.data else 0

            self._record_fetch(
                source=source,
                status="success",
                deals_fetched=parse_result.total_rows,
                deals_imported=imported,
                deals_skipped=skipped,
            )

            return {
                "status": "success",
                "fetched": parse_result.valid_rows,
                "imported": imported,
                "skipped": skipped,
                "errors": parse_result.errors,
                "message": f"Imported {imported} deals ({skipped} duplicates skipped)",
            }

        except Exception as e:
            self._record_fetch(
                source=source,
                status="error",
                error_message=str(e),
            )
            raise DatabaseError(f"CSV import failed: {e!s}") from e

    def get_fetch_history(
        self,
        *,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Get recent fetch history records."""
        try:
            result = (
                self.history_table
                .select("*")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            if result is None:
                return []
            return result.data or []
        except Exception as e:
            logger.warning("Failed to fetch history: %s", e)
            return []

    def get_last_fetch(self) -> dict[str, Any] | None:
        """Get the most recent successful fetch."""
        try:
            result = (
                self.history_table
                .select("*")
                .eq("status", "success")
                .order("created_at", desc=True)
                .limit(1)
                .maybe_single()
                .execute()
            )
            if result is None:
                return None
            return result.data
        except Exception:
            return None
