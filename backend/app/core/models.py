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
    
    id: str  # UUID as string
    date: datetime
    symbol: str
    security_name: str | None = None
    client_name: str
    deal_type: DealType
    quantity: int
    price: float
    remarks: str | None = None
    user_id: str | None = None  # UUID as string
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BulkDealFilter(BaseModel):
    """Model for filtering bulk deals."""
    
    symbol: Optional[str] = None
    deal_type: Optional[DealType] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_quantity: Optional[int] = None
    max_quantity: Optional[int] = None


class BulkDealsListResponse(BaseModel):
    """Model for bulk deals list API response."""
    
    deals: List[BulkDealResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


