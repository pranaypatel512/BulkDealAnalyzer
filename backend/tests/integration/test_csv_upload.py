"""
Integration test: Upload CSV → process → store result

Sprint 0: One integration test for the happy path.
"""

import pytest
from pathlib import Path
from app.core.parser import parse_csv_file, filter_buy_deals, sort_by_quantity


def test_csv_upload_and_process():
    """
    Integration test: Upload CSV, parse, filter BUY deals, sort by quantity.
    
    This is the happy path integration test for Sprint 0.
    """
    # Get fixture path
    fixture_path = Path(__file__).parent.parent.parent.parent / "tests" / "fixtures" / "bulk_deals_sample.csv"
    
    # Parse CSV
    result = parse_csv_file(fixture_path)
    
    # Verify parsing succeeded
    assert result.valid_rows > 0
    assert len(result.deals) > 0
    assert len(result.errors) == 0
    
    # Filter BUY deals
    buy_deals = filter_buy_deals(result.deals)
    
    # Verify we have BUY deals
    assert len(buy_deals) > 0
    assert all(deal.deal_type == "BUY" for deal in buy_deals)
    
    # Sort by quantity (descending)
    sorted_deals = sort_by_quantity(buy_deals, descending=True)
    
    # Verify sorting (first deal should have highest quantity)
    if len(sorted_deals) > 1:
        assert sorted_deals[0].quantity >= sorted_deals[1].quantity
    
    # This test validates the core workflow: parse → filter → sort


