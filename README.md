# Déploiement d'un Modèle de Machine Learning

## 📋 Description du Projet

Ce projet consiste à déployer un modèle de machine learning en production en créant :
- Une API REST avec FastAPI
- Une base de données PostgreSQL pour la gestion des données
- Un pipeline CI/CD automatisé
- Des tests unitaires et fonctionnels complets

**Client** : Futurisys  
**Contexte** : Projet professionnel - Déploiement d'un modèle ML en production  
**Auteur** : ANGEL MICKAEL

## 🎯 Livrables

- ✅ Dépôt Git structuré avec historique clair, branches et tags
- ✅ API FastAPI fonctionnelle avec documentation Swagger/OpenAPI
- ✅ Base de données PostgreSQL avec scripts de création
- ✅ Tests unitaires et fonctionnels (Pytest) - **95.05% de couverture**
- ✅ Pipeline CI/CD (GitHub Actions) avec gestion des environnements
- ✅ Documentation complète (README, Wiki, Docs)

## 🚀 Installation

### Prérequis

- Python 3.9 ou supérieur (recommandé : 3.11)
- PostgreSQL 12 ou supérieur
- Git
- Compte GitHub

### Installation des dépendances

```bash
# Cloner le dépôt
git clone https://github.com/mickaelangel/projet-5-ml-deployment.git
cd projet-5-ml-deployment

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Configuration

1. Créer un fichier `.env` à la racine du projet :

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ml_db

# API
API_HOST=0.0.0.0
API_PORT=8000

# Security
SECRET_KEY=votre_clé_secrète_ici_changez_en_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=True
```

2. Initialiser la base de données :

```bash
# Créer la base de données PostgreSQL
createdb ml_db

# Ou via psql
psql -U postgres
CREATE DATABASE ml_db;

# Exécuter les scripts de création
python scripts/create_db.py

# Ou via SQL directement
psql -U postgres -d ml_db -f scripts/create_db.sql

# (Optionnel) Insérer des données d'exemple
python scripts/seed_data.py
```

## 📖 Utilisation

### Démarrer l'API

```bash
# En développement (avec rechargement automatique)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# En production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

L'API sera accessible à l'adresse : `http://localhost:8000`

### Documentation interactive

Une fois l'API démarrée, accédez à :
- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`
- **Schéma OpenAPI** : `http://localhost:8000/openapi.json`

### Exemples de requêtes

#### Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

#### Prédiction d'attrition

```bash
curl -X POST "http://localhost:8000/predict/attrition" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
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
  }'
```

#### Prédiction en batch

```bash
curl -X POST "http://localhost:8000/predict/attrition/batch" \
  -H "Content-Type: application/json" \
  -d '[{...}, {...}]'
```

#### Historique des prédictions

```bash
# Toutes les prédictions
curl -X GET "http://localhost:8000/predict/history"

# Filtrer par employee_id
curl -X GET "http://localhost:8000/predict/history?employee_id=1&limit=10"
```

## 🧪 Tests

### Lancer les tests

```bash
# Tous les tests
pytest

# Avec affichage détaillé
pytest -v

# Tests avec couverture
pytest --cov=app --cov=ml --cov-report=html --cov-report=term-missing

# Tests d'un module spécifique
pytest tests/unit/
pytest tests/integration/

# Tests avec rapport XML (pour CI/CD)
pytest --cov=app --cov=ml --cov-report=xml
```

### Résultats des tests

- **57 tests** au total
- **52 tests passent** ✅
- **Couverture globale : 95.05%**
- Rapports disponibles dans `htmlcov/` et `coverage.xml`

## 🗄️ Base de Données

### Structure

La base de données PostgreSQL contient :

- **Table `predictions`** : Stocke toutes les prédictions d'attrition
  - `id` : Identifiant unique
  - `employee_id` : ID de l'employé (optionnel)
  - `input_data` : Données d'entrée (JSON)
  - `prediction` : Résultat (0 ou 1)
  - `probability` : Probabilité d'attrition (0-1)
  - `class_name` : Nom de la classe
  - `created_at` : Date de création
  - `model_version` : Version du modèle utilisé

- **Table `users`** : Utilisateurs pour l'authentification
  - `id` : Identifiant unique
  - `username` : Nom d'utilisateur (unique)
  - `email` : Email (unique)
  - `hashed_password` : Mot de passe hashé
  - `is_active` : Statut actif/inactif
  - `created_at` : Date de création

### Schéma UML

Voir la documentation complète dans :
- `docs/DATABASE_SCHEMA.md` - Documentation détaillée
- `wiki/Base-de-Données.md` - Schéma UML et explications

### Scripts disponibles

- `scripts/create_db.py` - Création des tables (Python/SQLAlchemy)
- `scripts/create_db.sql` - Création des tables (SQL pur)
- `scripts/seed_data.py` - Insertion de données d'exemple

## 🔐 Authentification et Sécurisation

### Méthodes d'authentification

L'API utilise **JWT (JSON Web Tokens)** pour l'authentification :

```bash
# Obtenir un token (endpoint à implémenter)
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'

# Utiliser le token
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

### Bonnes pratiques de sécurité

- ✅ **Hachage des mots de passe** : bcrypt avec salt
- ✅ **Validation des données** : Pydantic pour éviter les injections
- ✅ **Gestion des secrets** : Variables d'environnement (ne jamais commiter `.env`)
- ✅ **HTTPS en production** : Chiffrement des communications
- ✅ **Tokens JWT** : Expiration automatique configurable
- ✅ **Validation des entrées** : Validation stricte des types et formats

### Configuration des secrets

⚠️ **IMPORTANT** : Ne jamais commiter le fichier `.env` contenant les secrets réels !

Utilisez `.env.example` comme modèle et configurez vos propres secrets en local.

En production, utilisez :
- Variables d'environnement du serveur
- Secrets managers (AWS Secrets Manager, HashiCorp Vault, etc.)
- GitHub Secrets pour CI/CD

## 🔄 CI/CD

### Pipeline GitHub Actions

Le pipeline CI/CD est configuré dans `.github/workflows/ci-cd.yml`

#### Étapes du pipeline

1. **Tests et validation**
   - Exécution des tests unitaires et d'intégration
   - Vérification avec PostgreSQL
   - Génération des rapports de couverture
   - Upload vers Codecov (optionnel)

2. **Build**
   - Construction de l'application
   - Vérification de la structure

3. **Déploiement selon l'environnement**
   - **Development** : Sur push vers `develop`
   - **Staging** : Sur Pull Request vers `main`
   - **Production** : Sur création de release/tag
   - **Hugging Face** : Sur push vers `main`

#### Gestion des environnements

Le pipeline gère automatiquement différents environnements :

- **Development** : Tests et déploiement préliminaire
- **Staging** : Environnement de test avant production
- **Production** : Environnement de production
- **Hugging Face Spaces** : Déploiement cloud

#### Secrets requis

Configurez ces secrets dans GitHub (Settings > Secrets) :

- `DEV_DATABASE_URL`, `DEV_HOST`, `DEV_USER`, `DEV_URL`
- `STAGING_DATABASE_URL`, `STAGING_HOST`, `STAGING_USER`, `STAGING_URL`
- `PROD_DATABASE_URL`, `PROD_HOST`, `PROD_USER`, `PROD_URL`
- `HUGGINGFACE_TOKEN`, `HF_SPACE`
- `CODECOV_TOKEN` (optionnel)

Voir `docs/CI_CD.md` pour plus de détails.

## 📁 Structure du Projet

```
projet-5-ml-deployment/
├── app/                          # Application FastAPI
│   ├── api/
│   │   └── routes/              # Routes API (health, predict)
│   ├── core/                    # Configuration et sécurité
│   │   ├── config.py           # Configuration via variables d'env
│   │   └── security.py         # Authentification JWT
│   ├── models/                  # Modèles de données
│   │   ├── database.py         # Modèles SQLAlchemy
│   │   └── schemas.py          # Schémas Pydantic
│   └── main.py                 # Point d'entrée FastAPI
├── ml/                          # Machine Learning
│   ├── model_loader.py         # Chargeur de modèle ML
│   └── preprocessor.py         # Préprocesseur des données
├── tests/                       # Tests
│   ├── unit/                   # Tests unitaires
│   │   ├── test_main.py
│   │   ├── test_health.py
│   │   ├── test_security.py
│   │   ├── test_preprocessor.py
│   │   ├── test_model_loader.py
│   │   └── test_database.py
│   ├── integration/            # Tests d'intégration
│   │   ├── test_predict.py
│   │   ├── test_database.py
│   │   └── test_health.py
│   └── conftest.py             # Configuration pytest
├── scripts/                     # Scripts utilitaires
│   ├── create_db.py            # Création BDD (Python)
│   ├── create_db.sql           # Création BDD (SQL)
│   └── seed_data.py            # Données d'exemple
├── docs/                        # Documentation technique
│   ├── ARCHITECTURE.md
│   ├── BASE_DE_DONNEES.md
│   ├── CI_CD.md
│   ├── DATABASE_SCHEMA.md
│   ├── TESTS.md
│   └── UTILISATION_API.md
├── wiki/                        # Wiki du projet
│   ├── Home.md
│   ├── Architecture.md
│   ├── Base-de-Données.md
│   ├── CI-CD.md
│   ├── Installation.md
│   ├── Tests.md
│   └── Utilisation-API.md
├── models/                      # Modèles ML (fichiers .pkl)
│   ├── attrition_model_pipeline.pkl
│   ├── preprocessor.pkl
│   └── ...
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Pipeline CI/CD
├── requirements.txt            # Dépendances Python
├── pytest.ini                  # Configuration Pytest
├── README.md                   # Ce fichier
└── .env.example                # Exemple de configuration
```

## 🛡️ Sécurité

### Mesures implémentées

- ✅ **Authentification JWT** : Tokens sécurisés avec expiration
- ✅ **Validation des données** : Pydantic pour éviter les injections
- ✅ **Hachage des mots de passe** : bcrypt avec salt
- ✅ **Gestion des secrets** : Variables d'environnement (jamais en code)
- ✅ **HTTPS en production** : Chiffrement des communications
- ✅ **CORS configuré** : Contrôle des origines autorisées

### Recommandations de sécurité

1. Changez `SECRET_KEY` en production
2. Utilisez des mots de passe forts pour PostgreSQL
3. Limitez les accès réseau à la base de données
4. Activez le logging des actions sensibles
5. Configurez un rate limiting pour l'API
6. Mettez à jour régulièrement les dépendances

## 📊 Monitoring et Performance

- **Logs structurés** : Configuration disponible pour Loguru
- **Health checks** : Endpoint `/health` pour monitoring
- **Métriques** : Traçabilité complète des prédictions
- **Audit** : Toutes les interactions enregistrées en base

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Versions et Tags

Le projet utilise des tags Git pour la gestion des versions :

- `v1.0.0` - Version initiale
- `v1.0.1` - Version avec tests complets (95% couverture)

```bash
# Voir tous les tags
git tag -l

# Checkout une version spécifique
git checkout v1.0.0
```

## 📄 License

Ce projet est sous licence MIT.

## 👤 Auteur

**ANGEL MICKAEL**
- Email : mickaelangelcv@gmail.com
- GitHub : [@mickaelangel](https://github.com/mickaelangel)

## 📚 Documentation Complète

Pour plus de détails, consultez :
- **Wiki** : `wiki/` - Documentation complète du projet
- **Docs** : `docs/` - Documentation technique détaillée
- **LIVRABLES.md** : Liste complète des livrables

## 🙏 Remerciements

- OpenClassrooms pour le parcours
- La communauté FastAPI
- La communauté Python/ML
- Tous les contributeurs

---

**Projet réalisé dans le cadre du parcours Data Scientist - OpenClassrooms**
