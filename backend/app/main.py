"""
FastAPI Application Entry Point

Sprint 1: Core module structure with routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import get_settings

# Get settings
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API for analyzing bulk deals data",
    version=settings.app_version,
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "status": "ok",
        "message": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "docs_url": "/docs",
        "api_prefix": settings.api_v1_prefix,
    }


