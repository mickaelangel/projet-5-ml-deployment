"""
Chargeur de modèle pour l'API
"""
import joblib
import pickle
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np
from app.core.config import get_settings

settings = get_settings()


class ModelLoader:
    """Charge le modèle d'attrition et ses dépendances"""
    
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_names_original = None
        self.feature_names_transformed = None
        self.seuil_info = None
        self.metadata = None
        self.base_dir = Path("models")
        
    def load(self) -> bool:
        """Charge le modèle, le préprocesseur et les métadonnées"""
        try:
            # Charger le pipeline complet
            model_path = self.base_dir / "attrition_model_pipeline.pkl"
            if model_path.exists():
                self.model = joblib.load(model_path)
                print("✅ Modèle chargé avec succès")
            else:
                print(f"⚠️  Modèle non trouvé à {model_path}")
                print("💡 Le modèle sera créé lors de l'utilisation avec des données d'exemple")
                return False
            
            # Charger le préprocesseur
            preprocessor_path = self.base_dir / "preprocessor.pkl"
            if preprocessor_path.exists():
                self.preprocessor = joblib.load(preprocessor_path)
                print("✅ Préprocesseur chargé avec succès")
            
            # Charger les noms de features
            features_original_path = self.base_dir / "feature_names_original.pkl"
            if features_original_path.exists():
                with open(features_original_path, 'rb') as f:
                    self.feature_names_original = pickle.load(f)
                print("✅ Noms de features originaux chargés")
            
            features_transformed_path = self.base_dir / "feature_names_transformed.pkl"
            if features_transformed_path.exists():
                with open(features_transformed_path, 'rb') as f:
                    self.feature_names_transformed = pickle.load(f)
                print("✅ Noms de features transformés chargés")
            
            # Charger le seuil optimal
            seuil_path = self.base_dir / "seuil_info.pkl"
            if seuil_path.exists():
                with open(seuil_path, 'rb') as f:
                    self.seuil_info = pickle.load(f)
                print("✅ Informations de seuil chargées")
            
            # Charger les métadonnées
            metadata_path = self.base_dir / "model_metadata.pkl"
            if metadata_path.exists():
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                print("✅ Métadonnées chargées")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
            return False
    
    def predict(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Fait une prédiction avec le modèle
        
        Args:
            data: DataFrame avec les features
            
        Returns:
            Dictionnaire avec prediction, probability, class_name
        """
        if self.model is None:
            raise ValueError("Modèle non chargé. Appelez load() d'abord.")
        
        try:
            # Faire la prédiction avec le pipeline complet
            # Le pipeline inclut déjà le preprocessing et SMOTE
            prediction = self.model.predict(data)
            probability = self.model.predict_proba(data)
            
            # Utiliser le seuil optimal si disponible
            seuil = self.seuil_info.get('seuil_optimal', 0.5) if self.seuil_info else 0.5
            
            # Ajuster la prédiction selon le seuil
            proba_attrition = probability[0][1]  # Probabilité d'attrition
            prediction_ajustee = 1 if proba_attrition >= seuil else 0
            
            return {
                'prediction': int(prediction_ajustee),
                'probability': float(proba_attrition),
                'probability_class_0': float(probability[0][0]),
                'probability_class_1': float(probability[0][1]),
                'class_name': 'Attrition' if prediction_ajustee == 1 else 'Pas d\'attrition',
                'seuil_utilise': seuil
            }
        except Exception as e:
            raise ValueError(f"Erreur lors de la prédiction: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Vérifie si le modèle est chargé"""
        return self.model is not None


# Instance globale du chargeur de modèle
model_loader = ModelLoader()


