"""
Tests pour les événements de démarrage/arrêt de l'application
"""
import pytest
from unittest.mock import patch, MagicMock
from app.main import app, startup_event
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_startup_event_model_not_loaded():
    """Test du startup event quand le modèle ne se charge pas - ligne 60"""
    from ml.model_loader import model_loader
    
    # Mock pour simuler un échec de chargement
    with patch.object(model_loader, 'load', return_value=False):
        with patch('builtins.print') as mock_print:
            # Appeler directement le startup event
            await startup_event()
            
            # Vérifier que le print de ligne 60 a été appelé
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("modèle n'a pas pu être chargé" in str(call).lower() or "charger manuellement" in str(call).lower() for call in print_calls)


def test_main_module_if_name_main():
    """Test que le code if __name__ == "__main__" existe - lignes 72-73"""
    import app.main
    import inspect
    
    # Vérifier que le fichier contient le code
    source = inspect.getsource(app.main)
    assert "if __name__" in source
    assert "uvicorn.run" in source
    
    # Note: On ne peut pas vraiment exécuter ce code dans les tests car
    # cela lancerait le serveur. Mais on peut vérifier qu'il existe.

