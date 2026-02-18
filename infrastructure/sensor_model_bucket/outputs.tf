output "model_bucket_name" {
  description = "Name of the S3 bucket for models"
  value       = aws_s3_bucket.model_bucket.id
}

output "model_bucket_arn" {
  description = "ARN of the S3 bucket for models"
  value       = aws_s3_bucket.model_bucket.arn
}

output "model_bucket_region" {
  description = "Region of the S3 bucket for models"
  value       = aws_s3_bucket.model_bucket.region
}
