# Rôle pour l'exécution des tâches ECS
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "spotlike-task-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

# Politique d'exécution de tâche standard
resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Rôle pour l'application elle-même (pour accéder à S3, etc.)
resource "aws_iam_role" "app_role" {
  name = "spotlike-app-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

# Politique pour accès S3
resource "aws_iam_policy" "s3_access_policy" {
  name        = "spotlike-s3-access"
  description = "Allow access to S3 bucket for storage"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
        "s3:DeleteObject"
      ]
      Effect   = "Allow"
      Resource = [
        "arn:aws:s3:::spotlike-storage-*",
        "arn:aws:s3:::spotlike-storage-*/*"
      ]
    }]
  })
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  role       = aws_iam_role.app_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}
