# Guide d'Utilisation de l'API

## Vue d'ensemble

Cette API REST permet de prédire le risque d'attrition des employés à l'aide d'un modèle de machine learning.

## Base URL

- **Local** : `http://localhost:8000`
- **Production** : (à définir selon le déploiement)

## Documentation Interactive

Une fois l'API démarrée, accédez à :
- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

## Endpoints

### 1. Health Check

Vérifier l'état de l'API, du modèle et de la base de données.

**Endpoint** : `GET /health`

**Réponse** :
```json
{
  "status": "healthy",
  "message": "API opérationnelle",
  "model_loaded": true,
  "database_connected": true,
  "version": "1.0.0"
}
```

**Exemple avec curl** :
```bash
curl http://localhost:8000/health
```

### 2. Prédiction d'Attrition (Simple)

Prédire le risque d'attrition pour un employé.

**Endpoint** : `POST /predict/attrition`

**Corps de la requête** :
```json
{
  "employee_id": 123,
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
```

**Réponse** :
```json
{
  "prediction": 1,
  "probability": 0.75,
  "probability_class_0": 0.25,
  "probability_class_1": 0.75,
  "class_name": "Attrition",
  "seuil_utilise": 0.5,
  "employee_id": 123,
  "prediction_id": 42
}
```

**Exemple avec curl** :
```bash
curl -X POST "http://localhost:8000/predict/attrition" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 123,
    "age": 32,
    "revenu_mensuel": 75000,
    "nombre_heures_travailless": 45,
    "annees_dans_l_entreprise": 5
  }'
```

**Codes de réponse** :
- `200` : Prédiction réussie
- `400` : Erreur de validation des données
- `503` : Modèle non disponible

### 3. Prédiction d'Attrition (Batch)

Prédire le risque d'attrition pour plusieurs employés en une seule requête.

**Endpoint** : `POST /predict/attrition/batch`

**Corps de la requête** :
```json
[
  {
    "employee_id": 123,
    "age": 32,
    "revenu_mensuel": 75000,
    ...
  },
  {
    "employee_id": 124,
    "age": 28,
    "revenu_mensuel": 65000,
    ...
  }
]
```

**Réponse** :
```json
[
  {
    "prediction": 1,
    "probability": 0.75,
    "class_name": "Attrition",
    "employee_id": 123,
    "prediction_id": 42
  },
  {
    "prediction": 0,
    "probability": 0.30,
    "class_name": "Pas d'attrition",
    "employee_id": 124,
    "prediction_id": 43
  }
]
```

### 4. Historique des Prédictions

Récupérer l'historique des prédictions.

**Endpoint** : `GET /predict/history`

**Paramètres de requête** :
- `employee_id` (optionnel) : Filtrer par ID d'employé
- `limit` (optionnel, défaut: 100) : Nombre maximum de résultats

**Exemple** :
```
GET /predict/history?employee_id=123&limit=50
```

**Réponse** :
```json
[
  {
    "id": 42,
    "employee_id": 123,
    "prediction": 1,
    "probability": 0.75,
    "class_name": "Attrition",
    "created_at": "2025-12-03T22:00:00",
    "model_version": "1.0.0"
  },
  ...
]
```

## Authentification (Future)

L'authentification JWT sera implémentée pour sécuriser les endpoints.

**Exemple** :
```bash
# Obtenir un token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'

# Utiliser le token
curl -X POST "http://localhost:8000/predict/attrition" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## Gestion des Erreurs

L'API retourne des codes d'erreur HTTP standards :

- `400 Bad Request` : Données invalides
- `401 Unauthorized` : Authentification requise
- `404 Not Found` : Ressource introuvable
- `500 Internal Server Error` : Erreur serveur
- `503 Service Unavailable` : Modèle non disponible

**Format d'erreur** :
```json
{
  "detail": "Description de l'erreur"
}
```

## Exemples d'Utilisation

### Python

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Prédiction
data = {
    "employee_id": 123,
    "age": 32,
    "revenu_mensuel": 75000,
    "nombre_heures_travailless": 45,
    "annees_dans_l_entreprise": 5
}
response = requests.post(
    "http://localhost:8000/predict/attrition",
    json=data
)
result = response.json()
print(f"Prédiction: {result['class_name']}")
print(f"Probabilité: {result['probability']}")
```

### JavaScript (Fetch)

```javascript
// Prédiction
const data = {
  employee_id: 123,
  age: 32,
  revenu_mensuel: 75000,
  nombre_heures_travailless: 45,
  annees_dans_l_entreprise: 5
};

fetch('http://localhost:8000/predict/attrition', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
  console.log('Prédiction:', result.class_name);
  console.log('Probabilité:', result.probability);
});
```

## Validation des Données

Toutes les données d'entrée sont validées avec Pydantic :

- Types de données vérifiés
- Valeurs requises
- Formats validés
- Contraintes respectées

En cas d'erreur de validation, l'API retourne un `400 Bad Request` avec les détails.

## Performances

- Temps de réponse moyen : < 500ms
- Support du batch processing
- Historique paginé (limit par défaut: 100)












