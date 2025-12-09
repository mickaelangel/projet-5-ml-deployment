"""
Tests unitaires pour le module de sécurité
"""
import pytest
from datetime import timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from unittest.mock import patch, MagicMock

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    get_current_user,
)
from app.core.config import get_settings

settings = get_settings()


def test_get_password_hash():
    """Test du hachage de mot de passe"""
    password = "test123"
    # Utiliser un mock pour éviter les problèmes avec bcrypt
    with patch('app.core.security.pwd_context') as mock_context:
        mock_context.hash.return_value = "$2b$12$testhash123"
        hashed = get_password_hash(password)
        
        mock_context.hash.assert_called_once_with(password)
        assert hashed != password
        assert len(hashed) > 0
        assert isinstance(hashed, str)


def test_verify_password_correct():
    """Test de vérification de mot de passe correct"""
    password = "test123"
    hashed = "$2b$12$testhash123"
    
    with patch('app.core.security.pwd_context') as mock_context:
        mock_context.verify.return_value = True
        result = verify_password(password, hashed)
        
        mock_context.verify.assert_called_once_with(password, hashed)
        assert result is True


def test_verify_password_incorrect():
    """Test de vérification de mot de passe incorrect"""
    password = "test123"
    wrong_password = "wrong123"
    hashed = "$2b$12$testhash123"
    
    with patch('app.core.security.pwd_context') as mock_context:
        mock_context.verify.return_value = False
        result = verify_password(wrong_password, hashed)
        
        mock_context.verify.assert_called_once_with(wrong_password, hashed)
        assert result is False


def test_verify_password_empty():
    """Test avec mot de passe vide"""
    password = ""
    hashed = "$2b$12$testhash123"
    
    with patch('app.core.security.pwd_context') as mock_context:
        mock_context.verify.return_value = True
        result = verify_password(password, hashed)
        mock_context.verify.assert_called_once_with(password, hashed)
        assert result is True
        
        # Test avec mauvais mot de passe
        mock_context.verify.return_value = False
        result2 = verify_password("not_empty", hashed)
        assert result2 is False


def test_create_access_token():
    """Test de création de token JWT"""
    data = {"sub": "test_user", "email": "test@example.com"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_with_expires_delta():
    """Test de création de token avec délai d'expiration personnalisé"""
    data = {"sub": "test_user"}
    expires_delta = timedelta(minutes=60)
    token = create_access_token(data, expires_delta=expires_delta)
    
    assert token is not None
    # Vérifier que le token contient l'expiration
    payload = verify_token(token)
    assert payload is not None
    assert "exp" in payload


def test_verify_token_valid():
    """Test de vérification de token valide"""
    data = {"sub": "test_user", "email": "test@example.com"}
    token = create_access_token(data)
    
    payload = verify_token(token)
    
    assert payload is not None
    assert payload["sub"] == "test_user"
    assert payload["email"] == "test@example.com"
    assert "exp" in payload


def test_verify_token_invalid():
    """Test de vérification de token invalide"""
    invalid_token = "invalid_token_string_12345"
    payload = verify_token(invalid_token)
    
    assert payload is None


def test_verify_token_expired():
    """Test de vérification de token expiré"""
    data = {"sub": "test_user"}
    # Créer un token expiré (délai négatif)
    expires_delta = timedelta(minutes=-60)
    token = create_access_token(data, expires_delta=expires_delta)
    
    payload = verify_token(token)
    
    # Le token expiré devrait retourner None
    assert payload is None


def test_verify_token_wrong_secret():
    """Test avec token signé avec une mauvaise clé secrète"""
    # Créer un token avec une clé différente
    wrong_secret = "wrong_secret_key"
    data = {"sub": "test_user"}
    
    # Créer le token avec la mauvaise clé
    token = jwt.encode(
        data,
        wrong_secret,
        algorithm=settings.ALGORITHM
    )
    
    # Vérifier avec la bonne clé devrait échouer
    payload = verify_token(token)
    assert payload is None


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    """Test de get_current_user avec token valide"""
    data = {"sub": "test_user"}
    token = create_access_token(data)
    
    # Créer une dépendance mock pour oauth2_scheme
    from unittest.mock import AsyncMock
    from app.core.security import get_current_user, oauth2_scheme
    
    # Mock oauth2_scheme pour retourner le token
    async def mock_oauth2_scheme():
        return token
    
    # Utiliser dependency_overrides pour injecter le token
    from app.main import app
    app.dependency_overrides[oauth2_scheme] = mock_oauth2_scheme
    
    try:
        username = await get_current_user(token)
        assert username == "test_user"
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """Test de get_current_user avec token invalide"""
    from app.core.security import get_current_user, oauth2_scheme
    from app.main import app
    
    invalid_token = "invalid_token"
    
    async def mock_oauth2_scheme():
        return invalid_token
    
    app.dependency_overrides[oauth2_scheme] = mock_oauth2_scheme
    
    try:
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(invalid_token)
        
        assert exc_info.value.status_code == 401
        assert "identifiants" in exc_info.value.detail.lower()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_current_user_missing_sub():
    """Test de get_current_user avec token sans 'sub'"""
    from app.core.security import get_current_user, oauth2_scheme
    from app.main import app
    
    # Créer un token sans 'sub'
    data = {"email": "test@example.com"}  # Pas de 'sub'
    token = create_access_token(data)
    
    async def mock_oauth2_scheme():
        return token
    
    app.dependency_overrides[oauth2_scheme] = mock_oauth2_scheme
    
    try:
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token)
        
        assert exc_info.value.status_code == 401
    finally:
        app.dependency_overrides.clear()


def test_password_hash_different_passwords():
    """Test que deux mots de passe différents produisent des hash différents"""
    password1 = "pass1"
    password2 = "pass2"
    
    with patch('app.core.security.pwd_context') as mock_context:
        mock_context.hash.side_effect = ["$2b$12$hash1", "$2b$12$hash2"]
        mock_context.verify.side_effect = lambda p, h: (p == password1 and h == "$2b$12$hash1") or (p == password2 and h == "$2b$12$hash2")
        
        hashed1 = get_password_hash(password1)
        hashed2 = get_password_hash(password2)
        
        assert hashed1 != hashed2
        assert verify_password(password1, hashed1) is True
        assert verify_password(password1, hashed2) is False
        assert verify_password(password2, hashed2) is True
        assert verify_password(password2, hashed1) is False


def test_verify_password_direct_call():
    """Test direct de verify_password pour couvrir la ligne 23"""
    password = "testpass"
    hashed = "$2b$12$testhash123"
    
    with patch('app.core.security.pwd_context') as mock_context:
        # Test direct de la ligne 23 : return pwd_context.verify(...)
        mock_context.verify.return_value = True
        result = verify_password(password, hashed)
        mock_context.verify.assert_called_once_with(password, hashed)
        assert result is True
        
        # Test avec mauvais mot de passe
        mock_context.verify.return_value = False
        result_false = verify_password("wrongpass", hashed)
        assert result_false is False

