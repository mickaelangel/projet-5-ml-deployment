# Tests

## Vue d'ensemble

Le projet utilise Pytest pour les tests unitaires et d'intégration.

## Structure

```
tests/
├── unit/              # Tests unitaires
└── integration/       # Tests d'intégration
```

## Lancer les Tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=app --cov-report=html
```

## Couverture

Objectif : **60%+** (actuellement **78.02%** ✅)

## Documentation Complète

Pour plus de détails, voir [docs/TESTS.md](../docs/TESTS.md).
