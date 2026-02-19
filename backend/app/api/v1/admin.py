"""
Admin API

Endpoints for admin-only operations. All routes require user_profiles.role = 'admin'.
"""

from fastapi import APIRouter

from app.core.auth import CurrentAdminUser
from app.core.responses import success_response

router = APIRouter()


@router.get("/status")
async def admin_status(_user: CurrentAdminUser):
    """
    Confirm current user has admin access.

    Returns 200 with admin: true. Use to guard admin UI or check access.
    """
    return success_response(data={"admin": True}, message="Admin access confirmed")
