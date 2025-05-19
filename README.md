# Spotilike - Projet Cloud

Application de streaming musical similaire à Spotify, développée avec FastAPI et déployée sur AWS.

## Architecture

L'architecture du projet a été simplifiée tout en respectant les exigences du cours :

- **Backend** : API FastAPI déployée sur ECS Fargate
- **Frontend** : Application Angular déployée sur ECS Fargate
- **Base de données** : PostgreSQL hébergée sur RDS
- **Stockage** : S3 pour les médias (images, avatars)
- **Load Balancer** : Application Load Balancer pour router le trafic

## Comment déployer

### 1. Configuration locale

```bash
# Cloner le dépôt
git clone https://github.com/votre-repo/fastapi-spotlike.git
cd fastapi-spotlike

# Lancer l'application en local
docker-compose up -d
```

### 2. Déploiement sur AWS (Terraform)

```bash
# Configuration des credentials AWS
export AWS_ACCESS_KEY_ID="votre_access_key"
export AWS_SECRET_ACCESS_KEY="votre_secret_key"
export AWS_DEFAULT_REGION="eu-west-3"

# Initialiser Terraform
cd terraform
terraform init

# Créer un plan d'exécution
terraform plan

# Appliquer les modifications
terraform apply
```

### 3. Construction et déploiement des images Docker

```bash
# Utiliser le script de build et push
chmod +x build_push_image.sh
./build_push_image.sh
```

## Structure du projet

- **app/** - Code source du backend FastAPI
- **frontend/** - Code source du frontend Angular
- **terraform/** - Scripts Terraform pour le déploiement AWS
- **alembic/** - Migrations de base de données

## Accès à l'application

Une fois déployée, l'application est accessible via l'URL du Load Balancer :

- **Frontend** : http://[ALB_DNS_NAME]/
- **API Swagger** : http://[ALB_DNS_NAME]/docs
- **API Health Check** : http://[ALB_DNS_NAME]/api/health

## Arrêt des services

Pour arrêter les services et éviter des coûts supplémentaires :

```bash
# Supprimer toutes les ressources
cd terraform
terraform destroy -auto-approve
```

## Notes importantes

- **Coût** : Les ressources AWS génèrent des coûts. Pensez à les arrêter quand vous ne les utilisez pas.
- **Sécurité** : Les credentials AWS sont sensibles, ne les partagez pas.
- **Configuration** : Le frontend est configuré pour communiquer avec l'API via le Load Balancer.

## Développement local

Pour le développement local, assurez-vous d'avoir Docker installé :

```bash
# Construction des images
docker-compose build

# Lancement des services
docker-compose up

# Accès aux services
- API Swagger : http://localhost:8000/docs
- Frontend : http://localhost:4200/
```

