# Étape 1 : Image de base légère
FROM python:3.12-slim

# Étape 2 : Variables d’environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Étape 3 : Création du répertoire de travail
WORKDIR /app

# Étape 4 : Copie des fichiers de dépendances
COPY requirements.txt .

# Étape 5 : Installation des dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Étape 6 : Copie du code source et des fichiers statiques
COPY . .

# Étape 7 : Exposition du port Flask
EXPOSE 5000

# Étape 8 : Commande de lancement (Gunicorn en production)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
