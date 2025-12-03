"""
Tests unitaires pour l'application principale
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test de la route racine (redirection vers /docs)"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Redirection


def test_openapi_schema():
    """Test que le schéma OpenAPI est accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "API Prédiction Attrition"


def test_docs_accessible():
    """Test que la documentation Swagger est accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_accessible():
    """Test que la documentation ReDoc est accessible"""
    response = client.get("/redoc")
    assert response.status_code == 200


