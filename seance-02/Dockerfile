# Utiliser une image Python légère comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances
RUN pip install --no-cache-dir pandas boto3

# Copier le script d'analyse (que nous créerons juste après)
COPY analyse_referentiel.py .

# Commande par défaut au démarrage du conteneur
CMD ["python", "analyse_referentiel.py"]

