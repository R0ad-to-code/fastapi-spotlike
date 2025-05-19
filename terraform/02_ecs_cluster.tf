resource "aws_ecs_cluster" "spotlike_cluster" {
  name = "spotlike-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Name = "spotlike-cluster"
    Environment = "dev"
  }
}

resource "aws_ecs_cluster_capacity_providers" "spotlike_cluster_capacity" {
  cluster_name = aws_ecs_cluster.spotlike_cluster.name
  
  capacity_providers = ["FARGATE", "FARGATE_SPOT"]
  
  default_capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 1
    base              = 1
  }
}