resource "aws_security_group" "spotlike_ecs_sg" {
  name        = "spotlike-ecs-sg"
  description = "Allow inbound traffic to ECS"
  vpc_id      = module.vpc_spotlike.vpc_id
  
  ingress {
    from_port   = 8000  # Port FastAPI
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80  # Port Nginx frontend
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "spotlike_db_sg" {
  name        = "spotlike-db-sg"
  description = "Allow PostgreSQL inbound traffic from ECS"
  vpc_id      = module.vpc_spotlike.vpc_id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.spotlike_ecs_sg.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "spotlike_alb_sg" {
  name        = "spotlike-alb-sg"
  description = "Allow inbound traffic to ALB"
  vpc_id      = module.vpc_spotlike.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}