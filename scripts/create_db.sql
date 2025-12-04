-- Script SQL pour créer la base de données PostgreSQL
-- 
-- Usage:
--   1. Se connecter à PostgreSQL: psql -U postgres
--   2. Créer la base: CREATE DATABASE ml_db;
--   3. Se connecter à la base: \c ml_db
--   4. Exécuter ce script: \i scripts/create_db.sql

-- Table pour les prédictions
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER,
    input_data JSONB NOT NULL,
    prediction INTEGER NOT NULL,
    probability DOUBLE PRECISION NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    model_version VARCHAR(20) DEFAULT '1.0.0'
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_predictions_employee_id ON predictions(employee_id);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at);
CREATE INDEX IF NOT EXISTS idx_predictions_prediction ON predictions(prediction);

-- Table pour les utilisateurs (authentification)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les utilisateurs
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Commentaires pour la documentation
COMMENT ON TABLE predictions IS 'Stocke toutes les prédictions d''attrition';
COMMENT ON COLUMN predictions.input_data IS 'Données d''entrée au format JSON';
COMMENT ON COLUMN predictions.prediction IS '0 = Pas d''attrition, 1 = Attrition';
COMMENT ON COLUMN predictions.probability IS 'Probabilité d''attrition (0-1)';




