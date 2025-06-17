variable "project_name" {
  description = "Nom du projet"
  type        = string
  default = "Spotilike"

}

variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default = "eu-west-3"

}

variable "environment" {
  description = "The deployment environment"
  type        = string
  default = "prod"
}

variable "db_password" {
  description = "PostgreSQL database password"
  type        = string
  sensitive   = true
}

variable "api_ecr_repo_url" {
  description = "URL of the ECR repository containing the FastAPI application image"
  type        = string
}

variable "frontend_ecr_repo_url" {
  description = "URL of the ECR repository containing the Frontend application image"
  type        = string
}