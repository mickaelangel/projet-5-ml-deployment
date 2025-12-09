"""
Routes pour les prédictions d'attrition
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import pandas as pd

from app.models.schemas import PredictRequest, PredictResponse
from app.models.database import get_db, Prediction
from ml.model_loader import model_loader
from ml.preprocessor import AttritionPreprocessor

router = APIRouter(prefix="/predict", tags=["predictions"])

# Initialiser le préprocesseur
preprocessor = AttritionPreprocessor()


@router.post("/attrition", response_model=PredictResponse)
async def predict_attrition(
    request: PredictRequest,
    db: Session = Depends(get_db)
):
    """
    Prédit le risque d'attrition d'un employé
    
    - **employee_id**: ID de l'employé (optionnel)
    - **age**: Âge de l'employé
    - **revenu_mensuel**: Revenu mensuel
    - **nombre_heures_travailless**: Nombre d'heures travaillées
    - Et autres features...
    
    Retourne la prédiction avec la probabilité d'attrition.
    """
    try:
        # Vérifier que le modèle est chargé
        if not model_loader.is_loaded():
            # Tentative de chargement
            model_loaded = model_loader.load()
            if not model_loaded:
                raise HTTPException(
                    status_code=503,
                    detail="Le modèle n'est pas disponible. Veuillez charger le modèle d'abord."
                )
        
        # Convertir la requête en dictionnaire
        data = request.dict(exclude_none=True)
        
        # Valider les données
        is_valid, errors = preprocessor.validate_input(data)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Erreurs de validation: {', '.join(errors)}")
        
        # Préprocesser les données
        processed_data = preprocessor.prepare_features(data)
        
        # Faire la prédiction
        result = model_loader.predict(processed_data)
        
        # Sauvegarder la prédiction en base de données
        db_prediction = Prediction(
            employee_id=request.employee_id,
            input_data=data,
            prediction=result['prediction'],
            probability=result['probability'],
            class_name=result['class_name'],
            model_version=model_loader.metadata.get('model_version', '1.0.0') if model_loader.metadata else '1.0.0'
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        # Ajouter l'ID de la prédiction à la réponse
        result['employee_id'] = request.employee_id
        result['prediction_id'] = db_prediction.id
        
        return PredictResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}")


@router.post("/attrition/batch", response_model=List[PredictResponse])
async def predict_attrition_batch(
    requests: List[PredictRequest],
    db: Session = Depends(get_db)
):
    """
    Prédit le risque d'attrition pour plusieurs employés en une seule requête
    """
    results = []
    
    for request in requests:
        try:
            # Utiliser la fonction de prédiction unique
            response = await predict_attrition(request, db)
            results.append(response)
        except Exception as e:
            # Continuer avec les autres même en cas d'erreur
            results.append(PredictResponse(
                prediction=-1,
                probability=0.0,
                probability_class_0=0.0,
                probability_class_1=0.0,
                class_name=f"Erreur: {str(e)}",
                seuil_utilise=0.5,
                employee_id=request.employee_id
            ))
    
    return results


@router.get("/history", response_model=List[dict])
async def get_prediction_history(
    employee_id: int = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère l'historique des prédictions
    
    - **employee_id**: Filtrer par ID d'employé (optionnel)
    - **limit**: Nombre maximum de résultats (défaut: 100)
    """
    query = db.query(Prediction)
    
    if employee_id:
        query = query.filter(Prediction.employee_id == employee_id)
    
    predictions = query.order_by(Prediction.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": p.id,
            "employee_id": p.employee_id,
            "prediction": p.prediction,
            "probability": p.probability,
            "class_name": p.class_name,
            "created_at": p.created_at.isoformat(),
            "model_version": p.model_version
        }
        for p in predictions
    ]


