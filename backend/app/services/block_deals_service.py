"""
Block Deals Service

Handles list/query for block deals (NSE block deals data).
Same interface as BulkDealsService but for block_deals table.
"""

from app.services.bulk_deals_service import BulkDealsService


class BlockDealsService(BulkDealsService):
    """Service for block deals database operations."""

    TABLE = "block_deals"
