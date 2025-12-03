#!/bin/bash
# run.sh - Quick start script for NLP Expert System

set -e

echo "🚀 NLP Expert System - Quick Start"
echo "=================================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r backend/requirements.txt

# Download spaCy model if not present
echo "🧠 Checking spaCy model..."
python -m spacy download -q en_core_web_sm 2>/dev/null || echo "   (spaCy model already installed)"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the system:"
echo ""
echo "Terminal 1 - Backend (FastAPI):"
echo "  cd backend"
echo "  uvicorn app:app --reload --port 8000"
echo ""
echo "Terminal 2 - Frontend (HTTP Server):"
echo "  python -m http.server 5500"
echo ""
echo "Then open: http://localhost:5500/frontend/index.html"
echo ""
