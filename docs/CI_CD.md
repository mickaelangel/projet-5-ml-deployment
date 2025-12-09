# Documentation CI/CD

## Vue d'ensemble

Le pipeline CI/CD est configuré avec GitHub Actions pour automatiser les tests et le déploiement.

## Fichier de Configuration

Le pipeline est défini dans : `.github/workflows/ci-cd.yml`

## Étapes du Pipeline

### 1. Tests et Validation

**Déclenchement** : À chaque push ou pull request

**Actions** :
- Installation des dépendances Python
- Lint du code (flake8)
- Exécution des tests unitaires et d'intégration
- Génération du rapport de couverture
- Validation de la couverture minimale (60%)

**Base de données de test** : PostgreSQL 13 (via service Docker)

### 2. Build de l'Application

**Déclenchement** : Après les tests réussis

**Actions** :
- Build de l'application
- Vérification de la compilation

### 3. Déploiement par Environnement

#### Development
- **Déclenchement** : Push sur `develop`
- **Environnement** : Development
- **Actions** : Déploiement automatique

#### Staging
- **Déclenchement** : Pull Request vers `main`
- **Environnement** : Staging
- **Actions** : Déploiement pour tests

#### Production
- **Déclenchement** : Création d'un release
- **Environnement** : Production
- **Actions** : Déploiement en production

### 4. Déploiement Hugging Face Spaces

**Déclenchement** : Push sur `main` ou création d'un tag de version

**Actions** :
- Déploiement automatique sur Hugging Face Spaces
- Configuration via GitHub Secrets

## Secrets GitHub

Configurer les secrets suivants dans GitHub Settings → Secrets :

- `HUGGINGFACE_TOKEN` : Token d'accès Hugging Face
- `DATABASE_URL` : URL de la base de données (production)
- `SECRET_KEY` : Clé secrète pour l'API

## Gestion des Environnements

### Variables par Environnement

**Development** :
```yaml
DATABASE_URL: postgresql://postgres:postgres@localhost:5432/ml_db_dev
ENVIRONMENT: development
DEBUG: true
```

**Staging** :
```yaml
DATABASE_URL: postgresql://postgres:postgres@staging-db:5432/ml_db_staging
ENVIRONMENT: staging
DEBUG: false
```

**Production** :
```yaml
DATABASE_URL: postgresql://user:pass@prod-db:5432/ml_db_prod
ENVIRONMENT: production
DEBUG: false
```

## Déclencheurs du Pipeline

### Sur Push
- Branches : `main`, `develop`, `feature/*`
- Actions : Tests + Build

### Sur Pull Request
- Vers : `main`, `develop`
- Actions : Tests + Staging Deployment

### Sur Release
- Type : `created`
- Actions : Production Deployment

### Sur Tag
- Format : `v*.*.*`
- Actions : Hugging Face Deployment

## Workflow Exemple

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=app
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: echo "Deploying..."
```

## Monitoring

### Badges de Statut

Ajouter dans le README.md :

```markdown
![CI/CD](https://github.com/username/repo/workflows/CI/CD%20Pipeline/badge.svg)
![Coverage](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)
```

### Notifications

Le pipeline peut envoyer des notifications :
- Email en cas d'échec
- Slack/Discord pour les déploiements
- GitHub Issues pour les erreurs critiques

## Troubleshooting

### Les tests échouent

1. Vérifier les logs GitHub Actions
2. Tester localement : `pytest`
3. Vérifier les dépendances dans `requirements.txt`

### Le déploiement échoue

1. Vérifier les secrets GitHub
2. Vérifier la configuration de l'environnement
3. Vérifier les permissions Hugging Face

### Performance

- Temps d'exécution cible : < 10 minutes
- Cache des dépendances activé
- Parallélisation des jobs si possible

## Bonnes Pratiques

1. **Commits atomiques** : Un commit = une fonctionnalité
2. **Messages clairs** : Descriptions explicites
3. **Branches** : Utiliser des branches feature
4. **Tests** : Toujours écrire des tests
5. **Review** : Faire des pull requests

## Améliorations Futures

- [ ] Déploiement automatique sur plusieurs plateformes
- [ ] Tests de performance automatisés
- [ ] Rollback automatique en cas d'erreur
- [ ] Monitoring et alertes
- [ ] Documentation automatique












