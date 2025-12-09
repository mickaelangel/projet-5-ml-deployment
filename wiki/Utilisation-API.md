# Utilisation de l'API

## Base URL

- **Local** : `http://localhost:8000`
- **Documentation** : `http://localhost:8000/docs`

## Endpoints Principaux

### Health Check
```
GET /health
```

### Prédiction d'Attrition
```
POST /predict/attrition
```

### Historique
```
GET /predict/history
```

## Exemple d'Utilisation

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/predict/attrition",
    json={
        "employee_id": 123,
        "age": 32,
        "revenu_mensuel": 75000,
        ...
    }
)
print(response.json())
```

### curl

```bash
curl -X POST "http://localhost:8000/predict/attrition" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": 123, "age": 32, ...}'
```

## Documentation Complète

Pour plus de détails, voir [docs/UTILISATION_API.md](../docs/UTILISATION_API.md).
