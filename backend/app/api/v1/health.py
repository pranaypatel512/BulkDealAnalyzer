"""
Health Check Endpoints

API endpoints for health checks and status.
"""

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.responses import success_response

router = APIRouter()


@router.get("/")
async def health_check():
    """Health check endpoint."""
    settings = get_settings()
    return success_response(
        data={
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        },
        message="Service is healthy",
    )


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    # TODO: Add database connection check
    return success_response(
        data={"ready": True},
        message="Service is ready",
    )


@router.get("/live")
async def liveness_check():
    """Liveness check endpoint."""
    return success_response(
        data={"alive": True},
        message="Service is alive",
    )

