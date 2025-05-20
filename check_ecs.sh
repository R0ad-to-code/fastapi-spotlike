#!/bin/bash

# Utiliser des variables d'environnement plutôt que des clés codées en dur
# Assurez-vous de configurer ces variables dans votre environnement
# export AWS_ACCESS_KEY_ID="votre_clé"
# export AWS_SECRET_ACCESS_KEY="votre_secret"
# export AWS_DEFAULT_REGION="eu-west-3"

# Vérifier les tâches ECS
echo "Vérification des tâches ECS..."
aws ecs list-tasks --cluster spotlike-cluster 

# Vérifier l'état du service
echo "Vérification de l'état du service..."
aws ecs describe-services --cluster spotlike-cluster --services spotlike-service

# Redémarrer le service avec 2 tâches
echo "Redémarrage du service avec 2 tâches..."
aws ecs update-service --cluster spotlike-cluster --service spotlike-service --desired-count 2 --force-new-deployment 