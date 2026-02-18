# 🚀 GreenVision Deployment Guide

## Prerequisites
- AWS Account
- MongoDB Atlas Account (or any MongoDB instance)
- GitHub Account

## Step 1: Configure GitHub Secrets

Go to your repository: **Settings → Secrets and variables → Actions → New repository secret**

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `AWS_DEFAULT_REGION` | `us-east-1` |
| `ECR_REPO` | `sensor` |
| `MONGODB_URL` | `mongodb+srv://<user>:<pass>@cluster.mongodb.net/` |

## Step 2: Create Terraform State Bucket

Run this AWS CLI command:
```bash
aws s3 mb s3://sensor-tf-state --region us-east-1
```

Or create manually in AWS S3 Console.

## Step 3: Deploy Infrastructure with Terraform

### Option A: Using GitHub Actions (Recommended)
The `terraform.yml` workflow will automatically run when you push changes to the `infrastructure/` folder.

### Option B: Local Terraform
```bash
cd infrastructure/
terraform init
terraform apply --auto-approve
```

## Step 4: Trigger CI/CD Pipeline

Push to main branch to trigger automatic deployment:
```bash
git push origin main
```

GitHub Actions will:
1. Build Docker image
2. Push to AWS ECR
3. Deploy to EC2 instance

## Step 5: Access Application

Once deployed, access at:
```
http://<your-ec2-public-ip>:8080/
```

## Local Development

```bash
# Create environment
conda create -p venv python==3.8 -y
conda activate ./venv

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AWS_ACCESS_KEY_ID=<your-key>
export AWS_SECRET_ACCESS_KEY=<your-secret>
export AWS_DEFAULT_REGION=us-east-1
export MONGODB_URL="<your-mongodb-url>"

# Run application
python app.py
```

## Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Main UI |
| `/train` | Train the model |
| `/predict` | Run predictions |

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   GitHub    │────▶│  AWS ECR     │────▶│  AWS EC2    │
│   Actions   │     │  (Docker)    │     │  (App)      │
└─────────────┘     └──────────────┘     └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌──────────────┐     ┌─────────────┐
                    │  AWS S3      │     │  MongoDB    │
                    │  (Models)    │     │  (Data)     │
                    └──────────────┘     └─────────────┘
```
