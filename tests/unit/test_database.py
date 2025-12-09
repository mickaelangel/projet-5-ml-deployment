"""
Tests unitaires pour les modèles de base de données
"""
import pytest
from datetime import datetime
from app.models.database import Prediction, User, get_db, create_tables


def test_prediction_model_creation(db):
    """Test de création d'un modèle Prediction"""
    prediction = Prediction(
        employee_id=1,
        input_data={"age": 30, "revenu": 50000},
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
    assert prediction.class_name == "Pas d'attrition"
    assert prediction.model_version == "1.0.0"
    assert isinstance(prediction.created_at, datetime)


def test_prediction_without_employee_id(db):
    """Test de création de prédiction sans employee_id"""
    prediction = Prediction(
        input_data={"age": 30},
        prediction=1,
        probability=0.75,
        class_name="Attrition"
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    assert prediction.id is not None
    assert prediction.employee_id is None


def test_user_model_creation(db):
    """Test de création d'un modèle User"""
    # Utiliser un hash simple pour éviter les problèmes de bcrypt dans les tests
    simple_hash = "hashed_password_for_testing"
    
    user = User(
        username="test_user",
        email="test@example.com",
        hashed_password=simple_hash,
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    assert user.id is not None
    assert user.username == "test_user"
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)


def test_user_unique_username(db):
    """Test que le username doit être unique"""
    user1 = User(
        username="test_user",
        email="test1@example.com",
        hashed_password="hashed1"
    )
    
    db.add(user1)
    db.commit()
    
    user2 = User(
        username="test_user",  # Même username
        email="test2@example.com",
        hashed_password="hashed2"
    )
    
    db.add(user2)
    
    # Devrait lever une exception d'unicité
    with pytest.raises(Exception):  # IntegrityError ou similaire
        db.commit()


def test_get_db():
    """Test de la fonction get_db"""
    db_gen = get_db()
    db = next(db_gen)
    
    assert db is not None
    
    # Fermer proprement
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_prediction_repr(db):
    """Test de la représentation string de Prediction"""
    prediction = Prediction(
        employee_id=1,
        input_data={"test": "data"},
        prediction=1,
        probability=0.8,
        class_name="Attrition"
    )
    
    db.add(prediction)
    db.commit()
    
    repr_str = repr(prediction)
    assert "Prediction" in repr_str
    assert "1" in repr_str  # employee_id ou prediction


def test_create_tables():
    """Test de la fonction create_tables"""
    from app.models.database import create_tables
    from unittest.mock import patch
    
    with patch('app.models.database.Base.metadata.create_all') as mock_create:
        with patch('builtins.print'):
            create_tables()
            # Vérifier que create_all a été appelé
            mock_create.assert_called_once()

