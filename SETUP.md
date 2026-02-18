# 🌲 Green-Vision Setup Guide

Complete guide to set up the Green-Vision Forest Prediction Project from scratch.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [AWS Configuration](#aws-configuration)
4. [MongoDB Configuration](#mongodb-configuration)
5. [GitHub Repository Setup](#github-repository-setup)
6. [Running the Application](#running-the-application)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Docker** (optional for local containerized testing) - [Download](https://docs.docker.com/get-docker/)

### Required Accounts
- **AWS Account** - [Sign Up](https://aws.amazon.com/)
- **MongoDB Atlas** (or any MongoDB instance) - [Sign Up](https://www.mongodb.com/cloud/atlas/register)
- **GitHub Account** - [Sign Up](https://github.com/join)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yashuanand9570/Green-vision.git
cd Green-vision
```

### 2. Run Setup Script

#### On Windows:
```cmd
deploy.bat
```

#### On Linux/Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

The setup script will:
- ✅ Check Python installation
- ✅ Install required dependencies
- ✅ Create `.env` file from template
- ✅ Build Docker image (if Docker is installed)
- ✅ Create necessary directories (data, models, predictions, logs)

### 3. Configure Environment Variables

Edit the `.env` file with your credentials:

```bash
# On Linux/Mac
nano .env

# On Windows
notepad .env
```

Update the following variables:
```env
AWS_ACCESS_KEY_ID=your_actual_aws_access_key
AWS_SECRET_ACCESS_KEY=your_actual_aws_secret_key
AWS_DEFAULT_REGION=us-east-1

MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

### 4. Download Dataset (Optional for Training)

Download the Forest Cover Type dataset:
1. Visit: https://www.kaggle.com/competitions/forest-cover-type-prediction/data
2. Download the dataset ZIP file
3. Place it in: `data/forest-cover-type.zip`

---

## AWS Configuration

### 1. Create IAM User

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Create a new user with **Programmatic access**
3. Attach the following policies:
   - `AmazonEC2FullAccess`
   - `AmazonS3FullAccess`
   - `AmazonECRFullAccess`
   - Or create a custom policy with minimal required permissions

4. Save the **Access Key ID** and **Secret Access Key**

### 2. Configure AWS CLI (Optional but Recommended)

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1`
- Default output format: `json`

### 3. Create S3 Bucket for Terraform State

```bash
aws s3 mb s3://sensor-tf-state --region us-east-1
```

This bucket stores Terraform state for infrastructure management.

---

## MongoDB Configuration

### Option A: MongoDB Atlas (Recommended for Cloud)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user:
   - Username: `your_username`
   - Password: `your_password`
4. Whitelist your IP address (or use `0.0.0.0/0` for testing)
5. Get connection string:
   ```
   mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

### Option B: Local MongoDB

1. Install MongoDB locally
2. Start MongoDB service:
   ```bash
   # Linux
   sudo systemctl start mongod
   
   # Mac
   brew services start mongodb-community
   
   # Windows
   net start MongoDB
   ```
3. Connection string: `mongodb://localhost:27017/`

---

## GitHub Repository Setup

### 1. Fork/Clone Repository

If you haven't already:
```bash
git clone https://github.com/yashuanand9570/Green-vision.git
cd Green-vision
```

### 2. Configure GitHub Secrets

For automated deployment, add these secrets to your repository:

1. Go to: **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Add the following secrets:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `AWS_DEFAULT_REGION` | AWS Region | `us-east-1` |
| `ECR_REPO` | ECR Repository Name | `sensor` |
| `MONGODB_URL` | MongoDB Connection String | `mongodb+srv://user:pass@cluster.mongodb.net/` |

### 3. Set Up Self-Hosted Runner (For EC2 Deployment)

The CI/CD pipeline uses a self-hosted runner on EC2. After deploying infrastructure:

1. Go to: **Settings → Actions → Runners → New self-hosted runner**
2. Follow instructions to install runner on your EC2 instance
3. Configure and start the runner service

---

## Running the Application

### Local Development

#### Method 1: Direct Python
```bash
python app.py
```

Visit: http://127.0.0.1:8080/

#### Method 2: Using Run Script

**Windows:**
```cmd
run.bat
```

**Linux/Mac:**
```bash
./run.sh
```

#### Method 3: Docker
```bash
docker build -t greenvision:latest .
docker run -d -p 8080:8080 --env-file .env greenvision:latest
```

Visit: http://localhost:8080/

### Cloud Deployment

1. Ensure GitHub secrets are configured
2. Push to main branch:
   ```bash
   git add .
   git commit -m "Deploy application"
   git push origin main
   ```
3. GitHub Actions will automatically:
   - Build Docker image
   - Push to AWS ECR
   - Deploy to EC2 instance

---

## Application Features

Once running, you can access:

- **Home Page**: `http://localhost:8080/`
- **Train Model**: `http://localhost:8080/train`
- **Make Predictions**: `http://localhost:8080/predict`

---

## Project Structure

```
Green-vision/
├── app.py                    # Main FastAPI application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── deploy.sh / deploy.bat   # Deployment scripts
├── run.sh / run.bat        # Local run scripts
├── .env.example            # Environment template
├── setup.py                # Package setup
│
├── src/forest/             # Main source code
│   ├── components/        # ML pipeline components
│   ├── configuration/     # AWS & MongoDB config
│   ├── constant/         # Application constants
│   ├── entity/           # Data entities
│   ├── pipeline/         # Training & prediction pipelines
│   └── utils/            # Utility functions
│
├── infrastructure/        # Terraform IaC
│   ├── sensor_ec2/       # EC2 instance config
│   ├── sensor_ecr/       # ECR repository config
│   ├── sensor_model_bucket/    # S3 model storage
│   └── sensor_pred_data_bucket/ # S3 predictions storage
│
├── .github/workflows/    # GitHub Actions
│   ├── main.yml         # CI/CD pipeline
│   └── terraform.yml    # Infrastructure deployment
│
├── templates/           # Web UI templates
├── config/             # Configuration files
├── data/              # Training data
├── models/            # Trained models
├── predictions/       # Prediction outputs
└── docs/             # Documentation
```

---

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
ModuleNotFoundError: No module named 'src'
```
**Solution:** Install the package in editable mode:
```bash
pip install -e .
```

#### 2. AWS Credentials Not Found
```
NoCredentialsError: Unable to locate credentials
```
**Solution:** 
- Check `.env` file has correct AWS credentials
- Or run `aws configure` to set credentials globally

#### 3. MongoDB Connection Failed
```
pymongo.errors.ServerSelectionTimeoutError
```
**Solution:**
- Verify MongoDB URL in `.env`
- Check network connectivity
- Whitelist your IP in MongoDB Atlas

#### 4. Docker Build Failed
```
ERROR: failed to solve: process "/bin/sh -c pip install" didn't complete successfully
```
**Solution:**
- Check internet connection
- Try building with `--no-cache`: `docker build --no-cache -t greenvision:latest .`

#### 5. Port Already in Use
```
Error: Address already in use (Port 8080)
```
**Solution:**
- Kill process using port: `lsof -ti:8080 | xargs kill -9` (Linux/Mac)
- Or change port in `.env`: `APP_PORT=8081`

### Getting Help

- 📖 Check [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment specifics
- 📋 Check [CHECKLIST.md](./CHECKLIST.md) for pre-deployment verification
- 🐛 Open an issue on GitHub
- 📧 Contact: yashuanand9570@github.com

---

## Next Steps

After successful setup:

1. ✅ Read [DEPLOYMENT.md](./DEPLOYMENT.md) for cloud deployment
2. ✅ Review [CHECKLIST.md](./CHECKLIST.md) before deploying
3. ✅ Explore the codebase and customize as needed
4. ✅ Train your model with actual data
5. ✅ Deploy to production!

---

**Happy Coding! 🚀**
