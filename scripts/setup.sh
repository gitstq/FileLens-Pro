#!/bin/bash
# FileLens Setup Script for Linux/macOS

set -e

echo "🔍 FileLens Setup Script"
echo "========================"

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if Python 3.8+ is installed
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "❌ Python 3.8 or higher is required"
    exit 1
fi
echo "✅ Python version OK"

# Check Node.js
echo "Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi
node_version=$(node --version)
echo "Node.js version: $node_version"
echo "✅ Node.js OK"

# Create virtual environment
echo "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "To start FileLens:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start backend: python src/main.py"
echo "  3. In another terminal, start frontend: npm start"
echo ""
