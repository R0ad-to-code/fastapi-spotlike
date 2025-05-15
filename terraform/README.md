# Déploiement Terraform pour Spotilike

Ce dossier contient les scripts Terraform pour déployer l'application Spotilike sur AWS.

## Configuration IAM

Avant de déployer avec Terraform, créez un utilisateur IAM avec les accès appropriés:

1. Connectez-vous à la console AWS
2. Dans le service IAM, créez un utilisateur avec accès programmatique
3. Attribuez les politiques:
   - AmazonECS-FullAccess  
   - AmazonRDS-FullAccess
   - AmazonS3-FullAccess
   - AmazonVPC-FullAccess
4. Téléchargez les clés d'accès
5. Dans votre terminal:
   ```bash
   aws configure
   ```
6. Entrez vos clés, région (ex: eu-west-3) et format (json)

## Fichiers de configuration

- `main.tf` - Ressources complètes (VPC, RDS, S3, ECS Fargate)
- `providers.tf` - Configuration des providers AWS
- `variables.tf` - Variables utilisées par l'infrastructure

## Utilisation

```bash
# Initialiser Terraform
terraform init

# Voir ce qui va être créé
terraform plan

# Déployer l'infrastructure
terraform apply

# Supprimer toutes les ressources
terraform destroy
```

## Infrastructure créée

Lors du déploiement, Terraform va:
- Créer un VPC avec sous-réseaux dans plusieurs zones
- Provisionner une base de données PostgreSQL sur RDS
- Créer un bucket S3 pour les médias
- Déployer des services ECS Fargate pour le frontend et le backend
- Mettre en place IAM roles et security groups nécessaires
- Configurer les accès réseau entre les services

Le déploiement prend environ 5-10 minutes. Une fois terminé, les endpoints seront affichés dans la sortie du terminal.

## Architecture simplifiée

Pour faciliter la compréhension et le déploiement:
- Utilisation de sous-réseaux publics uniquement
- Configuration minimale des services AWS
- Tout est dans le tier gratuit AWS
- ECS Fargate pour éviter la gestion d'infrastructure

## Questions fréquentes pour l'oral

1. **Pourquoi garder des sous-réseaux?**
   AWS exige des sous-réseaux dans plusieurs zones de disponibilité pour RDS.

2. **Pourquoi PostgreSQL?**
   PostgreSQL est disponible en tier gratuit RDS.

3. **Est-ce sécurisé pour la production?**
   Ce déploiement est optimisé pour un POC étudiant, pas pour la production.

4. **Pourquoi Fargate au lieu d'EC2?**
   Fargate élimine le besoin de gérer des serveurs, parfait pour un POC étudiant. 