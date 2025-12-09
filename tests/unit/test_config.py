"""
Tests unitaires pour la configuration
"""
import pytest
from app.core.config import Settings, get_settings


def test_settings_default_values():
    """Test des valeurs par défaut de Settings"""
    settings = Settings()
    
    assert settings.API_TITLE == "API Prédiction Attrition"
    assert settings.API_VERSION == "1.0.0"
    assert settings.DATABASE_URL is not None
    assert settings.SECRET_KEY is not None


def test_get_settings_cached():
    """Test que get_settings utilise le cache"""
    settings1 = get_settings()
    settings2 = get_settings()
    
    # Devrait retourner la même instance (cached)
    assert settings1 is settings2








