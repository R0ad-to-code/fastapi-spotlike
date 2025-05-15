###############################################
# VARIABLES DE BASE POUR LE DÉPLOIEMENT AWS
###############################################

# Région où déployer les ressources (Paris)
# On utilise Paris car c'est la région la plus proche pour réduire la latence
variable "aws_region" {
  description = "La région AWS où déployer les ressources"
  type        = string
  default     = "eu-west-3" # Paris
}

# Nom du projet pour les tags des ressources
variable "project_name" {
  description = "Nom du projet pour identifier les ressources facilement"
  type        = string
  default     = "spotilike"
}

# Environnement (dev, staging, prod)
variable "environment" {
  description = "Environnement (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR du VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Zones de disponibilité"
  type        = list(string)
  default     = ["eu-west-3a", "eu-west-3b"]
}

###############################################
# VARIABLES POUR LA BASE DE DONNÉES
###############################################

# Infos de connexion à la base de données
variable "db_username" {
  description = "Nom d'utilisateur pour la base de données RDS"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Mot de passe pour la base de données RDS (à changer en production)"
  type        = string
  default     = "postgres12345" # Pour projet étudiant seulement
  sensitive   = true
}

variable "db_name" {
  description = "Nom de la base de données"
  type        = string
  default     = "spotilike_db"
}

variable "eks_node_instance_type" {
  description = "Type d'instance pour les nœuds EKS"
  type        = string
  default     = "t3.micro" # Type éligible à l'offre gratuite
}

variable "ecs_task_cpu" {
  description = "CPU allouée aux tâches ECS (en unités)"
  type        = number
  default     = 256 # 0.25 vCPU
}

variable "ecs_task_memory" {
  description = "Mémoire allouée aux tâches ECS (en MiB)"
  type        = number
  default     = 512 # 0.5 GB
} 