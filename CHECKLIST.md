# Deployment Checklist ✅

## Local Setup
- [ ] Python 3.8 installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with credentials
- [ ] Dataset downloaded to `data/forest-cover-type.zip`
- [ ] Application runs locally (`python app.py`)
- [ ] Can access http://127.0.0.1:8080/

## AWS Setup
- [ ] AWS account created
- [ ] AWS CLI installed and configured
- [ ] IAM user with programmatic access created
- [ ] S3 bucket `sensor-tf-state` created for Terraform state
- [ ] S3 buckets for model and prediction data (auto-created by Terraform)
- [ ] ECR repository `sensor` (auto-created by Terraform)
- [ ] EC2 instance (auto-created by Terraform)

## MongoDB Setup
- [ ] MongoDB Atlas account created (or MongoDB installed locally)
- [ ] Database cluster created
- [ ] Connection string obtained
- [ ] Network access configured (allow from anywhere or add EC2 IP)

## GitHub Setup
- [ ] Repository pushed to GitHub
- [ ] GitHub Secrets configured:
  - [ ] `AWS_ACCESS_KEY_ID`
  - [ ] `AWS_SECRET_ACCESS_KEY`
  - [ ] `AWS_DEFAULT_REGION`
  - [ ] `ECR_REPO`
  - [ ] `MONGODB_URL`

## Terraform Deployment
- [ ] Terraform installed (if running locally)
- [ ] `terraform init` executed
- [ ] `terraform apply --auto-approve` executed
- [ ] EC2 instance created and running
- [ ] Security groups allow ports 22 and 8080
- [ ] Elastic IP assigned to EC2

## CI/CD Pipeline
- [ ] Pushed to main branch
- [ ] GitHub Actions workflow triggered
- [ ] Docker image built successfully
- [ ] Image pushed to ECR
- [ ] Application deployed to EC2
- [ ] Application accessible at http://<ec2-ip>:8080/

## Testing
- [ ] Homepage loads
- [ ] Training endpoint works (`/train`)
- [ ] Prediction endpoint works (`/predict`)
- [ ] Models saved to S3
- [ ] Predictions stored in S3
- [ ] Logs visible in `logs/` directory

## Security
- [ ] IAM user has minimal required permissions
- [ ] MongoDB connection string uses strong password
- [ ] Security groups restrict access appropriately
- [ ] S3 buckets have appropriate policies
- [ ] EC2 key pair secured

## Monitoring
- [ ] CloudWatch logs enabled for EC2
- [ ] Application logs being written
- [ ] S3 bucket versioning enabled (optional)
- [ ] Cost alerts configured in AWS

---

## Quick Start Commands

### Local Development
```bash
# Setup
deploy.bat

# Run
python app.py
```

### Infrastructure (Local Terraform)
```bash
cd infrastructure/
terraform init
terraform apply --auto-approve
```

### Push to Deploy
```bash
git add .
git commit -m "Your changes"
git push origin main
```

---

## Troubleshooting

### Docker Build Fails
- Check Docker Desktop is running
- Ensure enough disk space
- Try `docker system prune`

### Terraform Fails
- Check AWS credentials: `aws configure`
- Verify S3 bucket for state exists
- Check region matches: `us-east-1`

### GitHub Actions Fails
- Verify all secrets are set correctly
- Check workflow logs for specific errors
- Ensure branch is `main`

### Application Won't Start
- Check `.env` file exists with correct values
- Verify MongoDB connection string
- Check AWS credentials have S3 permissions
- Review logs in `logs/` directory
