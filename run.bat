@echo off
echo ========================================
echo Forest Cover Type Prediction - Setup
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
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install
    echo You may need to install them manually
)
echo.

echo Step 3: Checking data directory...
if not exist "data" (
    echo Creating data directory...
    mkdir data
)
echo.

echo Step 4: Checking zip file...
if exist "data\forest-cover-type.zip" (
    echo Zip file found!
) else (
    echo WARNING: Zip file not found at data\forest-cover-type.zip
    echo Please place your dataset zip file there
)
echo.

echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To run the application:
echo   python app.py
echo.
echo Then visit: http://127.0.0.1:8080/
echo.
pause
