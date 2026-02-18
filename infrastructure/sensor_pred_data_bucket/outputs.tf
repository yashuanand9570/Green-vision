output "pred_data_bucket_name" {
  description = "Name of the S3 bucket for prediction data"
  value       = aws_s3_bucket.pred_data_bucket.id
}

output "pred_data_bucket_arn" {
  description = "ARN of the S3 bucket for prediction data"
  value       = aws_s3_bucket.pred_data_bucket.arn
}

output "pred_data_bucket_region" {
  description = "Region of the S3 bucket for prediction data"
  value       = aws_s3_bucket.pred_data_bucket.region
}
