# repository ECR existants
data "aws_ecr_repository" "spotlike_api" {
  name = "spotlike-api"
}

data "aws_ecr_repository" "spotlike_frontend" {
  name = "spotlike-frontend"
}

# nettoyage anciennes images API
resource "aws_ecr_lifecycle_policy" "spotlike_api_lifecycle" {
  repository = data.aws_ecr_repository.spotlike_api.name  

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last 5 images",
        selection = {
          tagStatus     = "any",
          countType     = "imageCountMoreThan",
          countNumber   = 5
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# nettoyage anciennes images Frontend
resource "aws_ecr_lifecycle_policy" "spotlike_frontend_lifecycle" {
  repository = data.aws_ecr_repository.spotlike_frontend.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last 5 images",
        selection = {
          tagStatus     = "any",
          countType     = "imageCountMoreThan",
          countNumber   = 5
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# Output des repository URLs
output "api_repository_url" {
  description = "URL du repository ECR pour l'API FastAPI"
  value       = data.aws_ecr_repository.spotlike_api.repository_url
}

output "frontend_repository_url" {
  description = "URL du repository ECR pour le Frontend"
  value       = data.aws_ecr_repository.spotlike_frontend.repository_url
}