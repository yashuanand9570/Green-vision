#!/bin/bash

echo "========================================"
echo "GreenVision - Full Deployment Setup"
echo "========================================"
echo ""

# Check if running as root (optional for Docker)
if [ "$EUID" -eq 0 ]; then 
    echo "Running as root user"
fi

# Function to check command existence
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check Python installation
echo "Step 1: Checking Python installation..."
if command_exists python3; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
elif command_exists python; then
    PYTHON_CMD=python
    PIP_CMD=pip
else
    echo "ERROR: Python is not installed or not in PATH"
    exit 1
fi

$PYTHON_CMD --version
echo ""

# Step 2: Install dependencies
echo "Step 2: Installing dependencies..."
$PIP_CMD install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "WARNING: Some packages may have failed to install"
fi
echo ""

# Step 3: Create .env file
echo "Step 3: Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file - Please edit with your credentials!"
    echo "Edit .env with: nano .env or vim .env"
else
    echo ".env file already exists"
fi
echo ""

# Step 4: Check and build Docker image
echo "Step 4: Building Docker image..."
if command_exists docker; then
    docker --version
    docker build -t greenvision:latest .
    if [ $? -eq 0 ]; then
        echo "Docker image built successfully!"
    else
        echo "ERROR: Docker build failed"
    fi
else
    echo "WARNING: Docker is not installed. Skipping Docker build."
    echo "Install Docker: https://docs.docker.com/get-docker/"
fi
echo ""

# Step 5: Check data directory
echo "Step 5: Checking data directory..."
if [ ! -d "data" ]; then
    echo "Creating data directory..."
    mkdir -p data
fi

if [ -f "data/forest-cover-type.zip" ]; then
    echo "Dataset found!"
else
    echo "WARNING: Dataset not found"
    echo "Download from: https://www.kaggle.com/competitions/forest-cover-type-prediction/data"
    echo "Place it at: data/forest-cover-type.zip"
fi
echo ""

# Step 6: Check AWS CLI (optional)
echo "Step 6: Checking AWS CLI..."
if command_exists aws; then
    aws --version
    echo "AWS CLI is installed"
else
    echo "WARNING: AWS CLI not installed (optional for local development)"
    echo "Install AWS CLI: https://aws.amazon.com/cli/"
fi
echo ""

# Step 7: Create necessary directories
echo "Step 7: Creating necessary directories..."
mkdir -p models predictions logs
echo "Directories created: models, predictions, logs"
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next Steps:"
echo "1. Edit .env file with your AWS and MongoDB credentials"
echo "   Command: nano .env"
echo "2. Run application locally:"
echo "   Command: $PYTHON_CMD app.py"
echo "3. Visit: http://127.0.0.1:8080/"
echo ""
echo "For Docker deployment:"
echo "   docker run -d -p 8080:8080 --env-file .env greenvision:latest"
echo ""
echo "For cloud deployment:"
echo "1. Configure GitHub Secrets (see DEPLOYMENT.md)"
echo "2. Create S3 bucket: aws s3 mb s3://sensor-tf-state --region us-east-1"
echo "3. Push to main branch to trigger CI/CD"
echo ""
