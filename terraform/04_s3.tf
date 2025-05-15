###############################################
# STOCKAGE S3
###############################################

# Bucket S3 pour les médias
resource "aws_s3_bucket" "media_bucket" {
  bucket = "${var.project_name}-media-${var.environment}"
  
  tags = {
    Name = "${var.project_name}-media"
  }
}

# Sécurisation du bucket S3
resource "aws_s3_bucket_public_access_block" "media_block" {
  bucket                  = aws_s3_bucket.media_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
} 