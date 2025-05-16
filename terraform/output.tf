output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.spotlike_alb.dns_name
}

output "db_endpoint" {
  description = "Endpoint of the RDS instance"
  value       = aws_db_instance.spotlike_postgres.endpoint
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket for storage"
  value       = aws_s3_bucket.spotlike_storage.bucket
}