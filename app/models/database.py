"""
Modèles de base de données SQLAlchemy
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.core.config import get_settings

settings = get_settings()

# Créer le moteur SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Vérifie les connexions avant de les utiliser
    echo=settings.DEBUG   # Log les requêtes SQL en mode debug
)

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles
Base = declarative_base()


class Prediction(Base):
    """Modèle pour stocker les prédictions d'attrition"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=True, index=True)
    
    # Données d'entrée (stockées en JSON)
    input_data = Column(JSON, nullable=False)
    
    # Résultats de la prédiction
    prediction = Column(Integer, nullable=False)  # 0 = Pas d'attrition, 1 = Attrition
    probability = Column(Float, nullable=False)   # Probabilité d'attrition (0-1)
    class_name = Column(String, nullable=False)   # "Attrition" ou "Pas d'attrition"
    
    # Métadonnées
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    model_version = Column(String, default="1.0.0")
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, employee_id={self.employee_id}, prediction={self.prediction})>"


class User(Base):
    """Modèle pour les utilisateurs de l'API (authentification)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_tables():
    """Crée toutes les tables dans la base de données"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès")


def get_db():
    """Dependency pour obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


