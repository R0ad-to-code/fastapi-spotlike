output "alb_dns_name" {
  description = "nom de domaine de l'ALB"
  value       = aws_lb.spotlike_alb.dns_name
}

output "db_endpoint" {
  description = "nom de l'endpoint BD Postgres"
  value       = aws_db_instance.spotlike_postgres.endpoint
}

output "s3_bucket_name" {
  description = "nom du bucket S3"
  value       = aws_s3_bucket.spotlike_storage.bucket
}