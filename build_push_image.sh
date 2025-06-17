# Récupérer l'URL du repository ECR depuis les outputs Terraform
API_REPO_URL=$(cd terraform && terraform output -raw api_repository_url)
FRONTEND_REPO_URL=$(cd terraform && terraform output -raw frontend_repository_url)

# Connexion à ECR
aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${API_REPO_URL%/*}

# Construire et pousser l'image backend
cd app
docker build -t ${API_REPO_URL}:latest .
docker push ${API_REPO_URL}:latest

# Construire et pousser l'image frontend
cd ../frontend
docker build -t ${FRONTEND_REPO_URL}:latest .
docker push ${FRONTEND_REPO_URL}:latest

# Forcer le redéploiement du service ECS
CLUSTER_NAME=$(cd ../terraform && terraform output -raw cluster_name)
SERVICE_NAME=$(cd ../terraform && terraform output -raw service_name)
aws ecs update-service --cluster ${CLUSTER_NAME} --service ${SERVICE_NAME} --force-new-deployment