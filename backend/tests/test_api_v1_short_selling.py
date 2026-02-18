"""Tests for short selling API endpoints."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

LIST_RESPONSE = {
    "deals": [
        {
            "id": "short-uuid-1",
            "date": "2026-02-16",
            "symbol": "INFY",
            "security_name": "Infosys Limited",
            "client_name": "Kotak Mahindra",
            "deal_type": "SELL",
            "quantity": 200000,
            "price": 1520.25,
            "remarks": None,
            "user_id": "user-uuid-1",
            "created_at": "2026-02-16T00:00:00+00:00",
            "updated_at": "2026-02-16T00:00:00+00:00",
        },
    ],
    "total": 1,
    "page": 1,
    "page_size": 20,
    "total_pages": 1,
}


def test_list_short_selling():
    """GET /short-selling/ returns short selling deals list."""
    with patch("app.api.v1.short_selling.ShortSellingService") as mock_svc_cls:
        mock_svc = MagicMock()
        mock_svc.list_deals.return_value = LIST_RESPONSE
        mock_svc_cls.return_value = mock_svc

        response = client.get("/api/v1/short-selling/")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] == 1
    assert len(data["data"]["deals"]) == 1
    assert data["data"]["deals"][0]["symbol"] == "INFY"


def test_list_short_selling_with_filters():
    """GET /short-selling/ passes filter params to service."""
    with patch("app.api.v1.short_selling.ShortSellingService") as mock_svc_cls:
        mock_svc = MagicMock()
        mock_svc.list_deals.return_value = LIST_RESPONSE
        mock_svc_cls.return_value = mock_svc

        response = client.get(
            "/api/v1/short-selling/?symbol=INFY&deal_type=SELL&page=2&page_size=10"
        )

    assert response.status_code == 200
    mock_svc.list_deals.assert_called_once_with(
        page=2,
        page_size=10,
        symbol="INFY",
        deal_type="SELL",
        date_from=None,
        date_to=None,
        sort_by="date",
        sort_order="desc",
    )


def test_list_short_selling_invalid_deal_type():
    """GET /short-selling/ rejects invalid deal_type."""
    response = client.get("/api/v1/short-selling/?deal_type=INVALID")
    assert response.status_code == 422


def test_list_short_selling_page_validation():
    """GET /short-selling/ rejects page < 1."""
    response = client.get("/api/v1/short-selling/?page=0")
    assert response.status_code == 422


def test_fetch_short_selling_requires_auth():
    """POST /short-selling/fetch without token returns 401."""
    response = client.post("/api/v1/short-selling/fetch")
    assert response.status_code == 401


def test_export_short_selling_csv():
    """GET /short-selling/export-csv returns raw CSV."""
    with patch("app.api.v1.short_selling.ShortSellingService") as mock_svc_cls:
        mock_svc = MagicMock()
        mock_svc.export_deals.return_value = {
            "deals": LIST_RESPONSE["deals"],
            "total": 1,
            "truncated": False,
        }
        mock_svc_cls.return_value = mock_svc

        response = client.get("/api/v1/short-selling/export-csv?symbol=INFY&max_rows=10")

    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    assert response.headers.get("x-export-total") == "1"
    assert response.headers.get("x-export-truncated") == "false"
    assert "INFY" in response.text
