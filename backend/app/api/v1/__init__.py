"""
API v1 Router

Main router for API version 1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1 import alerts, auth, block_deals, bulk_deals, health, profile, short_selling, watchlist

api_router = APIRouter()

# Include routers
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(
    bulk_deals.router,
    prefix="/bulk-deals",
    tags=["Bulk Deals"],
)
api_router.include_router(block_deals.router, prefix="/block-deals", tags=["Block Deals"])
api_router.include_router(short_selling.router, prefix="/short-selling", tags=["Short Selling"])
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["Watchlist"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])

