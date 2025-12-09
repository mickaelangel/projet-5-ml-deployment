"""
Configuration de l'application
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuration de l'application via variables d'environnement"""
    
    # Base de données
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ml_db"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "API Prédiction Attrition"
    API_DESCRIPTION: str = "API pour prédire le risque d'attrition des employés"
    API_VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-use-env-var"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Model
    MODEL_PATH: str = "models/attrition_model_pipeline.pkl"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Récupère la configuration (mise en cache)"""
    return Settings()


