#!/bin/bash

# Désactiver toute configuration SSO préexistante
unset AWS_PROFILE
unset AWS_SSO_ACCOUNT_ID
unset AWS_SSO_ROLE_NAME

# Variables communes
AWS_REGION="eu-west-3"
IMAGE_TAG="latest"
AWS_ACCOUNT_ID="362789396136"


# Authentification à ECR
echo "Authentification à AWS ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Fonction pour créer un repo ECR si nécessaire
create_repo() {
  local repo_name=$1
  echo "Vérification du repository ECR pour ${repo_name}..."
  aws ecr describe-repositories --repository-names ${repo_name} --region ${AWS_REGION} || \
  aws ecr create-repository --repository-name ${repo_name} --region ${AWS_REGION}
}

# Construire les images avec docker-compose
echo "Construction des images avec docker-compose..."
docker buildx build --platform=linux/amd64 -t fastapi-spotlike-api:latest -f app/Dockerfile .
docker buildx build --platform=linux/amd64 -t fastapi-spotlike-frontend:latest ./frontend

# Pour l'API
API_ECR_REPO_NAME="spotlike-api"
create_repo ${API_ECR_REPO_NAME}
API_ECR_REPO_URL="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${API_ECR_REPO_NAME}"

# Taguer et pousser l'image API depuis l'image docker-compose
echo "Tagging et push de l'image API..."
docker tag fastapi-spotlike-api:latest ${API_ECR_REPO_URL}:${IMAGE_TAG}
docker push ${API_ECR_REPO_URL}:${IMAGE_TAG}

# Pour le frontend (si vous avez un service frontend dans docker-compose)
FRONTEND_ECR_REPO_NAME="spotlike-frontend"
create_repo ${FRONTEND_ECR_REPO_NAME}
FRONTEND_ECR_REPO_URL="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${FRONTEND_ECR_REPO_NAME}"

# Taguer et pousser l'image frontend depuis l'image docker-compose
echo "Tagging et push de l'image frontend..."
docker tag fastapi-spotlike-frontend:latest ${FRONTEND_ECR_REPO_URL}:${IMAGE_TAG}
docker push ${FRONTEND_ECR_REPO_URL}:${IMAGE_TAG}

echo ""
echo "=== Résumé des URLs ECR ==="
echo "API (Backend): ${API_ECR_REPO_URL}"
echo "Frontend: ${FRONTEND_ECR_REPO_URL}"