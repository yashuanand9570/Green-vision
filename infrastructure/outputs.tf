# EC2 Outputs
output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = module.sensor_ec2.ec2_public_ip
}

output "ec2_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = module.sensor_ec2.ec2_public_dns
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = module.sensor_ec2.ec2_instance_id
}

# ECR Outputs
output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = module.sensor_ecr.ecr_repository_url
}

output "ecr_repository_name" {
  description = "Name of the ECR repository"
  value       = module.sensor_ecr.ecr_repository_name
}

# S3 Model Bucket Outputs
output "model_bucket_name" {
  description = "Name of the S3 bucket for models"
  value       = module.sensor_model.model_bucket_name
}

# S3 Prediction Data Bucket Outputs
output "pred_data_bucket_name" {
  description = "Name of the S3 bucket for prediction data"
  value       = module.sensor_pred_data.pred_data_bucket_name
}

# Application URL
output "application_url" {
  description = "URL to access the deployed application"
  value       = "http://${module.sensor_ec2.ec2_public_ip}:8080"
}
