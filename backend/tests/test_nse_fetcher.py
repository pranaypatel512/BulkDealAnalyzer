"""Tests for NSE Fetcher service."""

from unittest.mock import MagicMock, patch

import pytest

from app.services.nse_fetcher import NSEFetcher


def _mock_chain(mock, *attrs):
    """Build a chained mock: mock.a.b.c... = value."""
    obj = mock
    for attr in attrs:
        obj = getattr(obj.return_value, attr)
    return obj


@pytest.fixture
def mock_supabase():
    """Mock Supabase clients."""
    with patch(
        "app.services.nse_fetcher.NSEFetcher.__init__",
        return_value=None,
    ):
        fetcher = NSEFetcher.__new__(NSEFetcher)
        fetcher._client = MagicMock()
        yield fetcher


class TestNSEJsonToCsv:
    """Test JSON-to-CSV conversion."""

    def test_empty_deals(self, mock_supabase):
        result = mock_supabase._nse_json_to_csv([])
        assert result == ""

    def test_single_deal(self, mock_supabase):
        deals = [
            {
                "BD_DT_DATE": "16-Feb-2026",
                "BD_SYMBOL": "RELIANCE",
                "BD_SCRIP_NAME": "Reliance Industries",
                "BD_CLIENT_NAME": "ABC Capital",
                "BD_BUY_SELL": "BUY",
                "BD_QTY_TRD": "100000",
                "BD_TP_WATP": "2450.50",
                "BD_REMARKS": "",
            }
        ]
        csv = mock_supabase._nse_json_to_csv(deals)
        lines = csv.strip().split("\n")
        assert len(lines) == 2
        assert "RELIANCE" in lines[1]
        assert "ABC Capital" in lines[1]
        assert "BUY" in lines[1]

    def test_deal_with_commas_in_name(self, mock_supabase):
        deals = [
            {
                "BD_DT_DATE": "16-Feb-2026",
                "BD_SYMBOL": "TCS",
                "BD_SCRIP_NAME": "Tata Consultancy Services",
                "BD_CLIENT_NAME": "XYZ Securities, Private Ltd",
                "BD_BUY_SELL": "SELL",
                "BD_QTY_TRD": "50000",
                "BD_TP_WATP": "3800.00",
                "BD_REMARKS": "",
            }
        ]
        csv = mock_supabase._nse_json_to_csv(deals)
        assert '"XYZ Securities, Private Ltd"' in csv

    def test_skips_invalid_rows_empty_fields(self, mock_supabase):
        """Rows with empty date/symbol/client_name or zero qty/price are skipped."""
        deals = [
            {"BD_DT_DATE": "", "BD_SYMBOL": "", "BD_CLIENT_NAME": "", "BD_BUY_SELL": "BUY", "BD_QTY_TRD": 0, "BD_TP_WATP": 0},
            {"BD_DT_DATE": "16-Feb-2026", "BD_SYMBOL": "REL", "BD_CLIENT_NAME": "ABC", "BD_BUY_SELL": "BUY", "BD_QTY_TRD": 100, "BD_TP_WATP": 2500.0},
        ]
        csv = mock_supabase._nse_json_to_csv(deals)
        lines = csv.strip().split("\n")
        assert len(lines) == 2  # header + 1 valid row
        assert "REL" in lines[1]

    def test_camelCase_field_names(self, mock_supabase):
        """Supports camelCase NSE API fields (date, symbol, clientName, buySell, qty, watp)."""
        deals = [
            {
                "date": "2026-02-16",
                "symbol": "INFY",
                "name": "Infosys",
                "clientName": "MF Client",
                "buySell": "Buy",
                "qty": 50000,
                "watp": 1650.50,
                "remarks": "",
            }
        ]
        csv = mock_supabase._nse_json_to_csv(deals)
        lines = csv.strip().split("\n")
        assert len(lines) == 2
        assert "INFY" in lines[1]
        assert "BUY" in lines[1]
        assert "16-Feb-2026" in lines[1]


class TestDedup:
    """Test deduplication logic."""

    def test_no_existing_deals(self, mock_supabase):
        mock_result = MagicMock()
        mock_result.data = []
        tbl = mock_supabase._client.table.return_value
        tbl.select.return_value.eq.return_value.in_.return_value \
            .execute.return_value = mock_result

        deals = [
            {
                "date": "2026-02-16",
                "symbol": "RELIANCE",
                "client_name": "ABC",
                "deal_type": "BUY",
                "quantity": 100000,
            }
        ]
        result = mock_supabase._dedup_deals(deals)
        assert len(result) == 1

    def test_all_duplicates(self, mock_supabase):
        mock_result = MagicMock()
        mock_result.data = [
            {
                "date": "2026-02-16",
                "symbol": "RELIANCE",
                "client_name": "ABC",
                "deal_type": "BUY",
                "quantity": 100000,
            }
        ]
        tbl = mock_supabase._client.table.return_value
        tbl.select.return_value.eq.return_value.in_.return_value \
            .execute.return_value = mock_result

        deals = [
            {
                "date": "2026-02-16",
                "symbol": "RELIANCE",
                "client_name": "ABC",
                "deal_type": "BUY",
                "quantity": 100000,
            }
        ]
        result = mock_supabase._dedup_deals(deals)
        assert len(result) == 0

    def test_empty_input(self, mock_supabase):
        result = mock_supabase._dedup_deals([])
        assert result == []


class TestImportFromCsv:
    """Test CSV import with dedup."""

    def test_valid_csv_import(self, mock_supabase):
        csv_content = (
            "Date,Symbol,Security Name,Client Name,Buy/Sell,"
            "Quantity Traded,Trade Price,Remarks\n"
            "16-Feb-2026,RELIANCE,Reliance Industries,"
            "ABC Capital,BUY,100000,2450.50,\n"
        )

        # Mock empty existing (no dupes)
        mock_select = MagicMock()
        mock_select.data = []
        tbl = mock_supabase._client.table.return_value
        tbl.select.return_value.eq.return_value.in_.return_value \
            .execute.return_value = mock_select

        # Mock successful insert
        mock_insert = MagicMock()
        mock_insert.data = [{"id": "test-id"}]
        tbl.insert.return_value.execute.return_value = mock_insert

        result = mock_supabase.import_from_csv(
            csv_content, user_id="user-123",
        )
        assert result["status"] == "success"
        assert result["imported"] >= 0


class TestFetchHistory:
    """Test fetch history retrieval."""

    def test_get_empty_history(self, mock_supabase):
        mock_result = MagicMock()
        mock_result.data = []
        tbl = mock_supabase._client.table.return_value
        tbl.select.return_value.order.return_value \
            .limit.return_value.execute.return_value = mock_result

        result = mock_supabase.get_fetch_history()
        assert result == []

    def test_get_last_fetch_none(self, mock_supabase):
        tbl = mock_supabase._client.table.return_value
        tbl.select.return_value.eq.return_value \
            .order.return_value.limit.return_value \
            .maybe_single.return_value \
            .execute.return_value = None

        result = mock_supabase.get_last_fetch()
        assert result is None


class TestFetchEndpoints:
    """Test API endpoint access control."""

    def test_fetch_requires_auth(self):
        from fastapi.testclient import TestClient

        from app.main import app

        client = TestClient(app)
        response = client.post("/api/v1/bulk-deals/fetch")
        assert response.status_code == 401

    def test_fetch_history_is_public(self):
        from fastapi.testclient import TestClient

        from app.main import app

        client = TestClient(app)
        response = client.get("/api/v1/bulk-deals/fetch-history")
        assert response.status_code == 200
