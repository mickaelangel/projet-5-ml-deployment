"""
Schémas Pydantic pour la validation des données
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class PredictRequest(BaseModel):
    """Schéma pour les données d'entrée d'une prédiction"""
    
    # Informations de base
    employee_id: Optional[int] = Field(None, description="ID de l'employé (optionnel)")
    
    # Données démographiques
    age: int = Field(..., ge=18, le=100, description="Âge de l'employé")
    statut_marital: Optional[str] = Field(None, description="Statut marital")
    
    # Informations professionnelles
    revenu_mensuel: float = Field(..., ge=0, description="Revenu mensuel")
    nombre_heures_travailless: float = Field(..., ge=0, description="Nombre d'heures travaillées")
    annees_dans_l_entreprise: float = Field(..., ge=0, description="Années dans l'entreprise")
    annees_dans_le_poste_actuel: Optional[float] = Field(None, ge=0)
    annee_experience_totale: Optional[float] = Field(None, ge=0)
    
    # Poste et département
    poste: Optional[str] = Field(None, description="Poste occupé")
    department: Optional[str] = Field(None, description="Département")
    
    # Satisfaction
    satisfaction_employee_environnement: Optional[float] = Field(None, ge=0, le=5)
    satisfaction_employee_equilibre_pro_perso: Optional[float] = Field(None, ge=0, le=5)
    satisfaction_employee_nature_travail: Optional[float] = Field(None, ge=0, le=5)
    
    # Autres facteurs
    heure_supplementaires: Optional[int] = Field(None, ge=0, le=1)
    nombre_experiences_precedentes: Optional[int] = Field(None, ge=0)
    annees_depuis_la_derniere_promotion: Optional[float] = Field(None, ge=0)
    distance_domicile_travail: Optional[float] = Field(None, ge=0)
    frequence_deplacement: Optional[str] = None
    ayant_enfants: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "employee_id": 1,
                "age": 32,
                "statut_marital": "Marié(e)",
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
        }


class PredictResponse(BaseModel):
    """Schéma pour la réponse d'une prédiction"""
    prediction: int = Field(..., description="0 = Pas d'attrition, 1 = Attrition")
    probability: float = Field(..., ge=0, le=1, description="Probabilité d'attrition")
    probability_class_0: float = Field(..., ge=0, le=1, description="Probabilité de rester")
    probability_class_1: float = Field(..., ge=0, le=1, description="Probabilité de partir")
    class_name: str = Field(..., description="Nom de la classe prédite")
    seuil_utilise: float = Field(..., description="Seuil utilisé pour la décision")
    employee_id: Optional[int] = Field(None, description="ID de l'employé")
    prediction_id: Optional[int] = Field(None, description="ID de la prédiction en base")
    
    class Config:
        schema_extra = {
            "example": {
                "prediction": 1,
                "probability": 0.85,
                "probability_class_0": 0.15,
                "probability_class_1": 0.85,
                "class_name": "Attrition",
                "seuil_utilise": 0.72,
                "employee_id": 1,
                "prediction_id": 123
            }
        }


class PredictionHistory(BaseModel):
    """Schéma pour l'historique des prédictions"""
    id: int
    employee_id: Optional[int]
    prediction: int
    probability: float
    class_name: str
    created_at: datetime
    model_version: str
    
    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Schéma pour le health check"""
    status: str
    message: str
    model_loaded: bool
    database_connected: bool
    version: str


class ErrorResponse(BaseModel):
    """Schéma pour les erreurs"""
    error: str
    detail: Optional[str] = None


