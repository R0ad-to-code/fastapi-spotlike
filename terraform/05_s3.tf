resource "aws_s3_bucket" "spotlike_storage" {
  bucket = "spotlike-storage-${var.environment}-${random_id.bucket_suffix.hex}"
  
  tags = {
    Name        = "Spotlike Storage"
    Environment = var.environment
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_public_access_block" "spotlike_storage_access" {
  bucket = aws_s3_bucket.spotlike_storage.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}