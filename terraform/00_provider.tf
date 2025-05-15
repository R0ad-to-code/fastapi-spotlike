###############################################
# CONFIGURATION DE BASE TERRAFORM
###############################################

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.0.0"
}

# Configuration du provider AWS
provider "aws" {
  region = var.aws_region
} 