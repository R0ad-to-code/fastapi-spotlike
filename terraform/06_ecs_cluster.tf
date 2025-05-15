###############################################
# CLUSTER ECS
###############################################

# Cluster ECS pour l'application
resource "aws_ecs_cluster" "app_cluster" {
  name = "${var.project_name}-cluster"
  
  setting {
    name  = "containerInsights"
    value = "disabled"  # économie de coûts
  }
  
  tags = {
    Name = "${var.project_name}-cluster"
  }
} 