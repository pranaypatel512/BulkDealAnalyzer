"""
Unit tests for CSV parser.

Sprint 0: Tests for CSV parsing, business rules, and data validation.
"""

from datetime import datetime

import pytest

from app.core.parser import (
    BulkDeal,
    filter_buy_deals,
    filter_by_symbol,
    filter_sell_deals,
    normalize_header,
    parse_csv_content,
    sort_by_price,
    sort_by_quantity,
)


class TestBulkDealModel:
    """Tests for BulkDeal Pydantic model."""

    def test_bulk_deal_model_validation(self):
        """Test valid BulkDeal creation."""
        deal = BulkDeal(
            date="02-Jan-2026",
            symbol="RELIANCE",
            client_name="ABC SECURITIES",
            deal_type="BUY",
            quantity="50,000",  # With comma
            price="2,450.75",   # With comma
        )
        assert deal.symbol == "RELIANCE"
        assert deal.deal_type == "BUY"
        assert deal.quantity == 50000
        assert deal.price == 2450.75
        assert deal.date == datetime(2026, 1, 2)

    def test_bulk_deal_invalid_type(self):
        """Test BulkDeal rejects invalid deal type."""
        with pytest.raises(ValueError):
            BulkDeal(
                date="02-Jan-2026",
                symbol="TEST",
                client_name="Test Client",
                deal_type="INVALID",
                quantity=1000,
                price=100.0,
            )

    def test_bulk_deal_quantity_with_commas(self):
        """Test quantity parsing with commas."""
        deal = BulkDeal(
            date="02-Jan-2026",
            symbol="TEST",
            client_name="Test Client",
            deal_type="BUY",
            quantity="1,234,567",
            price="100.0",
        )
        assert deal.quantity == 1234567

    def test_bulk_deal_price_with_commas(self):
        """Test price parsing with commas."""
        deal = BulkDeal(
            date="02-Jan-2026",
            symbol="TEST",
            client_name="Test Client",
            deal_type="BUY",
            quantity="1000",
            price="1,234.56",
        )
        assert deal.price == 1234.56


class TestNormalizeHeader:
    """Tests for header normalization."""

    def test_normalize_date_header(self):
        """Test date header normalization with various formats."""
        assert normalize_header("DATE \n") == "date"
        assert normalize_header("Date") == "date"
        assert normalize_header('"DATE"') == "date"

    def test_normalize_buy_sell_header(self):
        """Test buy/sell header normalization."""
        assert normalize_header("BUY/SELL \n") == "deal_type"
        assert normalize_header("Buy / Sell") == "deal_type"

    def test_normalize_quantity_header(self):
        """Test quantity header normalization."""
        assert normalize_header("QUANTITY TRADED \n") == "quantity"
        assert normalize_header("Quantity Traded") == "quantity"

    def test_normalize_price_header(self):
        """Test price header normalization."""
        assert normalize_header("TRADE PRICE/ WEIGHTED. AVG. PRICE \n") == "price"
        assert normalize_header("Trade Price / Wght. Avg. Price") == "price"


class TestParseCSVContent:
    """Tests for CSV content parsing."""

    def test_parse_csv_content_valid(self):
        """Test parsing valid CSV content."""
        csv_content = (
            "Date,Symbol,Client Name,Buy / Sell,Quantity Traded,"
            "Trade Price / Wght. Avg. Price\n"
            "02-Jan-2026,RELIANCE,ABC SECURITIES,BUY,50000,2450.75\n"
            "02-Jan-2026,TCS,XYZ CAPITAL,SELL,75000,3875.50"
        )

        result = parse_csv_content(csv_content)

        assert result.total_rows == 2
        assert result.valid_rows == 2
        assert result.invalid_rows == 0
        assert len(result.deals) == 2
        assert result.deals[0].symbol == "RELIANCE"
        assert result.deals[0].deal_type == "BUY"

    def test_parse_csv_content_with_commas_in_numbers(self):
        """Test parsing CSV with comma-formatted numbers."""
        csv_content = (
            "Date,Symbol,Client Name,Buy / Sell,Quantity Traded,"
            "Trade Price / Wght. Avg. Price\n"
            '02-Jan-2026,TEST,CLIENT,"BUY","1,234,567","12,345.67"\n'
        )

        result = parse_csv_content(csv_content)

        assert result.valid_rows == 1
        assert result.deals[0].quantity == 1234567
        assert result.deals[0].price == 12345.67

    def test_parse_csv_content_invalid_row(self):
        """Test parsing CSV with invalid row."""
        csv_content = (
            "Date,Symbol,Client Name,Buy / Sell,Quantity Traded,"
            "Trade Price / Wght. Avg. Price\n"
            "02-Jan-2026,RELIANCE,ABC SECURITIES,BUY,50000,2450.75\n"
            "INVALID,DATA,HERE,WRONG,abc,xyz"
        )

        result = parse_csv_content(csv_content)

        assert result.total_rows == 2
        assert result.valid_rows == 1
        assert result.invalid_rows == 1
        assert len(result.errors) == 1

    def test_parse_csv_content_price_zero_treated_as_invalid(self):
        """Rows with price 0 are invalid and do not raise; valid rows still parsed."""
        csv_content = (
            "Date,Symbol,Security Name,Client Name,Buy/Sell,"
            "Quantity Traded,Trade Price,Remarks\n"
            "02-Jan-2026,REL,Reliance,Client A,BUY,10000,2450.50,\n"
            "02-Jan-2026,TCS,TCS Ltd,Client B,SELL,5000,0,\n"
            "02-Jan-2026,INFY,Infosys,Client C,BUY,20000,1650.25,\n"
        )
        result = parse_csv_content(csv_content)
        assert result.total_rows == 3
        assert result.valid_rows == 2
        assert result.invalid_rows == 1
        assert len(result.deals) == 2
        assert any(d.symbol == "REL" for d in result.deals)
        assert any(d.symbol == "INFY" for d in result.deals)

    def test_parse_nse_format_headers(self):
        """Test parsing CSV with NSE format headers (with newlines)."""
        # Simulating NSE format with header variations
        csv_content = (
            "DATE,SYMBOL,CLIENT NAME,BUY/SELL,QUANTITY TRADED,"
            "TRADE PRICE/ WEIGHTED. AVG. PRICE\n"
            "02-Jan-2026,RELIANCE,ABC SECURITIES,BUY,50000,2450.75"
        )

        result = parse_csv_content(csv_content)

        assert result.valid_rows == 1
        assert result.deals[0].symbol == "RELIANCE"


class TestFilters:
    """Tests for deal filtering functions."""

    @pytest.fixture
    def sample_deals(self):
        """Create sample deals for testing."""
        return [
            BulkDeal(
                date="02-Jan-2026",
                symbol="RELIANCE",
                client_name="A",
                deal_type="BUY",
                quantity=50000,
                price=2450.75,
            ),
            BulkDeal(
                date="02-Jan-2026",
                symbol="TCS",
                client_name="B",
                deal_type="SELL",
                quantity=75000,
                price=3875.50,
            ),
            BulkDeal(
                date="02-Jan-2026",
                symbol="INFY",
                client_name="C",
                deal_type="BUY",
                quantity=100000,
                price=1825.25,
            ),
            BulkDeal(
                date="02-Jan-2026",
                symbol="RELIANCE",
                client_name="D",
                deal_type="SELL",
                quantity=25000,
                price=2460.00,
            ),
        ]

    def test_filter_buy_deals(self, sample_deals):
        """Test filtering BUY deals only."""
        buy_deals = filter_buy_deals(sample_deals)

        assert len(buy_deals) == 2
        assert all(deal.deal_type == "BUY" for deal in buy_deals)

    def test_filter_sell_deals(self, sample_deals):
        """Test filtering SELL deals only."""
        sell_deals = filter_sell_deals(sample_deals)

        assert len(sell_deals) == 2
        assert all(deal.deal_type == "SELL" for deal in sell_deals)

    def test_filter_by_symbol(self, sample_deals):
        """Test filtering by symbol."""
        reliance_deals = filter_by_symbol(sample_deals, "RELIANCE")

        assert len(reliance_deals) == 2
        assert all(deal.symbol == "RELIANCE" for deal in reliance_deals)

    def test_filter_by_symbol_case_insensitive(self, sample_deals):
        """Test filtering by symbol is case-insensitive."""
        reliance_deals = filter_by_symbol(sample_deals, "reliance")

        assert len(reliance_deals) == 2


class TestSorting:
    """Tests for deal sorting functions."""

    @pytest.fixture
    def sample_deals(self):
        """Create sample deals for testing."""
        return [
            BulkDeal(
                date="02-Jan-2026",
                symbol="A",
                client_name="A",
                deal_type="BUY",
                quantity=50000,
                price=100.00,
            ),
            BulkDeal(
                date="02-Jan-2026",
                symbol="B",
                client_name="B",
                deal_type="BUY",
                quantity=100000,
                price=50.00,
            ),
            BulkDeal(
                date="02-Jan-2026",
                symbol="C",
                client_name="C",
                deal_type="BUY",
                quantity=25000,
                price=200.00,
            ),
        ]

    def test_sort_by_quantity_descending(self, sample_deals):
        """Test sorting by quantity (descending)."""
        sorted_deals = sort_by_quantity(sample_deals, descending=True)

        assert sorted_deals[0].quantity == 100000
        assert sorted_deals[1].quantity == 50000
        assert sorted_deals[2].quantity == 25000

    def test_sort_by_quantity_ascending(self, sample_deals):
        """Test sorting by quantity (ascending)."""
        sorted_deals = sort_by_quantity(sample_deals, descending=False)

        assert sorted_deals[0].quantity == 25000
        assert sorted_deals[1].quantity == 50000
        assert sorted_deals[2].quantity == 100000

    def test_sort_by_price_descending(self, sample_deals):
        """Test sorting by price (descending)."""
        sorted_deals = sort_by_price(sample_deals, descending=True)

        assert sorted_deals[0].price == 200.00
        assert sorted_deals[1].price == 100.00
        assert sorted_deals[2].price == 50.00

    def test_sort_by_price_ascending(self, sample_deals):
        """Test sorting by price (ascending)."""
        sorted_deals = sort_by_price(sample_deals, descending=False)

        assert sorted_deals[0].price == 50.00
        assert sorted_deals[1].price == 100.00
        assert sorted_deals[2].price == 200.00
