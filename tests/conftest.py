"""
Configuration globale pour les tests pytest
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.database import Base, get_db
from app.core.config import Settings

# Base de données de test (SQLite en mémoire)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Crée une session de base de données de test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Client de test pour l'API"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_prediction_data():
    """Données d'exemple pour les tests de prédiction"""
    return {
        "employee_id": 1,
        "age": 32,
        "revenu_mensuel": 75000,
        "nombre_heures_travailless": 45,
        "annees_dans_l_entreprise": 5,
        "annees_dans_le_poste_actuel": 2,
        "annee_experience_totale": 8,
        "poste": "Consultant",
        "department": "Consulting",
        "satisfaction_employee_environnement": 3.5,
        "satisfaction_employee_equilibre_pro_perso": 3.0,
        "satisfaction_employee_nature_travail": 4.0,
        "heure_supplementaires": 1,
        "nombre_experiences_precedentes": 2,
        "annees_depuis_la_derniere_promotion": 2.5,
        "distance_domicile_travail": 10,
        "frequence_deplacement": "Rare",
        "ayant_enfants": "Oui"
    }


