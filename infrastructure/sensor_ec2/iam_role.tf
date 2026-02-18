# IAM Role for EC2 Instance
resource "aws_iam_role" "ec2_role" {
  name = "sensor-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "sensor-ec2-role"
  }
}

# IAM Policy for S3 Access
resource "aws_iam_role_policy" "ec2_s3_policy" {
  name = "sensor-ec2-s3-policy"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ]
        Resource = [
          "arn:aws:s3:::*-sensor-model-bucket",
          "arn:aws:s3:::*-sensor-model-bucket/*",
          "arn:aws:s3:::*-sensor-pred-data-bucket",
          "arn:aws:s3:::*-sensor-pred-data-bucket/*"
        ]
      }
    ]
  })
}

# IAM Policy for ECR Access
resource "aws_iam_role_policy" "ec2_ecr_policy" {
  name = "sensor-ec2-ecr-policy"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM Instance Profile
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "sensor-ec2-instance-profile"
  role = aws_iam_role.ec2_role.name

  tags = {
    Name = "sensor-ec2-instance-profile"
  }
}
