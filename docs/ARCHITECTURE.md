# Architecture du Projet

## Vue d'ensemble

Ce projet implémente une architecture moderne pour le déploiement d'un modèle de machine learning en production. L'architecture suit les principes SOLID et les bonnes pratiques de développement.

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
│   │   ├── health.py      # Health check
│   │   └── predict.py     # Prédictions
│   ├── core/              # Configuration et sécurité
│   │   ├── config.py      # Variables d'environnement
│   │   └── security.py    # JWT et authentification
│   ├── models/            # Modèles SQLAlchemy
│   │   ├── database.py    # Modèles ORM
│   │   └── schemas.py     # Schémas Pydantic
│   └── main.py            # Point d'entrée
├── ml/                     # Machine Learning
│   ├── model_loader.py    # Chargeur de modèle
│   └── preprocessor.py    # Préprocessing
├── tests/                  # Tests
│   ├── unit/              # Tests unitaires
│   │   ├── test_health.py
│   │   └── test_main.py
│   ├── integration/       # Tests d'intégration
│   │   ├── test_predict.py
│   │   └── test_database.py
│   └── conftest.py        # Configuration pytest
├── scripts/                # Scripts utilitaires
│   ├── create_db.py       # Création BDD
│   ├── create_db.sql      # Script SQL
│   └── seed_data.py       # Données d'exemple
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md    # Ce fichier
│   └── DATABASE_SCHEMA.md # Schéma BDD
├── .github/workflows/      # CI/CD
│   └── ci-cd.yml          # Pipeline GitHub Actions
├── models/                 # Modèles ML (.pkl)
├── requirements.txt        # Dépendances
└── README.md              # Documentation principale
```

## Composants Principaux

### 1. API FastAPI

**Responsabilités** :
- Exposer les endpoints REST
- Valider les données d'entrée (Pydantic)
- Gérer l'authentification (JWT)
- Documenter automatiquement (Swagger/OpenAPI)

**Endpoints** :
- `GET /health` - Vérification de l'état
- `POST /predict/attrition` - Prédiction unique
- `POST /predict/attrition/batch` - Prédictions multiples
- `GET /predict/history` - Historique des prédictions

### 2. Modèle Machine Learning

**Responsabilités** :
- Charger le modèle entraîné
- Préprocesser les données d'entrée
- Effectuer les prédictions
- Gérer les métadonnées du modèle

**Fichiers** :
- `ml/model_loader.py` - Chargement et utilisation du modèle
- `ml/preprocessor.py` - Transformation des données

### 3. Base de Données PostgreSQL

**Responsabilités** :
- Stocker les prédictions (inputs + outputs)
- Gérer l'authentification des utilisateurs
- Assurer la traçabilité complète

**Tables** :
- `predictions` - Historique des prédictions
- `users` - Utilisateurs authentifiés

### 4. Pipeline CI/CD

**Responsabilités** :
- Exécuter les tests automatiquement
- Valider la qualité du code
- Déployer sur différents environnements

**Environnements** :
- Development
- Staging
- Production

## Flux de Données

### Prédiction d'Attrition

```
1. Client → API (POST /predict/attrition)
   ↓
2. Validation des données (Pydantic)
   ↓
3. Préprocessing (AttritionPreprocessor)
   ↓
4. Prédiction (Model Loader)
   ↓
5. Sauvegarde en BDD (PostgreSQL)
   ↓
6. Retour de la réponse au client
```

## Sécurité

- **Authentification JWT** : Tokens pour sécuriser les endpoints
- **Hachage des mots de passe** : bcrypt pour les utilisateurs
- **Validation des données** : Pydantic pour éviter les injections
- **Variables d'environnement** : Secrets stockés sécuritairement
- **HTTPS en production** : Chiffrement des communications

## Performance

- **Index de base de données** : Optimisation des requêtes
- **Pool de connexions** : Réutilisation des connexions DB
- **Cache du modèle** : Modèle chargé une seule fois
- **Requêtes optimisées** : Limitation et pagination

## Déploiement

- **GitHub Actions** : CI/CD automatisé
- **Hugging Face Spaces** : Déploiement cloud
- **Environnements multiples** : dev, staging, prod
- **Gestion des secrets** : Variables d'environnement sécurisées

## Technologies

- **FastAPI** : Framework web moderne et rapide
- **PostgreSQL** : Base de données relationnelle
- **SQLAlchemy** : ORM Python
- **Pydantic** : Validation de données
- **Pytest** : Framework de tests
- **GitHub Actions** : CI/CD
- **scikit-learn** : Machine Learning

