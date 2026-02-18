"""Tests for block deals API endpoints."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

LIST_RESPONSE = {
    "deals": [
        {
            "id": "block-uuid-1",
            "date": "2026-02-16",
            "symbol": "TCS",
            "security_name": "Tata Consultancy Services",
            "client_name": "ICICI Prudential",
            "deal_type": "BUY",
            "quantity": 500000,
            "price": 3850.50,
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


def test_list_block_deals():
    """GET /block-deals/ returns block deals list."""
    with patch("app.api.v1.block_deals.BlockDealsService") as mock_svc_cls:
        mock_svc = MagicMock()
        mock_svc.list_deals.return_value = LIST_RESPONSE
        mock_svc_cls.return_value = mock_svc

        response = client.get("/api/v1/block-deals/")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] == 1
    assert len(data["data"]["deals"]) == 1
    assert data["data"]["deals"][0]["symbol"] == "TCS"


def test_list_block_deals_with_filters():
    """GET /block-deals/ passes filter params to service."""
    with patch("app.api.v1.block_deals.BlockDealsService") as mock_svc_cls:
        mock_svc = MagicMock()
        mock_svc.list_deals.return_value = LIST_RESPONSE
        mock_svc_cls.return_value = mock_svc

        response = client.get(
            "/api/v1/block-deals/?symbol=TCS&deal_type=BUY&page=2&page_size=10"
        )

    assert response.status_code == 200
    mock_svc.list_deals.assert_called_once_with(
        page=2,
        page_size=10,
        symbol="TCS",
        deal_type="BUY",
        date_from=None,
        date_to=None,
        sort_by="date",
        sort_order="desc",
    )


def test_list_block_deals_invalid_deal_type():
    """GET /block-deals/ rejects invalid deal_type."""
    response = client.get("/api/v1/block-deals/?deal_type=INVALID")
    assert response.status_code == 422


def test_list_block_deals_page_validation():
    """GET /block-deals/ rejects page < 1."""
    response = client.get("/api/v1/block-deals/?page=0")
    assert response.status_code == 422


def test_fetch_block_deals_requires_auth():
    """POST /block-deals/fetch without token returns 401."""
    response = client.post("/api/v1/block-deals/fetch")
    assert response.status_code == 401


def test_export_block_deals_csv():
    """GET /block-deals/export-csv returns raw CSV."""
    with patch("app.api.v1.block_deals.BlockDealsService") as mock_svc_cls:
        mock_svc = MagicMock()
        mock_svc.export_deals.return_value = {
            "deals": LIST_RESPONSE["deals"],
            "total": 1,
            "truncated": False,
        }
        mock_svc_cls.return_value = mock_svc

        response = client.get("/api/v1/block-deals/export-csv?symbol=TCS&max_rows=10")

    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    assert response.headers.get("x-export-total") == "1"
    assert response.headers.get("x-export-truncated") == "false"
    assert "TCS" in response.text
