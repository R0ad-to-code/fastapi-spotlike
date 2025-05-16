variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "environment" {
  description = "The deployment environment"
  type        = string
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