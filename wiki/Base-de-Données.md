# Base de Données

## Vue d'ensemble

La base de données PostgreSQL stocke toutes les prédictions et permet une traçabilité complète.

## Structure

Deux tables principales :

- **predictions** : Historique des prédictions
- **users** : Utilisateurs authentifiés

## Schéma UML

```
┌─────────────────────────────────────┐
│         predictions                 │
├─────────────────────────────────────┤
│ PK  id                    SERIAL    │
│     employee_id           INTEGER   │
│     input_data            JSONB     │
│     prediction            INTEGER   │
│     probability           FLOAT     │
│     class_name            VARCHAR   │
│     created_at            TIMESTAMP │
│     model_version         VARCHAR   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           users                     │
├─────────────────────────────────────┤
│ PK  id                    SERIAL    │
│ UK  username              VARCHAR   │
│ UK  email                 VARCHAR   │
│     hashed_password       VARCHAR   │
│     is_active             BOOLEAN   │
│     created_at            TIMESTAMP │
└─────────────────────────────────────┘
```

## Configuration

### Créer la base de données

```bash
createdb ml_db
python scripts/create_db.py
```

### Variables d'environnement

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ml_db
```

## Traçabilité

Toutes les interactions avec le modèle sont enregistrées :
- Inputs (données d'entrée)
- Outputs (prédiction et probabilité)
- Métadonnées (date, version du modèle)

Pour plus de détails, voir [docs/DATABASE_SCHEMA.md](../docs/DATABASE_SCHEMA.md).
