# Architecture du Projet

## Vue d'ensemble

Ce projet implémente une architecture moderne pour le déploiement d'un modèle de machine learning en production.

## Architecture Globale

```
┌─────────────────────────────────────────────────────────┐
│                     Client (HTTP)                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              API FastAPI (app/main.py)                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Routes (app/api/routes/)                        │   │
│  │  - /health                                       │   │
│  │  - /predict/attrition                            │   │
│  │  - /predict/history                              │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Core (app/core/)                                │   │
│  │  - Configuration                                 │   │
│  │  - Sécurité (JWT)                                │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────┬─────────────────────────┬──────────────────┘
              │                         │
              ▼                         ▼
┌─────────────────────────┐  ┌──────────────────────────┐
│  Modèle ML              │  │  PostgreSQL Database      │
│  (ml/model_loader.py)   │  │  (app/models/database.py)│
│  - Chargement modèle    │  │  - predictions           │
│  - Prédictions          │  │  - users                 │
│  - Préprocessing        │  │  - Traçabilité           │
└─────────────────────────┘  └──────────────────────────┘
```

## Structure du Projet

```
projet-5-ml-deployment/
├── app/                    # Application FastAPI
│   ├── api/routes/        # Endpoints API
│   ├── core/              # Configuration et sécurité
│   └── models/            # Modèles SQLAlchemy
├── ml/                     # Machine Learning
│   ├── model_loader.py    # Chargeur de modèle
│   └── preprocessor.py    # Préprocessing
├── tests/                  # Tests
│   ├── unit/              # Tests unitaires
│   └── integration/       # Tests d'intégration
├── scripts/                # Scripts utilitaires
├── docs/                   # Documentation
└── models/                 # Modèles ML (.pkl)
```

## Composants Principaux

### API FastAPI
- Endpoints REST pour les prédictions
- Documentation automatique (Swagger)
- Validation des données (Pydantic)

### Base de Données PostgreSQL
- Stockage des prédictions
- Traçabilité complète
- Authentification

### Pipeline CI/CD
- Tests automatiques
- Déploiement automatisé
- Gestion des environnements
