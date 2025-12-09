"""
Préprocesseur des données pour le modèle d'attrition
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from pathlib import Path
import pickle


class AttritionPreprocessor:
    """Préprocesse les données avant la prédiction"""
    
    def __init__(self, feature_names: Optional[List[str]] = None):
        self.feature_names = feature_names
        self.base_dir = Path("models")
        
        # Charger les noms de features si disponibles
        if feature_names is None:
            features_path = self.base_dir / "feature_names_original.pkl"
            if features_path.exists():
                with open(features_path, 'rb') as f:
                    self.feature_names = pickle.load(f)
    
    def prepare_features(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Convertit les données d'entrée en DataFrame avec les bonnes colonnes
        
        Args:
            data: Dictionnaire avec les données d'entrée
            
        Returns:
            DataFrame prêt pour le modèle
        """
        # Créer un DataFrame
        df = pd.DataFrame([data])
        
        # Si on a les noms de features attendus, réorganiser les colonnes
        if self.feature_names:
            # Ajouter les colonnes manquantes avec des valeurs par défaut
            for col in self.feature_names:
                if col not in df.columns:
                    df[col] = 0  # Valeur par défaut
            
            # Réorganiser les colonnes dans l'ordre attendu
            df = df.reindex(columns=self.feature_names, fill_value=0)
        
        return df
    
    def validate_input(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Valide les données d'entrée
        
        Returns:
            Tuple (is_valid, list_of_errors)
        """
        errors = []
        
        # Vérifications de base
        if not isinstance(data, dict):
            errors.append("Les données doivent être un dictionnaire")
            return False, errors
        
        # Liste des champs requis (à adapter selon votre modèle)
        required_fields = [
            'age', 'revenu_mensuel', 'nombre_heures_travailless',
            'annees_dans_l_entreprise'
        ]
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Champ requis manquant: {field}")
        
        # Vérifications de type et valeurs
        if 'age' in data:
            if not isinstance(data['age'], (int, float)) or data['age'] < 18 or data['age'] > 100:
                errors.append("L'âge doit être un nombre entre 18 et 100")
        
        if 'revenu_mensuel' in data:
            if not isinstance(data['revenu_mensuel'], (int, float)) or data['revenu_mensuel'] < 0:
                errors.append("Le revenu mensuel doit être un nombre positif")
        
        return len(errors) == 0, errors

