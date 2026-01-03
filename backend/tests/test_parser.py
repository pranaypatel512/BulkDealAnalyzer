"""
Unit tests for CSV parser.

Sprint 0: Essential tests only (10-15 tests total).
"""

import pytest
from pathlib import Path
from datetime import datetime

from app.core.parser import (
    parse_csv_file,
    parse_csv_content,
    filter_buy_deals,
    sort_by_quantity,
    BulkDeal
)


# Sample CSV content for testing
SAMPLE_CSV = """Date,Symbol,Client Name,Buy / Sell,Quantity Traded,Trade Price / Wght. Avg. Price
01-Jan-2024,RELIANCE,ABC CAPITAL SERVICES LTD.,BUY,500000,2450.50
01-Jan-2024,TCS,XYZ SECURITIES PVT. LTD.,BUY,250000,3450.75
01-Jan-2024,HDFCBANK,DEF INVESTMENTS,SELL,100000,1650.25"""


def test_parse_csv_content_valid():
    """Test parsing valid CSV content."""
    result = parse_csv_content(SAMPLE_CSV)
    
    assert result.valid_rows == 3
    assert result.invalid_rows == 0
    assert len(result.deals) == 3
    assert result.errors == []


def test_parse_csv_content_invalid_row():
    """Test parsing CSV with invalid row."""
    invalid_csv = """Date,Symbol,Client Name,Buy / Sell,Quantity Traded,Trade Price / Wght. Avg. Price
01-Jan-2024,RELIANCE,ABC CAPITAL,BUY,500000,2450.50
01-Jan-2024,TCS,XYZ,INVALID_TYPE,250000,3450.75"""
    
    result = parse_csv_content(invalid_csv)
    
    assert result.valid_rows == 1
    assert result.invalid_rows == 1
    assert len(result.errors) > 0


def test_bulk_deal_model_validation():
    """Test BulkDeal model validation."""
    deal = BulkDeal(
        date=datetime(2024, 1, 1),
        symbol="RELIANCE",
        client_name="ABC Capital",
        deal_type="BUY",
        quantity=500000,
        price=2450.50
    )
    
    assert deal.symbol == "RELIANCE"
    assert deal.deal_type == "BUY"
    assert deal.quantity == 500000


def test_bulk_deal_invalid_type():
    """Test BulkDeal rejects invalid deal type."""
    with pytest.raises(ValueError):
        BulkDeal(
            date=datetime(2024, 1, 1),
            symbol="RELIANCE",
            client_name="ABC Capital",
            deal_type="INVALID",
            quantity=500000,
            price=2450.50
        )


def test_filter_buy_deals():
    """Test filtering only BUY deals."""
    deals = [
        BulkDeal(
            date=datetime(2024, 1, 1),
            symbol="RELIANCE",
            client_name="ABC",
            deal_type="BUY",
            quantity=500000,
            price=2450.50
        ),
        BulkDeal(
            date=datetime(2024, 1, 1),
            symbol="TCS",
            client_name="XYZ",
            deal_type="SELL",
            quantity=250000,
            price=3450.75
        ),
    ]
    
    buy_deals = filter_buy_deals(deals)
    
    assert len(buy_deals) == 1
    assert buy_deals[0].deal_type == "BUY"


def test_sort_by_quantity():
    """Test sorting deals by quantity."""
    deals = [
        BulkDeal(
            date=datetime(2024, 1, 1),
            symbol="TCS",
            client_name="XYZ",
            deal_type="BUY",
            quantity=250000,
            price=3450.75
        ),
        BulkDeal(
            date=datetime(2024, 1, 1),
            symbol="RELIANCE",
            client_name="ABC",
            deal_type="BUY",
            quantity=500000,
            price=2450.50
        ),
    ]
    
    sorted_deals = sort_by_quantity(deals, descending=True)
    
    assert sorted_deals[0].quantity == 500000
    assert sorted_deals[1].quantity == 250000


