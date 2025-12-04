"""
Tests unitaires pour les endpoints de health check
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Client de test pour l'API sans base de données"""
    return TestClient(app)


def test_health_endpoint(client):
    """Test du endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model_loaded" in data
    assert "database_connected" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


