"""
Point d'entrée pour Hugging Face Spaces
Adapté pour le port 7860 utilisé par Hugging Face
"""
from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7860
    )


