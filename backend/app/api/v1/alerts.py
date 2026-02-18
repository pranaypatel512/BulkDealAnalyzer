"""
Alerts API

Endpoints for listing and managing user alerts.
"""

from fastapi import APIRouter

from app.core.auth import CurrentUser
from app.core.responses import success_response
from app.services.alerts_service import AlertsService

router = APIRouter()


def _get_service() -> AlertsService:
    return AlertsService()


@router.get("/unread-count")
async def unread_count(user: CurrentUser):
    """Get count of unread alerts."""
    service = _get_service()
    count = service.unread_count(user_id=str(user.id))
    return success_response(data={"count": count}, message="Unread count")


@router.get("/")
async def list_alerts(
    user: CurrentUser,
    limit: int = 50,
    is_read: bool | None = None,
):
    """List current user's alerts, newest first."""
    service = _get_service()
    items = service.list(
        user_id=str(user.id),
        limit=min(limit, 100),
        is_read=is_read,
    )
    return success_response(data=items, message="Alerts retrieved")


@router.post("/mark-all-read")
async def mark_all_alerts_read(user: CurrentUser):
    """Mark all alerts as read."""
    service = _get_service()
    count = service.mark_all_read(user_id=str(user.id))
    return success_response(data={"marked": count}, message=f"Marked {count} alerts as read")


@router.post("/{alert_id}/read")
async def mark_alert_read(alert_id: str, user: CurrentUser):
    """Mark a single alert as read."""
    service = _get_service()
    item = service.mark_read(user_id=str(user.id), alert_id=alert_id)
    return success_response(data=item, message="Alert marked as read")
