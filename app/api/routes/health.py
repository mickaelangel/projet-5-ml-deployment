"""
Route de health check
"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from ml.model_loader import model_loader
from sqlalchemy import create_engine, text
from app.core.config import get_settings

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Vérifie l'état de l'API, du modèle et de la base de données
    """
    # Vérifier le modèle
    model_loaded = model_loader.is_loaded()
    
    # Vérifier la base de données
    database_connected = False
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            database_connected = True
    except Exception:
        database_connected = False
    
    status = "healthy" if (model_loaded and database_connected) else "degraded"
    message = "API opérationnelle" if status == "healthy" else "API fonctionnelle mais certaines dépendances ne sont pas disponibles"
    
    return HealthResponse(
        status=status,
        message=message,
        model_loaded=model_loaded,
        database_connected=database_connected,
        version=settings.API_VERSION
    )


