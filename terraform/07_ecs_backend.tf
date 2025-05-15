###############################################
# SERVICE ECS BACKEND
###############################################

# Définition de tâche pour le backend
resource "aws_ecs_task_definition" "backend_task" {
  family                   = "${var.project_name}-backend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.ecs_task_cpu
  memory                   = var.ecs_task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  
  container_definitions = jsonencode([{
    name      = "${var.project_name}-backend-container"
    image     = "public.ecr.aws/docker/library/python:3.9-slim" # Image de base pour démo
    essential = true
    
    portMappings = [{
      containerPort = 8000
      hostPort      = 8000
      protocol      = "tcp"
    }]
    
    environment = [
      { name = "DATABASE_URL", value = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.postgres.endpoint}/${var.db_name}" },
      { name = "MEDIA_BUCKET", value = aws_s3_bucket.media_bucket.id }
    ]
    
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/${var.project_name}-backend"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
        "awslogs-create-group"  = "true"
      }
    }
  }])
  
  tags = {
    Name = "${var.project_name}-backend-task"
  }
}

# Service ECS pour le backend
resource "aws_ecs_service" "backend_service" {
  name            = "${var.project_name}-backend-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.backend_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true  # Pour simplifier l'architecture
  }
  
  tags = {
    Name = "${var.project_name}-backend-service"
  }
} 