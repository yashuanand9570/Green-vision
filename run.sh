#!/bin/bash

echo "========================================"
echo "Forest Cover Type Prediction - Setup"
echo "========================================"
echo ""

echo "Step 1: Checking Python installation..."
python3 --version || python --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python is not installed or not in PATH"
    exit 1
fi
echo ""

echo "Step 2: Installing dependencies..."
pip3 install -r requirements.txt || pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "WARNING: Some packages may have failed to install"
    echo "You may need to install them manually"
fi
echo ""

echo "Step 3: Checking data directory..."
if [ ! -d "data" ]; then
    echo "Creating data directory..."
    mkdir -p data
fi
echo ""

echo "Step 4: Checking zip file..."
if [ -f "data/forest-cover-type.zip" ]; then
    echo "Zip file found!"
else
    echo "WARNING: Zip file not found at data/forest-cover-type.zip"
    echo "Please place your dataset zip file there"
fi
echo ""

echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  python3 app.py"
echo ""
echo "Then visit: http://127.0.0.1:8080/"
echo ""
