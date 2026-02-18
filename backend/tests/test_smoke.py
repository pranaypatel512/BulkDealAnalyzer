"""
Smoke tests: verify app is wired and key routes respond.

These run with TestClient (in-process, no real server).
CI runs them as part of ci-backend-test.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_smoke_root():
    """Root returns ok and api_prefix."""
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
    assert r.json().get("api_prefix") == "/api/v1"


def test_smoke_health():
    """Health endpoint returns healthy."""
    r = client.get("/api/v1/health/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("success") is True
    assert data.get("data", {}).get("status") == "healthy"


def test_smoke_bulk_deals_list():
    """Bulk deals list returns 200 and has deals key."""
    with patch("app.api.v1.bulk_deals._get_service") as mock_svc:
        mock_svc.return_value.list_deals.return_value = {
            "deals": [],
            "total": 0,
            "page": 1,
            "page_size": 20,
            "total_pages": 0,
        }
        r = client.get("/api/v1/bulk-deals/?page=1&page_size=5")
    assert r.status_code == 200
    assert "deals" in r.json().get("data", {})


def test_smoke_bulk_deals_export_csv():
    """Bulk deals export-csv returns CSV and 200."""
    with patch("app.api.v1.bulk_deals._get_service") as mock_svc:
        mock_svc.return_value.export_deals.return_value = {
            "deals": [],
            "total": 0,
            "truncated": False,
        }
        r = client.get("/api/v1/bulk-deals/export-csv?max_rows=10")
    assert r.status_code == 200
    assert "text/csv" in r.headers.get("content-type", "")
    assert r.text.strip().startswith("Date,Symbol,")
