"""
Pydantic Models for BulkDeal Analyzer

This module defines data models for bulk deals, user profiles, and related entities.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

try:
    from enum import StrEnum
except ImportError:  # Python < 3.11
    from enum import Enum

    class StrEnum(str, Enum):  # type: ignore[no-redef]
        """Backport of StrEnum for Python < 3.11."""


# =============================================================================
# Deal Types
# =============================================================================


class DealType(StrEnum):
    """Deal type enumeration."""
    BUY = "BUY"
    SELL = "SELL"


# =============================================================================
# User Profile Models
# =============================================================================


class UserProfileCreate(BaseModel):
    """Model for creating a user profile."""

    full_name: str | None = Field(None, max_length=255)


class UserProfileUpdate(BaseModel):
    """Model for updating a user profile."""

    full_name: str | None = Field(None, max_length=255)
    subscription_tier: str | None = Field(None, pattern=r"^(free|premium|enterprise)$")


class UserProfileResponse(BaseModel):
    """Model for user profile API response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    email: str
    full_name: str | None = None
    subscription_tier: str = "free"
    created_at: datetime
    updated_at: datetime


# =============================================================================
# Bulk Deal Models
# =============================================================================


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

    model_config = ConfigDict(from_attributes=True)

    id: str  # UUID as string (matches database schema)
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
