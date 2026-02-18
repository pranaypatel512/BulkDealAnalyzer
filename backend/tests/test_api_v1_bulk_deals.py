"""Tests for bulk deals API endpoints."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SAMPLE_DEAL = {
    "id": "deal-uuid-1",
    "date": "2026-02-16",
    "symbol": "RELIANCE",
    "security_name": "Reliance Industries",
    "client_name": "HDFC AMC",
    "deal_type": "BUY",
    "quantity": 150000,
    "price": 2456.75,
    "remarks": None,
    "user_id": "user-uuid-1",
    "created_at": "2026-02-16T00:00:00+00:00",
    "updated_at": "2026-02-16T00:00:00+00:00",
}

LIST_RESPONSE = {
    "deals": [SAMPLE_DEAL],
    "total": 1,
    "page": 1,
    "page_size": 20,
    "total_pages": 1,
}

STATS_RESPONSE = {
    "total_deals": 100,
    "buy_deals": 60,
    "sell_deals": 40,
}


def _auth_patch():
    """Patch auth to return a valid mock user."""
    mock_user = MagicMock()
    mock_user.id = "user-uuid-1"
    mock_user.email = "test@example.com"
    mock_user.user_metadata = {}
    mock_user.email_confirmed_at = "2026-01-01T00:00:00Z"
    mock_user.created_at = "2026-01-01T00:00:00Z"
    mock_user.last_sign_in_at = "2026-02-16T00:00:00Z"

    mock_response = MagicMock()
    mock_response.user = mock_user
    return patch(
        "app.core.auth._get_supabase_client",
        return_value=MagicMock(
            auth=MagicMock(get_user=MagicMock(return_value=mock_response)),
        ),
    )


# ---- GET /bulk-deals/ ----


def test_list_deals():
    """GET /bulk-deals/ returns deals list."""
    with patch("app.api.v1.bulk_deals._get_service") as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.list_deals.return_value = LIST_RESPONSE
        mock_svc_factory.return_value = mock_svc

        response = client.get("/api/v1/bulk-deals/")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] == 1
    assert len(data["data"]["deals"]) == 1
    assert data["data"]["deals"][0]["symbol"] == "RELIANCE"


def test_list_deals_with_filters():
    """GET /bulk-deals/ passes filter params to service."""
    with patch("app.api.v1.bulk_deals._get_service") as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.list_deals.return_value = LIST_RESPONSE
        mock_svc_factory.return_value = mock_svc

        response = client.get(
            "/api/v1/bulk-deals/?symbol=REL&deal_type=BUY&page=2&page_size=10"
        )

    assert response.status_code == 200
    mock_svc.list_deals.assert_called_once_with(
        page=2,
        page_size=10,
        symbol="REL",
        deal_type="BUY",
        date_from=None,
        date_to=None,
        sort_by="date",
        sort_order="desc",
    )


def test_list_deals_invalid_deal_type():
    """GET /bulk-deals/ rejects invalid deal_type."""
    response = client.get("/api/v1/bulk-deals/?deal_type=INVALID")
    assert response.status_code == 422


def test_list_deals_page_validation():
    """GET /bulk-deals/ rejects page < 1."""
    response = client.get("/api/v1/bulk-deals/?page=0")
    assert response.status_code == 422


# ---- GET /bulk-deals/stats ----


def test_get_stats():
    """GET /bulk-deals/stats returns statistics."""
    with patch("app.api.v1.bulk_deals._get_service") as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.get_stats.return_value = STATS_RESPONSE
        mock_svc_factory.return_value = mock_svc

        response = client.get("/api/v1/bulk-deals/stats")

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total_deals"] == 100
    assert data["data"]["buy_deals"] == 60
    assert data["data"]["sell_deals"] == 40


# ---- GET /bulk-deals/{deal_id} ----


def test_get_deal_by_id():
    """GET /bulk-deals/{id} returns a single deal."""
    with patch("app.api.v1.bulk_deals._get_service") as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.get_by_id.return_value = SAMPLE_DEAL
        mock_svc_factory.return_value = mock_svc

        response = client.get("/api/v1/bulk-deals/deal-uuid-1")

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == "deal-uuid-1"
    assert data["data"]["symbol"] == "RELIANCE"


# ---- POST /bulk-deals/import ----


def test_import_requires_auth():
    """POST /bulk-deals/import without token returns 401."""
    response = client.post(
        "/api/v1/bulk-deals/import",
        params={"csv_content": "Date,Symbol\n2026-01-01,TEST"},
    )
    assert response.status_code == 401


def test_parse_requires_auth():
    """POST /bulk-deals/parse without token returns 401."""
    response = client.post(
        "/api/v1/bulk-deals/parse",
        params={"csv_content": "Date,Symbol\n2026-01-01,TEST"},
    )
    assert response.status_code == 401


# ---- GET /bulk-deals/analytics/* ----


TOP_SYMBOLS_RESPONSE = [
    {
        "symbol": "RELIANCE",
        "total_quantity": 500000,
        "deal_count": 10,
        "buy_count": 6,
        "sell_count": 4,
    },
]

DAILY_TREND_RESPONSE = [
    {
        "date": "2026-02-16",
        "total_deals": 5,
        "buy_deals": 3,
        "sell_deals": 2,
        "total_quantity": 100000,
        "total_value": 245000000.0,
    },
]

PRICE_DIST_RESPONSE = [
    {"range": "0-50", "count": 5},
    {"range": "50-100", "count": 12},
    {"range": "100-500", "count": 30},
]


def test_top_symbols():
    """GET /analytics/top-symbols returns top symbols."""
    with patch(
        "app.api.v1.bulk_deals._get_service",
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.get_top_symbols.return_value = TOP_SYMBOLS_RESPONSE
        mock_svc_factory.return_value = mock_svc

        response = client.get(
            "/api/v1/bulk-deals/analytics/top-symbols",
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["symbol"] == "RELIANCE"


def test_daily_trend():
    """GET /analytics/daily-trend returns daily data."""
    with patch(
        "app.api.v1.bulk_deals._get_service",
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.get_daily_trend.return_value = DAILY_TREND_RESPONSE
        mock_svc_factory.return_value = mock_svc

        response = client.get(
            "/api/v1/bulk-deals/analytics/daily-trend?days=7",
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["total_deals"] == 5


def test_price_distribution():
    """GET /analytics/price-distribution returns ranges."""
    with patch(
        "app.api.v1.bulk_deals._get_service",
    ) as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.get_price_distribution.return_value = PRICE_DIST_RESPONSE
        mock_svc_factory.return_value = mock_svc

        response = client.get(
            "/api/v1/bulk-deals/analytics/price-distribution",
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 3


# ---- GET /bulk-deals/export-csv ----


def test_export_bulk_deals_csv():
    """GET /bulk-deals/export-csv returns raw CSV."""
    with patch("app.api.v1.bulk_deals._get_service") as mock_svc_factory:
        mock_svc = MagicMock()
        mock_svc.export_deals.return_value = {
            "deals": [SAMPLE_DEAL],
            "total": 1,
            "truncated": False,
        }
        mock_svc_factory.return_value = mock_svc

        response = client.get("/api/v1/bulk-deals/export-csv?symbol=REL&max_rows=10")

    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    assert response.headers.get("x-export-total") == "1"
    assert response.headers.get("x-export-truncated") == "false"
    assert response.text.splitlines()[0].startswith("Date,Symbol,")
    assert "RELIANCE" in response.text
