###############################################
# SORTIES
###############################################

output "db_endpoint" {
  description = "Endpoint de la base de données"
  value       = aws_db_instance.postgres.endpoint
}

output "s3_bucket" {
  description = "Nom du bucket S3"
  value       = aws_s3_bucket.media_bucket.id
}

output "backend_service" {
  description = "Service ECS Backend"
  value       = aws_ecs_service.backend_service.name
}

output "frontend_service" {
  description = "Service ECS Frontend"
  value       = aws_ecs_service.frontend_service.name
} 