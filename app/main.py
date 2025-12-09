"""
Application principale FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.core.config import get_settings
from app.api.routes import health, predict

# Charger la configuration
settings = get_settings()

# Créer l'application FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(health.router)
app.include_router(predict.router)


@app.get("/", include_in_schema=False)
async def root():
    """Redirige vers la documentation"""
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup_event():
    """Actions à effectuer au démarrage de l'API"""
    print("=" * 50)
    print(f"🚀 Démarrage de {settings.API_TITLE}")
    print(f"📖 Documentation: http://localhost:{settings.API_PORT}/docs")
    print(f"🔍 Environnement: {settings.ENVIRONMENT}")
    print("=" * 50)
    
    # Charger le modèle au démarrage
    from ml.model_loader import model_loader
    print("\n📦 Chargement du modèle...")
    model_loaded = model_loader.load()
    if model_loaded:
        print("✅ Modèle chargé avec succès")
    else:
        print("⚠️  Le modèle n'a pas pu être chargé. Vous devrez le charger manuellement.")
    print()


@app.on_event("shutdown")
async def shutdown_event():
    """Actions à effectuer à l'arrêt de l'API"""
    print("\n👋 Arrêt de l'API...")
    print("✅ Arrêt effectué")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )


