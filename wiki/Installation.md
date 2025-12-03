# Installation

## Prérequis

- Python 3.9 ou supérieur
- PostgreSQL 12 ou supérieur
- Git

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/mickaelangel/projet-5-ml-deployment.git
cd projet-5-ml-deployment
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer PostgreSQL

```bash
# Créer la base de données
createdb ml_db

# Créer les tables
python scripts/create_db.py
```

### 5. Créer le fichier .env

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ml_db
API_HOST=0.0.0.0
API_PORT=8000
```

### 6. Lancer l'API

```bash
uvicorn app.main:app --reload
```

L'API sera accessible sur `http://localhost:8000`

## Documentation Complète

Pour plus de détails, voir le [README.md](../README.md).
