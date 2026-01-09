"""
Pydantic Models for Bulk Deals

This module defines data models for bulk deals and related entities.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DealType(str, Enum):
    """Deal type enumeration."""
    BUY = "BUY"
    SELL = "SELL"


class BulkDealCreate(BaseModel):
    """Model for creating a bulk deal."""

    date: datetime
    symbol: str = Field(..., min_length=1, max_length=20)
    client_name: str = Field(..., min_length=1)
    deal_type: DealType
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class BulkDealResponse(BaseModel):
    """Model for bulk deal API response."""

    id: int
    date: datetime
    symbol: str
    client_name: str
    deal_type: DealType
    quantity: int
    price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BulkDealFilter(BaseModel):
    """Model for filtering bulk deals."""

    symbol: str | None = None
    deal_type: DealType | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    min_quantity: int | None = None
    max_quantity: int | None = None


class BulkDealsListResponse(BaseModel):
    """Model for bulk deals list API response."""

    deals: list[BulkDealResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


