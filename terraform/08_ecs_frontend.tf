###############################################
# SERVICE ECS FRONTEND
###############################################

# Définition de tâche pour le frontend
resource "aws_ecs_task_definition" "frontend_task" {
  family                   = "${var.project_name}-frontend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.ecs_task_cpu
  memory                   = var.ecs_task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  
  container_definitions = jsonencode([{
    name      = "${var.project_name}-frontend-container"
    image     = "public.ecr.aws/docker/library/nginx:latest" # Image de base pour démo
    essential = true
    
    portMappings = [{
      containerPort = 80
      hostPort      = 80
      protocol      = "tcp"
    }]
    
    environment = [
      { name = "API_URL", value = "http://backend.${var.project_name}.local:8000" }
    ]
    
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/${var.project_name}-frontend"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
        "awslogs-create-group"  = "true"
      }
    }
  }])
  
  tags = {
    Name = "${var.project_name}-frontend-task"
  }
}

# Service ECS pour le frontend
resource "aws_ecs_service" "frontend_service" {
  name            = "${var.project_name}-frontend-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.frontend_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true  # Pour simplifier l'architecture
  }
  
  tags = {
    Name = "${var.project_name}-frontend-service"
  }
} 