"""
Bulk Deals Endpoints

API endpoints for querying and managing bulk deals data.
"""

from fastapi import APIRouter, Query

from app.core.auth import CurrentUser, OptionalUser
from app.core.parser import parse_csv_content
from app.core.responses import success_response
from app.services.bulk_deals_service import BulkDealsService

router = APIRouter()


def _get_service() -> BulkDealsService:
    return BulkDealsService()


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


@router.get("/stats")
async def get_deal_stats(_user: OptionalUser):
    """Get summary statistics for bulk deals."""
    service = _get_service()
    stats = service.get_stats()
    return success_response(data=stats, message="Deal statistics retrieved")


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
