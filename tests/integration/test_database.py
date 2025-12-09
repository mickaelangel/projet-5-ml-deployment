"""
Tests d'intégration pour la base de données
"""
import pytest
from app.models.database import Prediction
from datetime import datetime
import json


def test_create_prediction(db):
    """Test de création d'une prédiction en base"""
    prediction = Prediction(
        employee_id=1,
        input_data={"age": 30, "revenu_mensuel": 50000},
        prediction=0,
        probability=0.25,
        class_name="Pas d'attrition",
        model_version="1.0.0"
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    assert prediction.id is not None
    assert prediction.employee_id == 1
    assert prediction.prediction == 0
    assert prediction.probability == 0.25


def test_query_predictions_by_employee(db):
    """Test de requête par ID d'employé"""
    # Créer plusieurs prédictions
    for emp_id in [1, 1, 2]:
        prediction = Prediction(
            employee_id=emp_id,
            input_data={"test": "data"},
            prediction=1,
            probability=0.8,
            class_name="Attrition"
        )
        db.add(prediction)
    
    db.commit()
    
    # Requêter par employee_id
    predictions = db.query(Prediction).filter(Prediction.employee_id == 1).all()
    assert len(predictions) == 2


def test_prediction_json_data(db):
    """Test que les données JSON sont bien stockées"""
    input_data = {
        "age": 35,
        "revenu_mensuel": 75000,
        "poste": "Consultant"
    }
    
    prediction = Prediction(
        employee_id=1,
        input_data=input_data,
        prediction=1,
        probability=0.85,
        class_name="Attrition"
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    assert prediction.input_data == input_data
    assert isinstance(prediction.input_data, dict)


