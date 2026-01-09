"""
Tests for Bulk Deals API Endpoints
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_bulk_deals():
    """Test list bulk deals endpoint."""
    response = client.get("/api/v1/bulk-deals/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "deals" in data["data"]
    assert "total" in data["data"]
    assert data["data"]["total"] == 0  # Empty list for now
    assert isinstance(data["data"]["deals"], list)


def test_get_bulk_deal():
    """Test get bulk deal by ID endpoint."""
    test_deal_id = "test-deal-id-123"
    response = client.get(f"/api/v1/bulk-deals/{test_deal_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "id" in data["data"]
    assert data["data"]["id"] == test_deal_id


def test_bulk_deals_response_format():
    """Test that bulk deals endpoints return correct response format."""
    response = client.get("/api/v1/bulk-deals/")
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "success" in data
    assert "message" in data
    assert "data" in data
    assert data["success"] is True

