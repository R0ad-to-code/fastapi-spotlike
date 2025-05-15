# Spotilike - Projet Cloud

Application de streaming musical similaire à Spotify, développée avec FastAPI et déployée sur AWS.

## Architecture

L'architecture du projet a été simplifiée tout en respectant les exigences du cours :

- **Backend** : API FastAPI déployée sur ECS
- **Frontend** : Application Angular déployée sur EKS
- **Base de données** : PostgreSQL hébergée sur RDS (tier gratuit)
- **Stockage** : S3 pour les médias (images, avatars)

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
# Initialiser Terraform
cd terraform
terraform init

# Créer un plan d'exécution
terraform plan

# Appliquer les modifications
terraform apply
```

## Structure du projet

- **app/** - Code source du backend FastAPI
- **frontend/** - Code source du frontend Angular
- **terraform/** - Scripts Terraform pour le déploiement AWS
- **alembic/** - Migrations de base de données

## Justification des choix techniques

### 1. PostgreSQL vs MongoDB

Nous avons migré de MongoDB vers PostgreSQL pour :
- Rester dans le tier gratuit d'AWS
- Utiliser une base relationnelle mieux adaptée au modèle de données

### 2. ECS pour le backend

- Simplifie le déploiement du backend FastAPI
- Reste dans le tier gratuit avec Fargate

### 3. EKS pour le frontend

- Répond à l'exigence du cours d'utiliser Kubernetes
- Utilise des instances t3.micro éligibles au tier gratuit

### 4. Terraform

- Infrastructure as Code pour faciliter la démonstration
- Configuration minimale pour réduire la complexité
- Commentaires explicatifs pour faciliter la compréhension

## Notes importantes

- **Coût** : Toutes les ressources sont configurées pour rester dans le tier gratuit d'AWS
- **Sécurité** : Configuration minimale pour un POC
- **Scalabilité** : Prêt pour être étendu avec plus de ressources si nécessaire

C'est un projet qui utilise docker, pour le lancer assurez vous d'avoir docker sur votre machine, 
placez vous à la racine du projet dans un terminal et utilisez :

    docker-compose build
    docker-compose up

Une fois le conteneur crée et lancé, il faut se rendre à l'url : 

    http://localhost:8000/docs pour tester les routes de l'API avec swagger

    http://localhost:4200/ pour l'interface utilisateur

