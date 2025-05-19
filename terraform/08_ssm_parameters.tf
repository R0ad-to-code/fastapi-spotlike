resource "aws_ssm_parameter" "db_password" {
  name        = "/${var.project_name}/${var.environment}/db-password"
  description = "Mot de passe pour la base de données PostgreSQL"
  type        = "SecureString"
  value       = var.db_password
  
  tags = {
    Name        = "${var.project_name}-db-password"
    Environment = var.environment
  }
}