"""
NSE Bulk Deals Fetcher

Fetches bulk deals data from NSE India website and imports into the database.
Uses session-based cookies to authenticate with NSE's API.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import httpx

from app.core.exceptions import DatabaseError
from app.core.parser import parse_csv_content

logger = logging.getLogger(__name__)

NSE_BASE_URL = "https://www.nseindia.com"
NSE_BULK_DEALS_API = f"{NSE_BASE_URL}/api/snapshot-capital-market-largedeal"
# Same API returns BULK_DEALS_DATA, BLOCK_DEALS_DATA; short selling may use mode=short_deals

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
    def block_deals_table(self):
        return self._client.table("block_deals")

    @property
    def short_selling_table(self):
        return self._client.table("short_selling_deals")

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

    async def _fetch_largedeal_snapshot(
        self,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Fetch the full snapshot from NSE largedeal API.
        Returns dict with keys BULK_DEALS_DATA, BLOCK_DEALS_DATA, and possibly SHORT_SELLING_DATA.
        """
        client = await self._get_nse_session()
        try:
            url = NSE_BULK_DEALS_API
            if mode:
                url = f"{url}?mode={mode}"
            resp = await client.get(url, headers={"Accept": "application/json"})
            resp.raise_for_status()
            return resp.json()
        finally:
            await client.aclose()

    async def fetch_bulk_deals_json(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch bulk deals from NSE API as JSON.
        The NSE snapshot API returns today's bulk deals.
        """
        data = await self._fetch_largedeal_snapshot()
        bulk_deals = data.get("BULK_DEALS_DATA", [])
        logger.info("Fetched %d bulk deals from NSE snapshot API", len(bulk_deals))
        return bulk_deals

    async def fetch_block_deals_json(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch block deals from NSE API as JSON.
        Same snapshot endpoint returns BLOCK_DEALS_DATA.
        """
        data = await self._fetch_largedeal_snapshot()
        block_deals = data.get("BLOCK_DEALS_DATA", [])
        logger.info("Fetched %d block deals from NSE snapshot API", len(block_deals))
        return block_deals

    async def fetch_short_selling_json(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch short selling / short deals from NSE API.
        Tries SHORT_SELLING_DATA from same snapshot, then mode=short_deals if needed.
        """
        data = await self._fetch_largedeal_snapshot()
        short_deals = data.get("SHORT_SELLING_DATA", data.get("SHORT_DEALS_DATA", []))
        if not short_deals:
            try:
                data2 = await self._fetch_largedeal_snapshot(mode="short_deals")
                short_deals = (
                    data2.get("SHORT_SELLING_DATA")
                    or data2.get("SHORT_DEALS_DATA")
                    or data2.get("data", [])
                    or []
                )
            except Exception as e:
                logger.debug("NSE short_deals mode fallback: %s", e)
        logger.info("Fetched %d short selling deals from NSE", len(short_deals))
        return short_deals

    @staticmethod
    def _normalize_nse_date(date_str: str) -> str:
        """Convert date to dd-Mon-yyyy format expected by parser."""
        date_str = date_str.strip()
        if not date_str:
            return date_str
        try:
            # Already dd-Mon-yyyy (e.g. 16-Feb-2026)
            if len(date_str) >= 11 and "-" in date_str and date_str[2] == "-":
                datetime.strptime(date_str[:11], "%d-%b-%Y")
                return date_str[:11]
        except ValueError:
            pass
        try:
            # ISO yyyy-mm-dd
            dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
            return dt.strftime("%d-%b-%Y")
        except ValueError:
            pass
        try:
            # dd/mm/yyyy
            dt = datetime.strptime(date_str[:10], "%d/%m/%Y")
            return dt.strftime("%d-%b-%Y")
        except ValueError:
            pass
        return date_str

    @staticmethod
    def _get_nse_field(deal: dict[str, Any], *keys: str, default: str = "") -> str:
        """Get first present key from deal, with optional default."""
        for key in keys:
            if key in deal and deal[key] is not None:
                v = str(deal[key]).strip()
                if v:
                    return v
        return default

    @staticmethod
    def _normalize_key(key: str) -> str:
        """Normalize dict keys for case/format-insensitive matching."""
        return "".join(ch for ch in key.lower() if ch.isalnum())

    @classmethod
    def _get_nse_field_ci(
        cls,
        deal: dict[str, Any],
        *normalized_keys: str,
        default: str = "",
    ) -> str:
        """
        Case/format-insensitive field lookup.

        Useful when NSE response keys vary by endpoint/version (e.g. SYMBOL vs symbol).
        `normalized_keys` should be pre-normalized (lowercase, alnum only).
        """
        if not deal:
            return default
        lookup = {cls._normalize_key(k): k for k in deal.keys()}
        for nk in normalized_keys:
            k = lookup.get(nk)
            if not k:
                continue
            v = deal.get(k)
            if v is None:
                continue
            s = str(v).strip()
            if s:
                return s
        return default

    @staticmethod
    def _get_nse_number(deal: dict[str, Any], *keys: str, default: int | float = 0) -> int | float:
        """Get first present numeric key from deal."""
        for key in keys:
            if key in deal and deal[key] is not None:
                try:
                    v = deal[key]
                    if isinstance(v, (int, float)):
                        return v
                    s = str(v).strip().replace(",", "")
                    return float(s) if "." in s else int(float(s))
                except (ValueError, TypeError):
                    pass
        return default

    @classmethod
    def _get_nse_number_ci(
        cls,
        deal: dict[str, Any],
        *normalized_keys: str,
        default: int | float = 0,
    ) -> int | float:
        """Case/format-insensitive numeric lookup for variable NSE key names."""
        if not deal:
            return default
        lookup = {cls._normalize_key(k): k for k in deal.keys()}
        for nk in normalized_keys:
            k = lookup.get(nk)
            if not k:
                continue
            v = deal.get(k)
            if v is None:
                continue
            try:
                if isinstance(v, (int, float)):
                    return v
                s = str(v).strip().replace(",", "")
                return float(s) if "." in s else int(float(s))
            except (ValueError, TypeError):
                continue
        return default

    def _nse_json_to_csv(self, deals: list[dict[str, Any]]) -> str:
        """
        Convert NSE JSON response to CSV format compatible with our parser.

        Supports multiple NSE response shapes:
        - BD_* (e.g. BD_DT_DATE, BD_SYMBOL, BD_CLIENT_NAME, BD_BUY_SELL, BD_QTY_TRD, BD_TP_WATP)
        - camelCase (e.g. date, symbol, clientName, buySell, qty, watp)
        - name for security name
        Skips rows missing required fields so parser only sees valid rows.
        """
        if not deals:
            return ""

        header = (
            "Date,Symbol,Security Name,Client Name,"
            "Buy/Sell,Quantity Traded,Trade Price,Remarks"
        )
        lines = [header]

        for deal in deals:
            date_str = self._get_nse_field(
                deal, "BD_DT_DATE", "mTIMESTAMP", "date", "tradeDate",
            )
            if not date_str:
                date_str = self._get_nse_field_ci(
                    deal,
                    "date",
                    "tradedate",
                    "tradedt",
                    "trddate",
                    "bddtdate",
                    "mtimestamp",
                    default="",
                )
            symbol = self._get_nse_field(deal, "BD_SYMBOL", "symbol", "sym")
            if not symbol:
                symbol = self._get_nse_field_ci(
                    deal,
                    "symbol",
                    "sym",
                    "tradingsymbol",
                    "securitysymbol",
                    default="",
                )
            security_name = self._get_nse_field(
                deal, "BD_SCRIP_NAME", "name", "securityName", "companyName",
            )
            if not security_name:
                security_name = self._get_nse_field_ci(
                    deal,
                    "securityname",
                    "companyname",
                    "scripname",
                    "security",
                    default="",
                )
            client_name = self._get_nse_field(
                deal, "BD_CLIENT_NAME", "clientName", "client_name",
            )
            if not client_name:
                client_name = self._get_nse_field_ci(
                    deal,
                    "clientname",
                    "client",
                    "participantname",
                    "participant",
                    "membername",
                    "member",
                    default="",
                )
            buy_sell_raw = self._get_nse_field(
                deal, "BD_BUY_SELL", "buySell", "deal_type", "buy_sell",
            )
            if not buy_sell_raw:
                buy_sell_raw = self._get_nse_field_ci(
                    deal,
                    "buysell",
                    "buyorsell",
                    "dealtype",
                    "tradetype",
                    default="",
                )
            quantity = self._get_nse_number(
                deal, "BD_QTY_TRD", "qty", "quantity", "quantityTraded",
                default=0,
            )
            if not quantity:
                quantity = self._get_nse_number_ci(
                    deal,
                    "qty",
                    "quantity",
                    "quantitytraded",
                    "qtytrd",
                    "bdqtytrd",
                    "shortqty",
                    default=0,
                )
            price = self._get_nse_number(
                deal,
                "BD_TP_WATP",
                "watp",
                "price",
                "tradePrice",
                "avgPrice",
                "averagePrice",
                "WAP",
                "wap",
                "lastPrice",
                "closePrice",
                default=0.0,
            )
            if not price:
                price = self._get_nse_number_ci(
                    deal,
                    "price",
                    "tradeprice",
                    "watp",
                    "wap",
                    "avgprice",
                    "averageprice",
                    "lastprice",
                    "closeprice",
                    default=0.0,
                )
            remarks = self._get_nse_field(
                deal, "BD_REMARKS", "remarks",
            )

            # Normalize buy/sell to BUY or SELL
            buy_sell = buy_sell_raw.upper() if buy_sell_raw else ""
            if buy_sell in ("B", "BUY", "BOUGHT"):
                buy_sell = "BUY"
            elif buy_sell in ("S", "SELL", "SOLD"):
                buy_sell = "SELL"

            # Skip rows missing required fields (avoid parser validation errors)
            if not date_str or not symbol or not client_name or buy_sell not in ("BUY", "SELL"):
                continue
            # Require positive quantity and price; skip otherwise so parser never sees invalid rows
            if not (quantity > 0 and price > 0):
                continue

            # Normalize date to dd-Mon-yyyy for parser (e.g. 2026-02-16 -> 16-Feb-2026)
            date_str = self._normalize_nse_date(date_str)

            def esc(v: Any) -> str:
                s = str(v).strip()
                return f'"{s}"' if s and "," in s else s

            lines.append(
                f"{esc(date_str)},{esc(symbol)},{esc(security_name)},"
                f"{esc(client_name)},{esc(buy_sell)},{int(quantity)},"
                f"{float(price)},{esc(remarks)}"
            )

        if len(lines) == 1 and deals:
            # No valid rows; log first deal keys to help debug API shape
            logger.debug(
                "NSE API sample keys (no valid rows): %s",
                list(deals[0].keys()) if deals else [],
            )
        return "\n".join(lines)

    def _get_existing_keys(
        self,
        date_str: str,
        symbols: list[str],
        table=None,
    ) -> set[str]:
        """
        Get existing deal keys for dedup.
        Key = date|symbol|client_name|deal_type|quantity
        """
        if not symbols:
            return set()
        tbl = table if table is not None else self.deals_table
        try:
            result = (
                tbl.select("date,symbol,client_name,deal_type,quantity")
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
        table=None,
    ) -> list[dict[str, Any]]:
        """Remove deals that already exist in the database (for given table)."""
        if not deals_data:
            return []
        tbl = table if table is not None else self.deals_table
        dates = {d["date"] for d in deals_data}
        symbols = list({d["symbol"] for d in deals_data})
        existing_keys: set[str] = set()
        for date_str in dates:
            existing_keys |= self._get_existing_keys(date_str, symbols, table=tbl)

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

    async def _fetch_and_import_for_table(
        self,
        table,
        fetch_method,
        user_id: str | None,
        date_from: str | None,
        date_to: str | None,
        source_label: str,
    ) -> dict[str, Any]:
        """Common flow: fetch JSON, parse, dedup, insert into given table."""
        try:
            raw_deals = await fetch_method(date_from=date_from, date_to=date_to)
            if not raw_deals:
                self._record_fetch(
                    source=source_label,
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
                    "message": f"No {source_label} found for the requested period",
                }
            csv_content = self._nse_json_to_csv(raw_deals)
            parse_result = parse_csv_content(csv_content)
            if not parse_result.deals:
                self._record_fetch(
                    source=source_label,
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
            new_deals = self._dedup_deals(deals_data, table=table)
            skipped = len(deals_data) - len(new_deals)
            imported = 0
            if new_deals:
                try:
                    result = table.insert(new_deals).execute()
                    imported = len(result.data) if result and result.data else 0
                except Exception as e:
                    logger.error("Bulk insert failed: %s", e)
                    self._record_fetch(
                        source=source_label,
                        status="error",
                        deals_fetched=len(raw_deals),
                        error_message=str(e),
                        date_from=date_from,
                        date_to=date_to,
                    )
                    raise DatabaseError(f"Failed to import deals: {e!s}") from e
            self._record_fetch(
                source=source_label,
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
                source=source_label,
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

    async def fetch_and_import_block_deals(
        self,
        user_id: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict[str, Any]:
        """Fetch block deals from NSE and import into block_deals table."""
        return await self._fetch_and_import_for_table(
            table=self.block_deals_table,
            fetch_method=self.fetch_block_deals_json,
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            source_label="nse_block_deals",
        )

    async def fetch_and_import_short_selling(
        self,
        user_id: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict[str, Any]:
        """Fetch short selling data from NSE and import into short_selling_deals table."""
        return await self._fetch_and_import_for_table(
            table=self.short_selling_table,
            fetch_method=self.fetch_short_selling_json,
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            source_label="nse_short_selling",
        )

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
