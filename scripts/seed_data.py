"""
Script pour insérer des données d'exemple dans la base de données
"""
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.database import SessionLocal, Prediction
import json

def main():
    """Insère des données d'exemple"""
    db = SessionLocal()
    
    try:
        print("=" * 50)
        print("Insertion de données d'exemple")
        print("=" * 50)
        
        # Exemples de prédictions
        examples = [
            {
                "employee_id": 1,
                "input_data": {
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
                },
                "prediction": 1,
                "probability": 0.85,
                "class_name": "Attrition"
            },
            {
                "employee_id": 2,
                "input_data": {
                    "age": 45,
                    "revenu_mensuel": 95000,
                    "nombre_heures_travailless": 40,
                    "annees_dans_l_entreprise": 10,
                    "annees_dans_le_poste_actuel": 5,
                    "annee_experience_totale": 15,
                    "poste": "Manager",
                    "department": "Sales",
                    "satisfaction_employee_environnement": 4.5,
                    "satisfaction_employee_equilibre_pro_perso": 4.0,
                    "satisfaction_employee_nature_travail": 4.5,
                    "heure_supplementaires": 0,
                    "nombre_experiences_precedentes": 1,
                    "annees_depuis_la_derniere_promotion": 1.0,
                    "distance_domicile_travail": 5,
                    "frequence_deplacement": "Non",
                    "ayant_enfants": "Non"
                },
                "prediction": 0,
                "probability": 0.15,
                "class_name": "Pas d'attrition"
            }
        ]
        
        for example in examples:
            prediction = Prediction(
                employee_id=example["employee_id"],
                input_data=example["input_data"],
                prediction=example["prediction"],
                probability=example["probability"],
                class_name=example["class_name"],
                model_version="1.0.0"
            )
            db.add(prediction)
        
        db.commit()
        print(f"\n✅ {len(examples)} exemples insérés avec succès")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur lors de l'insertion: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()











