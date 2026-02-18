"""
Short Selling Service

Handles list/query for short selling deals (NSE short selling data).
Same interface as BulkDealsService but for short_selling_deals table.
"""

from app.services.bulk_deals_service import BulkDealsService


class ShortSellingService(BulkDealsService):
    """Service for short selling deals database operations."""

    TABLE = "short_selling_deals"
