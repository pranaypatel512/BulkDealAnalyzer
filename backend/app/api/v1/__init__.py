"""
API v1 Router

Main router for API version 1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1 import bulk_deals, health

api_router = APIRouter()

# Include routers
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(
    bulk_deals.router,
    prefix="/bulk-deals",
    tags=["Bulk Deals"],
)

