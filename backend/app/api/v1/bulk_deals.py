"""
Bulk Deals Endpoints

API endpoints for querying and managing bulk deals data.
"""

from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi.responses import Response

from app.core.auth import CurrentUser, OptionalUser
from app.core.csv_export import deals_to_csv
from app.core.parser import parse_csv_content
from app.core.responses import success_response
from app.services.bulk_deals_service import BulkDealsService
from app.services.nse_fetcher import NSEFetcher

router = APIRouter()


def _get_service() -> BulkDealsService:
    return BulkDealsService()


def _get_fetcher() -> NSEFetcher:
    return NSEFetcher()


@router.get("/")
async def list_bulk_deals(
    _user: OptionalUser,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    symbol: str | None = Query(None, description="Filter by symbol (partial match)"),
    deal_type: str | None = Query(
        None, pattern="^(BUY|SELL)$", description="Filter by BUY or SELL",
    ),
    date_from: str | None = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: str | None = Query(None, description="Filter to date (YYYY-MM-DD)"),
    sort_by: str = Query("date", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
):
    """
    List bulk deals with filtering, sorting, and pagination.

    Works for both authenticated and anonymous users.
    """
    service = _get_service()
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
    return success_response(data=result, message="Bulk deals retrieved")

@router.get("/export-csv")
async def export_bulk_deals_csv(
    _user: OptionalUser,
    symbol: str | None = Query(None, description="Filter by symbol (partial match)"),
    deal_type: str | None = Query(
        None, pattern="^(BUY|SELL)$", description="Filter by BUY or SELL",
    ),
    date_from: str | None = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: str | None = Query(None, description="Filter to date (YYYY-MM-DD)"),
    sort_by: str = Query("date", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    max_rows: int = Query(10_000, ge=1, le=50_000, description="Max rows to export"),
):
    """
    Export filtered bulk deals as CSV.

    Returns raw CSV (not wrapped in the standard JSON envelope).
    """
    service = _get_service()
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
    filename = f"bulk-deals-{date.today().isoformat()}.csv"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "X-Export-Total": str(export_result.get("total") or 0),
        "X-Export-Truncated": "true" if export_result.get("truncated") else "false",
    }
    return Response(content=csv_text, media_type="text/csv; charset=utf-8", headers=headers)


@router.get("/stats")
async def get_deal_stats(_user: OptionalUser):
    """Get summary statistics for bulk deals."""
    service = _get_service()
    stats = service.get_stats()
    return success_response(data=stats, message="Deal statistics retrieved")


@router.get("/fetch-history")
async def get_fetch_history(
    _user: OptionalUser,
    limit: int = Query(20, ge=1, le=100, description="Number of records"),
):
    """Get recent data fetch history."""
    fetcher = _get_fetcher()
    history = fetcher.get_fetch_history(limit=limit)
    return success_response(data=history, message="Fetch history retrieved")


@router.get("/analytics/top-symbols")
async def get_top_symbols(
    _user: OptionalUser,
    limit: int = Query(10, ge=1, le=50, description="Number of symbols"),
    deal_type: str | None = Query(
        None,
        pattern="^(BUY|SELL)$",
        description="Filter by BUY or SELL",
    ),
):
    """Get top symbols by deal volume for bar chart."""
    service = _get_service()
    data = service.get_top_symbols(limit=limit, deal_type=deal_type)
    return success_response(
        data=data,
        message="Top symbols retrieved",
    )


@router.get("/analytics/daily-trend")
async def get_daily_trend(
    _user: OptionalUser,
    days: int = Query(30, ge=1, le=365, description="Number of days"),
):
    """Get daily deal trend for line/area chart."""
    service = _get_service()
    data = service.get_daily_trend(days=days)
    return success_response(
        data=data,
        message="Daily trend retrieved",
    )


@router.get("/analytics/price-distribution")
async def get_price_distribution(_user: OptionalUser):
    """Get price range distribution for histogram."""
    service = _get_service()
    data = service.get_price_distribution()
    return success_response(
        data=data,
        message="Price distribution retrieved",
    )


@router.get("/{deal_id}")
async def get_bulk_deal(deal_id: str, _user: OptionalUser):
    """Get a specific bulk deal by ID."""
    service = _get_service()
    deal = service.get_by_id(deal_id)
    return success_response(data=deal, message="Bulk deal retrieved")


@router.post("/parse")
async def parse_deals_csv(user: CurrentUser, csv_content: str):
    """
    Parse CSV content and return parsed deals (without storing).

    Requires authentication. Useful for previewing data before import.
    """
    result = parse_csv_content(csv_content)
    return success_response(
        data={
            "deals": [deal.model_dump(mode="json") for deal in result.deals],
            "total_rows": result.total_rows,
            "valid_rows": result.valid_rows,
            "invalid_rows": result.invalid_rows,
            "errors": result.errors,
        },
        message=f"Parsed {result.valid_rows} valid deals from {result.total_rows} rows",
    )


@router.post("/import")
async def import_deals(user: CurrentUser, csv_content: str):
    """
    Parse CSV content and import valid deals into the database.

    Requires authentication. Deals are associated with the authenticated user.
    """
    result = parse_csv_content(csv_content)
    if not result.deals:
        return success_response(
            data={
                "imported": 0,
                "errors": result.errors,
            },
            message="No valid deals to import",
        )

    service = _get_service()
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
            "user_id": str(user.id),
        }
        for deal in result.deals
    ]

    insert_result = service.bulk_insert(deals_data)
    return success_response(
        data={
            "imported": insert_result["inserted"],
            "total_parsed": result.valid_rows,
            "parse_errors": result.errors,
        },
        message=f"Imported {insert_result['inserted']} deals",
    )


@router.post("/fetch")
async def fetch_from_nse(user: CurrentUser):
    """
    Fetch latest bulk deals from NSE India and import into the database.

    Requires authentication. Fetches today's bulk deals from the NSE
    snapshot API, deduplicates against existing data, and imports new deals.
    """
    fetcher = _get_fetcher()
    result = await fetcher.fetch_and_import(user_id=str(user.id))
    return success_response(data=result, message=result.get("message", "Fetch complete"))


@router.post("/upload-csv")
async def upload_csv(user: CurrentUser, csv_content: str = Body(..., embed=True)):
    """
    Upload CSV content and import deals with deduplication.

    Unlike /import, this endpoint deduplicates against existing database
    records before inserting.
    """
    fetcher = _get_fetcher()
    result = fetcher.import_from_csv(csv_content, user_id=str(user.id))
    return success_response(data=result, message=result.get("message", "Import complete"))
