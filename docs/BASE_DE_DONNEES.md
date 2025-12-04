# Documentation Base de Données

## Vue d'ensemble

La base de données PostgreSQL stocke toutes les prédictions et permet une traçabilité complète des interactions avec le modèle ML.

## Configuration

### Variables d'environnement

Dans le fichier `.env` :
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ml_db
```

### Création de la base de données

1. **Créer la base de données** :
```bash
createdb ml_db
```

Ou via psql :
```sql
CREATE DATABASE ml_db;
```

2. **Créer les tables** :
```bash
python scripts/create_db.py
```

Ou via SQL :
```bash
psql -U postgres -d ml_db -f scripts/create_db.sql
```

## Structure des Tables

Voir le fichier [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) pour le schéma détaillé.

## Utilisation avec SQLAlchemy

### Connexion

```python
from app.models.database import SessionLocal, Prediction

# Créer une session
db = SessionLocal()

# Utiliser la session
try:
    # Votre code ici
    pass
finally:
    db.close()
```

### Exemples de requêtes

#### Créer une prédiction

```python
from app.models.database import SessionLocal, Prediction

db = SessionLocal()

prediction = Prediction(
    employee_id=123,
    input_data={"age": 32, "revenu_mensuel": 75000},
    prediction=1,
    probability=0.75,
    class_name="Attrition"
)

db.add(prediction)
db.commit()
db.refresh(prediction)
```

#### Récupérer des prédictions

```python
from app.models.database import SessionLocal, Prediction

db = SessionLocal()

# Toutes les prédictions
predictions = db.query(Prediction).all()

# Par employé
employee_predictions = db.query(Prediction).filter(
    Prediction.employee_id == 123
).all()

# Dernières prédictions
recent = db.query(Prediction).order_by(
    Prediction.created_at.desc()
).limit(10).all()
```

## Requêtes SQL Utiles

### Statistiques globales

```sql
SELECT 
    COUNT(*) as total_predictions,
    SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as attrition_count,
    AVG(probability) as avg_probability,
    MAX(probability) as max_probability,
    MIN(probability) as min_probability
FROM predictions;
```

### Prédictions par employé

```sql
SELECT 
    employee_id,
    COUNT(*) as nb_predictions,
    AVG(probability) as avg_probability,
    MAX(created_at) as derniere_prediction
FROM predictions
WHERE employee_id IS NOT NULL
GROUP BY employee_id
ORDER BY nb_predictions DESC;
```

### Prédictions récentes

```sql
SELECT *
FROM predictions
WHERE created_at >= NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;
```

### Top 10 prédictions avec risque élevé

```sql
SELECT 
    id,
    employee_id,
    probability,
    class_name,
    created_at
FROM predictions
WHERE prediction = 1
ORDER BY probability DESC
LIMIT 10;
```

## Traçabilité

Toutes les interactions avec le modèle sont enregistrées :

- **Inputs** : Données d'entrée stockées en JSONB
- **Outputs** : Prédiction et probabilité
- **Métadonnées** : Date, version du modèle, ID employé

Cela permet de :
- Auditer les prédictions
- Analyser les performances
- Déboguer les problèmes
- Réentraîner le modèle si nécessaire

## Migration et Maintenance

### Sauvegarder la base de données

```bash
pg_dump -U postgres ml_db > backup.sql
```

### Restaurer la base de données

```bash
psql -U postgres ml_db < backup.sql
```

### Nettoyer les anciennes prédictions

```sql
-- Supprimer les prédictions de plus de 1 an
DELETE FROM predictions
WHERE created_at < NOW() - INTERVAL '1 year';
```

### Analyser les performances

```sql
-- Vérifier les index
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public';
```

## Sécurité

- Les mots de passe sont hashés avec bcrypt
- Les connexions utilisent SSL en production
- Les secrets sont stockés dans les variables d'environnement
- Accès limité aux utilisateurs autorisés

## Performance

### Index créés

- `idx_predictions_employee_id` : Recherche par employé
- `idx_predictions_created_at` : Tri par date
- `idx_predictions_prediction` : Filtrage par résultat

### Optimisations recommandées

- Partitionner par date pour de gros volumes
- Archiver les anciennes données
- Utiliser des vues matérialisées pour les statistiques

## Scripts Utilitaires

### seed_data.py

Insère des données d'exemple dans la base :

```bash
python scripts/seed_data.py
```

### create_db.py

Crée toutes les tables :

```bash
python scripts/create_db.py
```




