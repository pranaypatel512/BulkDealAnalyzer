"""
Tests for Health Check API Endpoints
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
    assert "version" in data
    assert "api_prefix" in data
    assert data["api_prefix"] == "/api/v1"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"
    assert "app_name" in data["data"]
    assert "version" in data["data"]
    assert "environment" in data["data"]


def test_readiness_check():
    """Test readiness check endpoint."""
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["ready"] is True


def test_liveness_check():
    """Test liveness check endpoint."""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["alive"] is True

