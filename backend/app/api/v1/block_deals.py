"""
Block Deals Endpoints

API for block deals data from NSE India (large single trades).
"""

from datetime import date

from fastapi import APIRouter, Query
from fastapi.responses import Response

from app.core.auth import CurrentUser, OptionalUser
from app.core.csv_export import deals_to_csv
from app.core.responses import success_response
from app.services.block_deals_service import BlockDealsService
from app.services.nse_fetcher import NSEFetcher

router = APIRouter()


@router.get("/")
async def list_block_deals(
    _user: OptionalUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    symbol: str | None = Query(None),
    deal_type: str | None = Query(None, pattern="^(BUY|SELL)$"),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    sort_by: str = Query("date"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
):
    """List block deals with filtering and pagination."""
    service = BlockDealsService()
    result = service.list_deals(
        page=page,
        page_size=page_size,
        symbol=symbol,
        deal_type=deal_type,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return success_response(data=result, message="Block deals retrieved")

@router.get("/export-csv")
async def export_block_deals_csv(
    _user: OptionalUser,
    symbol: str | None = Query(None, description="Filter by symbol (partial match)"),
    deal_type: str | None = Query(None, pattern="^(BUY|SELL)$"),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    sort_by: str = Query("date"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    max_rows: int = Query(10_000, ge=1, le=50_000),
):
    """Export filtered block deals as CSV (raw CSV response)."""
    service = BlockDealsService()
    export_result = service.export_deals(
        symbol=symbol,
        deal_type=deal_type,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        sort_order=sort_order,
        max_rows=max_rows,
    )

    csv_text = deals_to_csv(export_result["deals"])
    filename = f"block-deals-{date.today().isoformat()}.csv"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "X-Export-Total": str(export_result.get("total") or 0),
        "X-Export-Truncated": "true" if export_result.get("truncated") else "false",
    }
    return Response(content=csv_text, media_type="text/csv; charset=utf-8", headers=headers)


@router.post("/fetch")
async def fetch_block_deals_from_nse(user: CurrentUser):
    """Fetch latest block deals from NSE and import."""
    fetcher = NSEFetcher()
    result = await fetcher.fetch_and_import_block_deals(user_id=str(user.id))
    return success_response(data=result, message=result.get("message", "Fetch complete"))
