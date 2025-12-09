"""
Tests unitaires pour le préprocesseur
"""
import pytest
import pandas as pd
from ml.preprocessor import AttritionPreprocessor


def test_prepare_features_with_valid_data():
    """Test de préparation de features avec données valides"""
    preprocessor = AttritionPreprocessor()
    data = {
        "age": 30,
        "revenu_mensuel": 50000,
        "nombre_heures_travailless": 40,
        "annees_dans_l_entreprise": 5
    }
    
    df = preprocessor.prepare_features(data)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "age" in df.columns or len(df.columns) > 0


def test_prepare_features_with_missing_fields():
    """Test avec des champs manquants"""
    preprocessor = AttritionPreprocessor()
    data = {
        "age": 30,
        "revenu_mensuel": 50000
        # Manque d'autres champs
    }
    
    df = preprocessor.prepare_features(data)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1


def test_validate_input_valid_data():
    """Test de validation avec données valides"""
    preprocessor = AttritionPreprocessor()
    data = {
        "age": 30,
        "revenu_mensuel": 50000,
        "nombre_heures_travailless": 40,
        "annees_dans_l_entreprise": 5
    }
    
    is_valid, errors = preprocessor.validate_input(data)
    
    assert is_valid is True
    assert len(errors) == 0


def test_validate_input_not_dict():
    """Test avec données qui ne sont pas un dictionnaire"""
    preprocessor = AttritionPreprocessor()
    
    is_valid, errors = preprocessor.validate_input("not a dict")
    
    assert is_valid is False
    assert len(errors) > 0
    assert any("dictionnaire" in error.lower() for error in errors)


def test_validate_input_missing_required_fields():
    """Test avec champs requis manquants"""
    preprocessor = AttritionPreprocessor()
    data = {
        "age": 30
        # Manque revenu_mensuel, nombre_heures_travailless, etc.
    }
    
    is_valid, errors = preprocessor.validate_input(data)
    
    assert is_valid is False
    assert len(errors) > 0


def test_validate_input_invalid_age():
    """Test avec âge invalide"""
    preprocessor = AttritionPreprocessor()
    
    # Âge trop jeune
    data = {
        "age": 10,  # < 18
        "revenu_mensuel": 50000,
        "nombre_heures_travailless": 40,
        "annees_dans_l_entreprise": 5
    }
    is_valid, errors = preprocessor.validate_input(data)
    assert is_valid is False
    
    # Âge trop vieux
    data = {
        "age": 150,  # > 100
        "revenu_mensuel": 50000,
        "nombre_heures_travailless": 40,
        "annees_dans_l_entreprise": 5
    }
    is_valid, errors = preprocessor.validate_input(data)
    assert is_valid is False


def test_validate_input_invalid_revenu():
    """Test avec revenu invalide"""
    preprocessor = AttritionPreprocessor()
    data = {
        "age": 30,
        "revenu_mensuel": -1000,  # Négatif
        "nombre_heures_travailless": 40,
        "annees_dans_l_entreprise": 5
    }
    
    is_valid, errors = preprocessor.validate_input(data)
    
    assert is_valid is False
    assert len(errors) > 0


def test_validate_input_valid_age_boundaries():
    """Test avec âge aux limites valides"""
    preprocessor = AttritionPreprocessor()
    
    # Âge minimum
    data = {
        "age": 18,
        "revenu_mensuel": 50000,
        "nombre_heures_travailless": 40,
        "annees_dans_l_entreprise": 5
    }
    is_valid, _ = preprocessor.validate_input(data)
    assert is_valid is True
    
    # Âge maximum
    data = {
        "age": 100,
        "revenu_mensuel": 50000,
        "nombre_heures_travailless": 40,
        "annees_dans_l_entreprise": 5
    }
    is_valid, _ = preprocessor.validate_input(data)
    assert is_valid is True







