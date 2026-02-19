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

### Option A: Using GitHub Actions UI (Recommended - No Terminal Needed!)

We have three GitHub Actions workflows for infrastructure management:

#### 1. **Deploy Infrastructure** (`deploy-infrastructure.yml`)
- **Purpose**: Deploy, update, or destroy infrastructure
- **How to run**:
  1. Go to **Actions** tab in GitHub
  2. Click **Deploy Infrastructure** workflow
  3. Click **Run workflow** button
  4. Select options:
     - **Environment**: `dev`, `staging`, or `production`
     - **Terraform action**: `plan`, `apply`, or `destroy`
  5. Click **Run workflow**
- **Features**:
  - Shows step-by-step progress in real-time
  - Displays all resource IDs and IPs in job summary
  - Saves Terraform outputs as downloadable artifacts
  - Automatically creates job summary with connection details

#### 2. **Infrastructure Status** (`infrastructure-status.yml`)
- **Purpose**: Check current infrastructure status without making changes
- **How to run**:
  1. Go to **Actions** tab in GitHub
  2. Click **Infrastructure Status** workflow
  3. Click **Run workflow** button
  4. Choose detailed output (optional)
  5. Click **Run workflow**
- **Features**:
  - Shows current Terraform state
  - Lists all running AWS resources
  - Displays public IPs and connection info
  - Generates downloadable status report

#### 3. **Auto Deploy** (`terraform.yml`)
- **Purpose**: Automatically deploys when infrastructure code changes
- **Trigger**: Automatically runs on push to `main` branch with changes to `infrastructure/`

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

After running the **Deploy Infrastructure** workflow, you'll see a job summary with:
- **EC2 Instance**: Instance ID, Public IP, Public DNS
- **ECR Repository**: Repository URL and Name
- **S3 Buckets**: Model bucket and Prediction data bucket names
- **Application URL**: Direct link to access your application

Once deployed, access at:
```
http://<your-ec2-public-ip>:8080/
```

You can also download the `terraform-outputs` artifact from the workflow run for detailed JSON output.

### Quick Status Check
To quickly check what's running without making changes:
1. Go to **Actions** → **Infrastructure Status**
2. Click **Run workflow**
3. View the summary for all connection details

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
