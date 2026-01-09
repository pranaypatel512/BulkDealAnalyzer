"""
Integration test: Upload CSV → process → store result

Sprint 0: One integration test for the happy path.
Uses actual NSE bulk deals CSV format.
"""

from pathlib import Path

from app.core.parser import (
    filter_buy_deals,
    filter_by_symbol,
    filter_sell_deals,
    parse_csv_file,
    sort_by_quantity,
)


def test_csv_upload_and_process():
    """
    Integration test: Upload CSV, parse, filter BUY deals, sort by quantity.

    This is the happy path integration test for Sprint 0.
    Uses actual NSE bulk deals CSV format.
    """
    # Get fixture path (relative to project root)
    # From backend/tests/integration/test_csv_upload.py -> project_root/tests/fixtures/
    project_root = Path(__file__).parent.parent.parent.parent
    fixture_path = project_root / "tests" / "fixtures" / "bulk_deals_sample.csv"

    # Debug: ensure file exists
    assert fixture_path.exists(), f"Fixture not found at {fixture_path}"

    # Parse CSV
    result = parse_csv_file(fixture_path)

    # Verify parsing succeeded (allow some errors due to edge cases)
    assert result.total_rows > 0, "No rows found in CSV"
    assert result.valid_rows > 0, f"No valid rows. Errors: {result.errors[:5]}"
    assert len(result.deals) > 0, "No deals parsed"

    # Filter BUY deals
    buy_deals = filter_buy_deals(result.deals)

    # Verify we have BUY deals
    assert len(buy_deals) > 0, "No BUY deals found"
    assert all(deal.deal_type == "BUY" for deal in buy_deals)

    # Filter SELL deals
    sell_deals = filter_sell_deals(result.deals)
    assert len(sell_deals) > 0, "No SELL deals found"

    # Sort by quantity (descending)
    sorted_deals = sort_by_quantity(buy_deals, descending=True)

    # Verify sorting (first deal should have highest quantity)
    if len(sorted_deals) > 1:
        assert sorted_deals[0].quantity >= sorted_deals[1].quantity

    # Test symbol filter
    all_symbols = set(deal.symbol for deal in result.deals)
    if all_symbols:
        test_symbol = list(all_symbols)[0]
        symbol_deals = filter_by_symbol(result.deals, test_symbol)
        assert len(symbol_deals) > 0
        assert all(deal.symbol == test_symbol for deal in symbol_deals)

    # Print summary for debugging
    print("\n✅ Integration test passed!")
    print(f"   Total rows: {result.total_rows}")
    print(f"   Valid rows: {result.valid_rows}")
    print(f"   BUY deals: {len(buy_deals)}")
    print(f"   SELL deals: {len(sell_deals)}")
    print(f"   Unique symbols: {len(all_symbols)}")


