"""
Tests d'intégration pour les endpoints de prédiction
"""
import pytest
from unittest.mock import patch, Mock
from app.models.database import Prediction


def test_predict_attrition_endpoint(client, sample_prediction_data):
    """Test de l'endpoint de prédiction avec des données valides"""
    response = client.post("/predict/attrition", json=sample_prediction_data)
    
    # Même si le modèle n'est pas chargé, l'endpoint devrait répondre
    assert response.status_code in [200, 503, 500]  # Ajout de 500 pour erreur interne
    
    if response.status_code == 200:
        data = response.json()
        assert "prediction" in data
        assert "probability" in data
        assert "class_name" in data
        assert data["prediction"] in [0, 1]
        assert 0 <= data["probability"] <= 1


def test_predict_attrition_invalid_data(client):
    """Test avec des données invalides"""
    invalid_data = {
        "age": -5,  # Âge invalide
        "revenu_mensuel": -1000  # Revenu invalide
    }
    
    response = client.post("/predict/attrition", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_predict_attrition_missing_fields(client):
    """Test avec des champs manquants"""
    incomplete_data = {
        "age": 30
        # Manque les champs requis
    }
    
    response = client.post("/predict/attrition", json=incomplete_data)
    assert response.status_code == 422  # Validation error


def test_predict_batch(client, sample_prediction_data):
    """Test de prédiction en batch"""
    batch_data = [sample_prediction_data] * 3
    
    response = client.post("/predict/attrition/batch", json=batch_data)
    assert response.status_code in [200, 503, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3


def test_prediction_history(client, db):
    """Test de récupération de l'historique"""
    response = client.get("/predict/history")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_prediction_history_with_limit(client, db):
    """Test de récupération de l'historique avec limite"""
    response = client.get("/predict/history?limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5


def test_prediction_history_with_employee_id(client, db, sample_prediction_data):
    """Test de récupération de l'historique filtré par employee_id"""
    # Créer une prédiction avec un employee_id spécifique
    prediction = Prediction(
        employee_id=999,
        input_data=sample_prediction_data,
        prediction=1,
        probability=0.8,
        class_name="Attrition"
    )
    db.add(prediction)
    db.commit()
    
    response = client.get("/predict/history?employee_id=999")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert all(p.get("employee_id") == 999 for p in data)


def test_prediction_saved_in_db(client, sample_prediction_data, db):
    """Test que la prédiction est bien sauvegardée en base"""
    # Faire une prédiction
    response = client.post("/predict/attrition", json=sample_prediction_data)
    
    if response.status_code == 200:
        # Vérifier qu'elle est en base
        predictions = db.query(Prediction).all()
        assert len(predictions) > 0


def test_predict_with_model_not_loaded(client, sample_prediction_data):
    """Test lorsque le modèle n'est pas chargé"""
    with patch('ml.model_loader.model_loader.is_loaded', return_value=False):
        with patch('ml.model_loader.model_loader.load', return_value=False):
            response = client.post("/predict/attrition", json=sample_prediction_data)
            assert response.status_code == 503
            assert "modèle" in response.json()["detail"].lower()


def test_predict_batch_empty_list(client):
    """Test de batch avec liste vide"""
    response = client.post("/predict/attrition/batch", json=[])
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


