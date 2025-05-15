#!/bin/bash

# Attente que la base de données soit prête
echo "Attente de la disponibilité de la base de données..."
sleep 5

# Application des migrations
cd /app
alembic upgrade head

# Démarrage de l'application
echo "Démarrage de l'application..."
uvicorn main:app --host 0.0.0.0 --port 8000 