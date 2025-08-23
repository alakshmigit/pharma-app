#!/bin/bash

# Dependency installation script with pyarrow fix
# This script tries multiple approaches to install dependencies

set -e  # Exit on any error

echo "🔧 Installing Pharma App Dependencies"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Upgrade pip first
echo "📦 Upgrading pip..."
pip install --upgrade pip
print_status "Pip upgraded"

# Try to install pyarrow with pre-built wheel first
echo "🏗️  Attempting to install pyarrow with pre-built wheel..."
if pip install --only-binary=pyarrow pyarrow; then
    print_status "PyArrow installed successfully with pre-built wheel"
    PYARROW_SUCCESS=true
else
    print_warning "Pre-built wheel installation failed, trying alternative approach..."
    PYARROW_SUCCESS=false
fi

# Install core backend dependencies (these should work)
echo "📦 Installing core backend dependencies..."
pip install fastapi==0.104.1 uvicorn==0.24.0 sqlalchemy==2.0.23 pydantic==2.5.0 python-multipart==0.0.6 requests==2.31.0 python-dotenv==1.0.0 psycopg2-binary python-jose[cryptography] passlib[bcrypt]
print_status "Core backend dependencies installed"

# Try to install pandas (might need pyarrow)
echo "📊 Installing pandas..."
if pip install pandas==2.1.3; then
    print_status "Pandas installed successfully"
else
    print_warning "Pandas installation failed, trying without version constraint..."
    pip install pandas
    print_status "Pandas installed (latest version)"
fi

# Try to install streamlit if pyarrow worked
if [ "$PYARROW_SUCCESS" = true ]; then
    echo "🎨 Installing Streamlit..."
    if pip install streamlit==1.28.1; then
        print_status "Streamlit installed successfully"
    else
        print_warning "Streamlit 1.28.1 failed, trying older version..."
        pip install streamlit==1.25.0
        print_status "Streamlit installed (older version)"
    fi
else
    print_warning "Skipping Streamlit installation due to pyarrow issues"
    echo "   You can install it later with: pip install streamlit"
fi

echo ""
echo "🎉 Installation Summary"
echo "======================"

# Test installations
echo "🧪 Testing installations..."

if python -c "import fastapi; print('FastAPI: OK')" 2>/dev/null; then
    print_status "FastAPI is working"
else
    print_error "FastAPI installation failed"
fi

if python -c "import uvicorn; print('Uvicorn: OK')" 2>/dev/null; then
    print_status "Uvicorn is working"
else
    print_error "Uvicorn installation failed"
fi

if python -c "import sqlalchemy; print('SQLAlchemy: OK')" 2>/dev/null; then
    print_status "SQLAlchemy is working"
else
    print_error "SQLAlchemy installation failed"
fi

if python -c "import psycopg2; print('PostgreSQL driver: OK')" 2>/dev/null; then
    print_status "PostgreSQL driver is working"
else
    print_error "PostgreSQL driver installation failed"
fi

if python -c "import streamlit; print('Streamlit: OK')" 2>/dev/null; then
    print_status "Streamlit is working"
else
    print_warning "Streamlit is not available (this is OK for backend-only usage)"
fi

echo ""
echo "🚀 Next Steps:"
echo "1. Run the backend: uvicorn backend.main:app --host 0.0.0.0 --port 8000"
if [ "$PYARROW_SUCCESS" = true ]; then
    echo "2. Run the frontend: streamlit run frontend/app.py --server.port 8501"
else
    echo "2. Fix pyarrow issue to enable Streamlit frontend (see PYARROW_FIX.md)"
fi
echo "3. Set up PostgreSQL database"
echo ""
print_status "Installation complete!"