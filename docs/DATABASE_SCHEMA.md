# Schéma de la Base de Données

## Vue d'ensemble

La base de données PostgreSQL contient deux tables principales pour gérer les prédictions d'attrition et l'authentification.

---

## Diagramme UML

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
            │
            │
            │
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

---

## Description des Tables

### Table `predictions`

Stocke toutes les prédictions d'attrition réalisées par le modèle.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `id` | SERIAL | Identifiant unique | PRIMARY KEY, AUTO_INCREMENT |
| `employee_id` | INTEGER | ID de l'employé | NULLABLE, INDEX |
| `input_data` | JSONB | Données d'entrée au format JSON | NOT NULL |
| `prediction` | INTEGER | Résultat : 0=Pas d'attrition, 1=Attrition | NOT NULL |
| `probability` | FLOAT | Probabilité d'attrition (0-1) | NOT NULL |
| `class_name` | VARCHAR(50) | Nom de la classe prédite | NOT NULL |
| `created_at` | TIMESTAMP | Date et heure de la prédiction | NOT NULL, DEFAULT NOW() |
| `model_version` | VARCHAR(20) | Version du modèle utilisé | DEFAULT '1.0.0' |

**Index créés** :
- `idx_predictions_employee_id` sur `employee_id`
- `idx_predictions_created_at` sur `created_at`
- `idx_predictions_prediction` sur `prediction`

### Table `users`

Stocke les utilisateurs pour l'authentification.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `id` | SERIAL | Identifiant unique | PRIMARY KEY, AUTO_INCREMENT |
| `username` | VARCHAR(100) | Nom d'utilisateur | UNIQUE, NOT NULL, INDEX |
| `email` | VARCHAR(255) | Email de l'utilisateur | UNIQUE, NOT NULL, INDEX |
| `hashed_password` | VARCHAR(255) | Mot de passe hashé (bcrypt) | NOT NULL |
| `is_active` | BOOLEAN | Compte actif ou non | DEFAULT TRUE |
| `created_at` | TIMESTAMP | Date de création du compte | DEFAULT NOW() |

**Index créés** :
- `idx_users_username` sur `username`
- `idx_users_email` sur `email`

---

## Relations

- **predictions** ↔ **users** : Relation optionnelle via `employee_id`
  - Un utilisateur peut avoir plusieurs prédictions
  - Une prédiction peut être liée à un utilisateur (optionnel)

---

## Requêtes SQL Utiles

### Récupérer toutes les prédictions d'un employé

```sql
SELECT * 
FROM predictions 
WHERE employee_id = 123 
ORDER BY created_at DESC;
```

### Statistiques des prédictions

```sql
SELECT 
    COUNT(*) as total_predictions,
    SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as attrition_count,
    AVG(probability) as avg_probability
FROM predictions;
```

---

## Sécurité

- Les mots de passe sont hashés avec bcrypt
- Les données sensibles ne sont pas stockées en clair
- Les connexions utilisent des variables d'environnement pour les secrets











