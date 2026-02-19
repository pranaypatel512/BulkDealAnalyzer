"""
Admin API

Endpoints for admin-only operations. All routes require user_profiles.role = 'admin'.
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.core.auth import CurrentAdminUser
from app.core.responses import success_response
from app.services.admin_service import AdminService


class RoleUpdateBody(BaseModel):
    """Body for PATCH /admin/users/{user_id}/role."""

    role: str  # 'user' | 'admin' validated in endpoint

router = APIRouter()


def _get_admin_service() -> AdminService:
    return AdminService()


@router.get("/status")
async def admin_status(_user: CurrentAdminUser):
    """
    Confirm current user has admin access.

    Returns 200 with admin: true. Use to guard admin UI or check access.
    """
    return success_response(data={"admin": True}, message="Admin access confirmed")


@router.get("/users")
async def list_users(
    _user: CurrentAdminUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: str | None = Query(None, pattern="^(user|admin)$"),
):
    """
    List user profiles (admin only). Paginated.

    Optional role filter: user | admin.
    """
    service = _get_admin_service()
    result = service.list_users(page=page, page_size=page_size, role=role)
    return success_response(data=result, message="Users retrieved")


@router.patch("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    _user: CurrentAdminUser,
    body: RoleUpdateBody,
):
    """
    Update a user's role (admin only). Body: { "role": "user" | "admin" }.
    """
    if body.role not in ("user", "admin"):
        from app.core.exceptions import BulkDealValidationError

        raise BulkDealValidationError("role must be 'user' or 'admin'")
    service = _get_admin_service()
    profile = service.update_user_role(user_id=user_id, role=body.role)
    return success_response(data=profile, message="Role updated")


@router.get("/stats")
async def admin_stats(_user: CurrentAdminUser):
    """
    Simple dashboard stats: user count, bulk_deals count, block_deals count (admin only).
    """
    service = _get_admin_service()
    stats = service.get_stats()
    return success_response(data=stats, message="Stats retrieved")
