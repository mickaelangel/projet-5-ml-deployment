# Déploiement d'un Modèle de Machine Learning

## 📋 Description du Projet

Ce projet consiste à déployer un modèle de machine learning en production en créant :
- Une API REST avec FastAPI
- Une base de données PostgreSQL pour la gestion des données
- Un pipeline CI/CD automatisé
- Des tests unitaires et fonctionnels complets

**Client** : Futurisys  
**Contexte** : Projet professionnel - Déploiement d'un modèle ML en production

## 🎯 Livrables

- ✅ Dépôt Git structuré avec historique clair
- ✅ API FastAPI fonctionnelle avec documentation Swagger
- ✅ Base de données PostgreSQL
- ✅ Tests unitaires et fonctionnels (Pytest)
- ✅ Pipeline CI/CD (GitHub Actions)
- ✅ Documentation complète

## 🚀 Installation

### Prérequis

- Python 3.9 ou supérieur
- PostgreSQL 12 ou supérieur
- Git
- Compte GitHub

### Installation des dépendances

```bash
# Cloner le dépôt
git clone <url-du-repo>
cd projet-ml-deployment

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration

1. Créer un fichier `.env` à la racine du projet :
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ml_db

# API
API_HOST=0.0.0.0
API_PORT=8000

# Security
SECRET_KEY=votre_clé_secrète_ici
ALGORITHM=HS256

# Environment
ENVIRONMENT=development
```

2. Initialiser la base de données :
```bash
# Démarrer PostgreSQL
# Créer la base de données
createdb ml_db

# Exécuter les migrations
python scripts/create_db.py
```

## 📖 Utilisation

### Démarrer l'API

```bash
# En développement
uvicorn app.main:app --reload

# En production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

L'API sera accessible à l'adresse : `http://localhost:8000`

### Documentation interactive

Une fois l'API démarrée, accédez à :
- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

### Exemple de requête

```bash
# Prédiction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "feature1": 1.5,
    "feature2": 2.3
  }'
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Lancer les tests avec couverture
pytest --cov=app --cov-report=html

# Lancer les tests d'un module spécifique
pytest tests/test_api.py
```

## 🗄️ Base de données

### Structure

```
ml_db
├── users          # Utilisateurs
├── models         # Modèles ML
├── predictions    # Prédictions
└── audit_logs     # Logs d'audit
```

### Schéma UML

[À compléter avec le diagramme UML]

## 🔐 Authentification

L'API utilise JWT pour l'authentification :

```bash
# Obtenir un token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'

# Utiliser le token
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

## 🔄 CI/CD

Le pipeline CI/CD est configuré avec GitHub Actions :

- **Tests automatiques** à chaque commit
- **Déploiement automatique** sur Hugging Face Spaces
- **Gestion des environnements** (dev, test, prod)

Fichier : `.github/workflows/ci-cd.yml`

## 📁 Structure du Projet

```
projet-ml-deployment/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── dependencies.py
│   ├── models/
│   │   ├── database.py
│   │   └── schemas.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── scripts/
│   ├── create_db.py
│   └── seed_data.py
├── docs/
├── .github/
│   └── workflows/
├── requirements.txt
├── README.md
└── .env.example
```

## 🛡️ Sécurité

- Authentification JWT
- Validation des données avec Pydantic
- Hachage des mots de passe avec bcrypt
- Gestion des secrets avec des variables d'environnement
- HTTPS en production

## 📊 Monitoring

- Logs structurés avec Loguru
- Métriques de performance
- Audit des interactions avec la base de données

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT.

## 👤 Auteur

**ANGEL MICKAEL**
- Email : mickaelangelcv@gmail.com
- GitHub : [@mickaelangel](https://github.com/mickaelangel)

## 🙏 Remerciements

- OpenClassrooms pour le parcours
- La communauté FastAPI
- Tous les contributeurs

