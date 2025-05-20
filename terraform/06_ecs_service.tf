resource "aws_ecs_task_definition" "spotlike_task" {
  family                   = "spotlike-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"  # Augmenter pour deux conteneurs
  memory                   = "1024" # Augmenter pour deux conteneurs
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  
  container_definitions = jsonencode([
    {
      name      = "api-container"
      image     = "${var.api_ecr_repo_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]
      environment = [
        { name = "DB_HOST", value = aws_db_instance.spotlike_postgres.address },
        { name = "DB_PORT", value = "5432" },
        { name = "DB_NAME", value = "spotilike_db" },
        { name = "DB_USER", value = "postgres" },
        { name = "DB_PASSWORD", value = var.db_password },  # Mot de passe directement ici
        { name = "S3_BUCKET", value = aws_s3_bucket.spotlike_storage.bucket }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/spotlike-logs"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "api"
        }
      }
    },
    {
      name      = "frontend-container"
      image     = "${var.frontend_ecr_repo_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
        }
      ]
      environment = [
        { name = "API_URL", value = "/api" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/spotlike-logs"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "frontend"
        }
      }
    }
  ])
}

resource "aws_cloudwatch_log_group" "spotlike_logs" {
  name              = "/ecs/spotlike-logs"
  retention_in_days = 30
}

# Application Load Balancer
resource "aws_lb" "spotlike_alb" {
  name               = "spotlike-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.spotlike_alb_sg.id]
  subnets            = module.vpc_spotlike.public_subnets
}


# Target group pour l'API
resource "aws_lb_target_group" "api_tg" {
  name        = "spotlike-api-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = module.vpc_spotlike.vpc_id
  target_type = "ip"
  
  health_check {
    path                = "/api/health"
    port                = "traffic-port"
    healthy_threshold   = 3
    unhealthy_threshold = 3
    timeout             = 30
    interval            = 60
    matcher             = "200"
  }
}

# Target group pour le frontend
resource "aws_lb_target_group" "frontend_tg" {
  name        = "spotlike-frontend-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = module.vpc_spotlike.vpc_id
  target_type = "ip"
  
  health_check {
    path                = "/"
    port                = "traffic-port"
    healthy_threshold   = 3
    unhealthy_threshold = 3
    timeout             = 30
    interval            = 60
    matcher             = "200"
  }
}

# Listener pour rediriger vers le frontend par défaut
resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.spotlike_alb.arn
  port              = 80
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend_tg.arn
  }
}
# Listener rule pour diriger vers l'API quand le path commence par /api
resource "aws_lb_listener_rule" "api_rule" {
  listener_arn = aws_lb_listener.http_listener.arn
  priority     = 100
  
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api_tg.arn
  }
  
  condition {
    path_pattern {
      values = ["/api/*", "/docs", "/openapi.json", "/api/openapi.json"]
    }
  }
}

resource "aws_ecs_service" "spotlike_service" {
  name            = "spotlike-service"
  cluster         = aws_ecs_cluster.spotlike_cluster.id
  task_definition = aws_ecs_task_definition.spotlike_task.arn
  launch_type     = "FARGATE"
  desired_count   = 2
  
  network_configuration {
    subnets          = module.vpc_spotlike.private_subnets
    security_groups  = [aws_security_group.spotlike_ecs_sg.id]
    assign_public_ip = false
  }
  
  # Configuration pour le conteneur API
  load_balancer {
    target_group_arn = aws_lb_target_group.api_tg.arn
    container_name   = "api-container"
    container_port   = 8000
  }
  
  # Configuration pour le conteneur Frontend
  load_balancer {
    target_group_arn = aws_lb_target_group.frontend_tg.arn
    container_name   = "frontend-container"
    container_port   = 80
  }
  
  depends_on = [aws_lb_listener.http_listener]

}