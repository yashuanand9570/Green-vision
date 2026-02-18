@echo off
echo ========================================
echo GreenVision - Full Deployment Setup
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo Step 2: Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install
)
echo.

echo Step 3: Creating .env file...
if not exist ".env" (
    copy .env.example .env
    echo Created .env file - Please edit with your credentials!
) else (
    echo .env file already exists
)
echo.

echo Step 4: Building Docker image...
docker --version
if errorlevel 1 (
    echo WARNING: Docker is not installed. Skipping Docker build.
    echo Install Docker Desktop: https://www.docker.com/products/docker-desktop
) else (
    docker build -t greenvision:latest .
    echo Docker image built successfully!
)
echo.

echo Step 5: Checking data directory...
if not exist "data" (
    echo Creating data directory...
    mkdir data
)
if exist "data\forest-cover-type.zip" (
    echo Dataset found!
) else (
    echo WARNING: Dataset not found
    echo Download from: https://www.kaggle.com/competitions/forest-cover-type-prediction/data
    echo Place it at: data\forest-cover-type.zip
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Edit .env file with your AWS and MongoDB credentials
echo 2. Run: python app.py
echo 3. Visit: http://127.0.0.1:8080/
echo.
echo For cloud deployment:
echo 1. Configure GitHub Secrets (see DEPLOYMENT.md)
echo 2. Create S3 bucket: aws s3 mb s3://sensor-tf-state
echo 3. Push to main branch to trigger CI/CD
echo.
pause
