"""
Script de création de la base de données PostgreSQL
"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.database import create_tables, engine
from app.core.config import get_settings

def main():
    """Crée toutes les tables dans la base de données"""
    settings = get_settings()
    
    print("=" * 50)
    print("Création de la base de données PostgreSQL")
    print("=" * 50)
    print(f"\n📊 Base de données: {settings.DATABASE_URL.split('@')[-1]}")
    
    try:
        # Tester la connexion
        with engine.connect() as conn:
            print("✅ Connexion à la base de données réussie")
        
        # Créer les tables
        print("\n📋 Création des tables...")
        create_tables()
        
        print("\n" + "=" * 50)
        print("✅ Base de données initialisée avec succès !")
        print("=" * 50)
        print("\nTables créées:")
        print("  - predictions (pour stocker les prédictions)")
        print("  - users (pour l'authentification)")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la création de la base de données: {e}")
        print("\n💡 Vérifiez que:")
        print("  1. PostgreSQL est installé et démarré")
        print("  2. La base de données 'ml_db' existe")
        print("  3. Les identifiants dans DATABASE_URL sont corrects")
        sys.exit(1)


if __name__ == "__main__":
    main()





