# CI/CD Pipeline

## Vue d'ensemble

Le pipeline CI/CD est configuré avec GitHub Actions pour automatiser les tests et le déploiement.

## Fichier de Configuration

`.github/workflows/ci-cd.yml`

## Étapes du Pipeline

1. **Tests** : Validation du code et exécution des tests
2. **Build** : Construction de l'application
3. **Déploiement** : Déploiement selon l'environnement (dev, staging, prod)

## Environnements

- **Development** : Push sur `develop`
- **Staging** : Pull Request vers `main`
- **Production** : Création d'un release

## Déploiement Hugging Face

Automatique sur push vers `main` ou création d'un tag.

## Documentation Complète

Pour plus de détails, voir [docs/CI_CD.md](../docs/CI_CD.md).
