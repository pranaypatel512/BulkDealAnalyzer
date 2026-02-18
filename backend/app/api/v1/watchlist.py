"""
Watchlist API

Endpoints for managing user watchlist (symbols to track).
"""

from fastapi import APIRouter, HTTPException

from app.core.auth import CurrentUser
from app.core.models import WatchlistAdd, WatchlistUpdate
from app.core.responses import success_response
from app.services.watchlist_service import WatchlistService

router = APIRouter()


def _get_service() -> WatchlistService:
    return WatchlistService()


@router.get("/")
async def list_watchlist(user: CurrentUser):
    """List current user's watchlist."""
    service = _get_service()
    items = service.list(user_id=str(user.id))
    return success_response(data=items, message="Watchlist retrieved")


@router.post("/")
async def add_to_watchlist(user: CurrentUser, body: WatchlistAdd):
    """Add a symbol to watchlist."""
    service = _get_service()
    try:
        item = service.add(
            user_id=str(user.id),
            symbol=body.symbol.strip().upper(),
            notes=body.notes,
            alert_on_buy=body.alert_on_buy,
            alert_on_sell=body.alert_on_sell,
            min_quantity=body.min_quantity,
            min_value=body.min_value,
        )
        return success_response(data=item, message="Added to watchlist")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{item_id}")
async def get_watchlist_item(item_id: str, user: CurrentUser):
    """Get a single watchlist item."""
    service = _get_service()
    item = service.get(user_id=str(user.id), item_id=item_id)
    return success_response(data=item, message="Watchlist item retrieved")


@router.patch("/{item_id}")
async def update_watchlist_item(item_id: str, user: CurrentUser, body: WatchlistUpdate):
    """Update a watchlist item."""
    service = _get_service()
    updates = body.model_dump(exclude_none=True)
    item = service.update(
        user_id=str(user.id),
        item_id=item_id,
        **updates,
    )
    return success_response(data=item, message="Watchlist item updated")


@router.delete("/{item_id}")
async def remove_from_watchlist(item_id: str, user: CurrentUser):
    """Remove a watchlist item by id."""
    service = _get_service()
    service.remove(user_id=str(user.id), item_id=item_id)
    return success_response(data=None, message="Removed from watchlist")
