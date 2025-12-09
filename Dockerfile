FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY . .

# Exposer le port (Hugging Face utilise le port 7860)
EXPOSE 7860

# Variables d'environnement
ENV API_HOST=0.0.0.0
ENV API_PORT=7860

# Lancer l'application
CMD ["python", "app_hf.py"]

