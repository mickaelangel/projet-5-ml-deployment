# 🌿 Structure des Branches Git

## 📋 Vue d'ensemble

Ce projet utilise une stratégie de branches Git basée sur **Git Flow**, adaptée pour le déploiement ML.

## 🌳 Branches Principales

### `main` (Production)
- **Rôle** : Branche principale pour la production
- **Utilisation** : Déploiements en production
- **Protection** : Ne doit recevoir que des merges depuis `develop` ou `hotfix/*`
- **Déploiement** : Déploiement automatique sur Hugging Face Spaces

### `develop` (Développement)
- **Rôle** : Branche d'intégration pour le développement
- **Utilisation** : Intégration des nouvelles fonctionnalités
- **Source** : Les branches `feature/*` sont mergées ici
- **Déploiement** : Déploiement automatique en environnement de développement

## 🌿 Branches de Fonctionnalités

### `feature/*`
- **Rôle** : Développement de nouvelles fonctionnalités
- **Création** : Depuis `develop`
- **Merge** : Retour vers `develop`
- **Exemples** :
  - `feature/add-authentication`
  - `feature/improve-api-docs`
  - `feature/add-monitoring`

**Workflow** :
```bash
# Créer une branche feature
git checkout develop
git pull origin develop
git checkout -b feature/nom-fonctionnalite

# Développer la fonctionnalité
# ... commits ...

# Merger dans develop
git checkout develop
git merge feature/nom-fonctionnalite
git push origin develop
```

## 🔧 Branches de Correction

### `hotfix/*`
- **Rôle** : Corrections urgentes pour la production
- **Création** : Depuis `main`
- **Merge** : Vers `main` ET `develop`
- **Exemples** :
  - `hotfix/fix-security-issue`
  - `hotfix/fix-api-bug`

**Workflow** :
```bash
# Créer une branche hotfix
git checkout main
git pull origin main
git checkout -b hotfix/nom-correction

# Corriger le problème
# ... commits ...

# Merger dans main
git checkout main
git merge hotfix/nom-correction
git push origin main

# Merger aussi dans develop
git checkout develop
git merge hotfix/nom-correction
git push origin develop
```

## 🏷️ Branches de Release

### `release/*`
- **Rôle** : Préparation d'une nouvelle version
- **Création** : Depuis `develop`
- **Merge** : Vers `main` (avec tag) ET `develop`
- **Exemples** :
  - `release/v1.0.0`
  - `release/v1.1.0`

**Workflow** :
```bash
# Créer une branche release
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Finaliser la release (tests, documentation)
# ... commits ...

# Merger dans main avec tag
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags

# Merger aussi dans develop
git checkout develop
git merge release/v1.0.0
git push origin develop
```

## 📊 Diagramme de Flux

```
main (production)
  ↑
  │ merge + tag
  │
release/v1.0.0
  ↑
  │ merge
  │
develop (développement)
  ↑
  │ merge
  │
feature/add-auth ──┐
feature/improve-docs ──┼──→ develop
feature/add-monitoring ──┘

main
  ↑
  │ merge
  │
hotfix/fix-bug
  │
  └──→ develop (merge aussi)
```

## 🎯 Bonnes Pratiques

### 1. Naming Convention

- **Features** : `feature/nom-descriptif`
- **Hotfixes** : `hotfix/nom-descriptif`
- **Releases** : `release/vX.Y.Z`

### 2. Commit Messages

Utilisez des messages clairs et descriptifs :
```
feat: Add user authentication
fix: Resolve API timeout issue
docs: Update README with deployment instructions
test: Add integration tests for prediction endpoint
refactor: Improve model loader error handling
```

### 3. Pull Requests

- Toujours créer une Pull Request pour merger dans `develop` ou `main`
- Utiliser des descriptions claires
- Faire revoir le code par un collègue (si possible)
- S'assurer que les tests passent

### 4. Branches à Supprimer

Après avoir mergé une branche :
```bash
# Supprimer la branche locale
git branch -d feature/nom-fonctionnalite

# Supprimer la branche distante
git push origin --delete feature/nom-fonctionnalite
```

## 🔄 Workflow Complet

### Développement d'une nouvelle fonctionnalité

1. **Créer la branche** :
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/nouvelle-fonctionnalite
   ```

2. **Développer** :
   ```bash
   # Faire des commits réguliers
   git add .
   git commit -m "feat: Description de la fonctionnalité"
   ```

3. **Pousser et créer une PR** :
   ```bash
   git push origin feature/nouvelle-fonctionnalite
   # Créer une Pull Request sur GitHub vers develop
   ```

4. **Après approbation, merger** :
   ```bash
   git checkout develop
   git merge feature/nouvelle-fonctionnalite
   git push origin develop
   ```

5. **Nettoyer** :
   ```bash
   git branch -d feature/nouvelle-fonctionnalite
   ```

### Déploiement en Production

1. **Créer une release** :
   ```bash
   git checkout develop
   git checkout -b release/v1.0.0
   # Finaliser les tests, documentation
   ```

2. **Merger dans main** :
   ```bash
   git checkout main
   git merge release/v1.0.0
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin main --tags
   ```

3. **Le déploiement se déclenche automatiquement** (via GitHub Actions)

## 📝 Commandes Utiles

```bash
# Voir toutes les branches
git branch -a

# Voir les branches distantes
git branch -r

# Voir les branches mergées
git branch --merged

# Voir les branches non mergées
git branch --no-merged

# Supprimer une branche locale
git branch -d nom-branche

# Supprimer une branche distante
git push origin --delete nom-branche

# Renommer une branche
git branch -m ancien-nom nouveau-nom
```

## 🎓 Pour la Soutenance

### Points à Mentionner

1. **Structure Git Flow** : Expliquer la stratégie de branches
2. **Séparation des environnements** : 
   - `develop` → Développement
   - `main` → Production
3. **Traçabilité** : Tags pour les releases
4. **CI/CD** : Déploiement automatique selon la branche
5. **Pull Requests** : Processus de revue de code

### Démonstration

```bash
# Montrer la structure
git branch -a

# Montrer les commits
git log --oneline --graph --all --decorate

# Montrer les tags
git tag
```

---

**Note** : Cette structure est adaptée pour un projet ML avec déploiement automatique. Elle peut être simplifiée pour des projets plus petits.


