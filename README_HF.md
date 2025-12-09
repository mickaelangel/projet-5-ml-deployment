---
title: API Prédiction Attrition
emoji: 🔮
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: latest
app_file: app_hf.py
pinned: false
---

# API Prédiction Attrition

API REST pour prédire le risque d'attrition des employés.

## Utilisation

Accédez à `/docs` pour la documentation interactive Swagger.

### Endpoints disponibles

- `GET /health` - Health check
- `POST /predict/attrition` - Prédiction d'attrition
- `POST /predict/attrition/batch` - Prédictions en batch
- `GET /predict/history` - Historique des prédictions
- `GET /docs` - Documentation Swagger

## Technologies

- FastAPI
- PostgreSQL
- scikit-learn
- Docker


