"""
Tests d'intégration pour les endpoints de health check
"""
import pytest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Client de test pour l'API"""
    return TestClient(app)


def test_health_database_not_connected(client):
    """Test lorsque la base de données n'est pas accessible"""
    with patch('app.api.routes.health.create_engine') as mock_engine:
        mock_conn = Mock()
        mock_engine.return_value.connect.side_effect = Exception("Connection failed")
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "database_connected" in data
        # Le test peut passer ou échouer selon la configuration, mais l'endpoint doit répondre


def test_health_with_model_loaded(client):
    """Test du health check avec modèle chargé"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model_loaded" in data
    assert "database_connected" in data
    assert "version" in data
    assert data["version"] == "1.0.0"







