# Documentation des Tests

## Vue d'ensemble

Le projet utilise Pytest pour les tests unitaires et d'intégration. L'objectif est d'atteindre une couverture de code supérieure à 60%.

## Structure des Tests

```
tests/
├── conftest.py              # Configuration globale
├── unit/                    # Tests unitaires
│   ├── test_health.py      # Tests du health check
│   └── test_main.py        # Tests de l'application principale
└── integration/             # Tests d'intégration
    ├── test_predict.py     # Tests des prédictions
    └── test_database.py    # Tests de la base de données
```

## Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=60
```

### Fixtures Globales

Dans `conftest.py` :
- `db` : Session de base de données de test
- `client` : Client FastAPI pour les tests
- `sample_prediction_data` : Données d'exemple

## Lancer les Tests

### Tous les tests

```bash
pytest
```

### Avec couverture

```bash
pytest --cov=app --cov-report=html
```

Le rapport HTML sera généré dans `htmlcov/index.html`

### Tests spécifiques

```bash
# Tests unitaires uniquement
pytest tests/unit/

# Tests d'intégration uniquement
pytest tests/integration/

# Un fichier spécifique
pytest tests/unit/test_health.py

# Une fonction spécifique
pytest tests/unit/test_health.py::test_health_endpoint
```

### Mode verbeux

```bash
pytest -v
```

### Afficher les print

```bash
pytest -s
```

## Types de Tests

### Tests Unitaires

Testent des composants isolés.

**Exemple** :
```python
def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Tests d'Intégration

Testent l'interaction entre plusieurs composants.

**Exemple** :
```python
def test_predict_endpoint(client, sample_prediction_data):
    response = client.post(
        "/predict/attrition",
        json=sample_prediction_data
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
```

## Couverture de Code

### Vérifier la couverture

```bash
pytest --cov=app --cov-report=term-missing
```

### Rapport HTML

```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Couverture minimale

Le pipeline CI/CD exige un minimum de 60% de couverture.

## Exemples de Tests

### Test d'API

```python
def test_predict_attrition(client, sample_prediction_data):
    """Test de prédiction d'attrition"""
    response = client.post(
        "/predict/attrition",
        json=sample_prediction_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert data["prediction"] in [0, 1]
```

### Test de Base de Données

```python
def test_create_prediction(db):
    """Test de création d'une prédiction en BDD"""
    prediction = Prediction(
        employee_id=123,
        input_data={"age": 32},
        prediction=1,
        probability=0.75,
        class_name="Attrition"
    )
    
    db.add(prediction)
    db.commit()
    
    assert prediction.id is not None
    assert prediction.employee_id == 123
```

### Test de Validation

```python
def test_invalid_input(client):
    """Test avec des données invalides"""
    response = client.post(
        "/predict/attrition",
        json={"invalid": "data"}
    )
    
    assert response.status_code == 400
```

## Mocking

### Mocker le modèle ML

```python
from unittest.mock import patch

@patch('ml.model_loader.model_loader.predict')
def test_predict_with_mock(mock_predict, client):
    mock_predict.return_value = {
        'prediction': 1,
        'probability': 0.75
    }
    
    response = client.post("/predict/attrition", json={...})
    assert response.status_code == 200
```

## Tests de Performance

### Mesurer le temps de réponse

```python
import time

def test_prediction_performance(client):
    start = time.time()
    response = client.post("/predict/attrition", json={...})
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 1.0  # Moins d'1 seconde
```

## Bonnes Pratiques

1. **Noms descriptifs** : `test_should_return_error_when_invalid_input`
2. **Tests isolés** : Chaque test doit être indépendant
3. **AAA Pattern** : Arrange, Act, Assert
4. **Couverture** : Tester les cas d'erreur aussi
5. **Fixtures** : Réutiliser les données de test

## Tests à Implémenter

- [ ] Tests de tous les endpoints
- [ ] Tests de validation des données
- [ ] Tests d'erreurs
- [ ] Tests de performance
- [ ] Tests de sécurité
- [ ] Tests de charge

## Intégration Continue

Les tests sont exécutés automatiquement :
- À chaque commit
- Sur chaque pull request
- Avant chaque déploiement

Voir [CI_CD.md](./CI_CD.md) pour plus de détails.

