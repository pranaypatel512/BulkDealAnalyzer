"""
FastAPI Application Entry Point

Sprint 0: Basic FastAPI app structure.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BulkDeal Analyzer API",
    description="API for analyzing bulk deals data",
    version="0.1.0"
)

# CORS middleware (basic setup for Sprint 0)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "BulkDeal Analyzer API",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


