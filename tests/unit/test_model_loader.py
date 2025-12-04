"""
Tests unitaires pour le chargeur de modèle
"""
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch
from ml.model_loader import ModelLoader


def test_model_loader_initialization():
    """Test d'initialisation du ModelLoader"""
    loader = ModelLoader()
    
    assert loader.model is None
    assert loader.preprocessor is None
    assert loader.feature_names_original is None
    assert loader.feature_names_transformed is None
    assert loader.seuil_info is None
    assert loader.metadata is None
    assert isinstance(loader.base_dir, Path)


def test_is_loaded_false():
    """Test de is_loaded quand le modèle n'est pas chargé"""
    loader = ModelLoader()
    
    assert loader.is_loaded() is False


def test_is_loaded_true():
    """Test de is_loaded quand le modèle est chargé"""
    loader = ModelLoader()
    loader.model = Mock()  # Simuler un modèle chargé
    
    assert loader.is_loaded() is True


def test_load_model_not_found(tmp_path, monkeypatch):
    """Test lorsque le modèle n'est pas trouvé"""
    loader = ModelLoader()
    loader.base_dir = tmp_path / "nonexistent"
    
    result = loader.load()
    
    assert result is False
    assert loader.model is None


def test_predict_without_loading():
    """Test de prédiction sans avoir chargé le modèle"""
    loader = ModelLoader()
    data = pd.DataFrame([{"age": 30, "revenu_mensuel": 50000}])
    
    with pytest.raises(ValueError, match="Modèle non chargé"):
        loader.predict(data)


def test_predict_with_loaded_model():
    """Test de prédiction avec modèle chargé (mock)"""
    loader = ModelLoader()
    
    # Créer un mock du modèle
    mock_model = Mock()
    mock_model.predict.return_value = [1]
    mock_model.predict_proba.return_value = [[0.2, 0.8]]
    
    loader.model = mock_model
    loader.seuil_info = {"seuil_optimal": 0.5}
    
    data = pd.DataFrame([{"age": 30, "revenu_mensuel": 50000}])
    
    result = loader.predict(data)
    
    assert result is not None
    assert "prediction" in result
    assert "probability" in result
    assert "class_name" in result
    assert result["prediction"] in [0, 1]
    assert 0 <= result["probability"] <= 1


def test_predict_with_different_threshold():
    """Test de prédiction avec différents seuils"""
    loader = ModelLoader()
    
    mock_model = Mock()
    mock_model.predict.return_value = [0]
    mock_model.predict_proba.return_value = [[0.6, 0.4]]  # 40% probabilité d'attrition
    
    loader.model = mock_model
    
    # Seuil bas (0.3) - devrait prédire attrition
    loader.seuil_info = {"seuil_optimal": 0.3}
    data = pd.DataFrame([{"age": 30}])
    result = loader.predict(data)
    assert result["prediction"] == 1  # Au-dessus du seuil
    
    # Seuil haut (0.5) - devrait prédire pas d'attrition
    loader.seuil_info = {"seuil_optimal": 0.5}
    result = loader.predict(data)
    assert result["prediction"] == 0  # En-dessous du seuil


def test_predict_without_seuil_info():
    """Test de prédiction sans seuil_info (utilise 0.5 par défaut)"""
    loader = ModelLoader()
    
    mock_model = Mock()
    mock_model.predict.return_value = [0]
    mock_model.predict_proba.return_value = [[0.6, 0.4]]
    
    loader.model = mock_model
    loader.seuil_info = None  # Pas de seuil
    
    data = pd.DataFrame([{"age": 30}])
    result = loader.predict(data)
    
    assert result is not None
    assert result["seuil_utilise"] == 0.5  # Seuil par défaut


def test_predict_error_handling():
    """Test de gestion d'erreur lors de la prédiction"""
    loader = ModelLoader()
    
    mock_model = Mock()
    mock_model.predict.side_effect = Exception("Erreur de prédiction")
    
    loader.model = mock_model
    
    data = pd.DataFrame([{"age": 30}])
    
    with pytest.raises(ValueError, match="Erreur lors de la prédiction"):
        loader.predict(data)


def test_load_with_exception():
    """Test de load() quand une exception est levée (lignes 75-77)"""
    loader = ModelLoader()
    
    # Simuler une exception lors du chargement du modèle
    with patch('joblib.load', side_effect=Exception("Erreur de chargement")):
        with patch('builtins.print'):
            result = loader.load()
            assert result is False
            assert loader.model is None


def test_load_with_file_not_found():
    """Test de load() quand les fichiers n'existent pas"""
    loader = ModelLoader()
    loader.base_dir = Path("/nonexistent/path")
    
    with patch('builtins.print'):
        result = loader.load()
        assert result is False

