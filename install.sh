#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}🏗️  Pharma Order Management System - Installation Script${NC}"
echo -e "${PURPLE}=========================================================${NC}"

# Check Python version
echo -e "${YELLOW}🐍 Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
if [ -z "$python_version" ]; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

major_version=$(echo $python_version | cut -d. -f1)
minor_version=$(echo $python_version | cut -d. -f2)

if [ "$major_version" -lt 3 ] || ([ "$major_version" -eq 3 ] && [ "$minor_version" -lt 8 ]); then
    echo -e "${RED}❌ Python $python_version found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $python_version found${NC}"

# Check if PostgreSQL is installed
echo -e "${YELLOW}🗄️  Checking PostgreSQL installation...${NC}"
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✅ PostgreSQL found${NC}"
else
    echo -e "${YELLOW}⚠️  PostgreSQL not found. Please install PostgreSQL 12 or higher.${NC}"
    echo -e "${BLUE}💡 Installation instructions:${NC}"
    echo -e "   Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    echo -e "   CentOS/RHEL:   sudo yum install postgresql-server postgresql-contrib"
    echo -e "   macOS:         brew install postgresql"
    echo -e "   Windows:       Download from https://www.postgresql.org/download/windows/"
fi

# Create virtual environment
echo -e "${YELLOW}🔧 Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists. Removing...${NC}"
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment created${NC}"

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}📦 Upgrading pip...${NC}"
pip install --upgrade pip

# Install backend dependencies
echo -e "${YELLOW}📦 Installing backend dependencies...${NC}"
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
else
    echo -e "${YELLOW}💡 Installing backend dependencies manually...${NC}"
    pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv
fi

# Install frontend dependencies
echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
if [ -f "frontend/requirements.txt" ]; then
    pip install -r frontend/requirements.txt
else
    echo -e "${YELLOW}💡 Installing frontend dependencies manually...${NC}"
    pip install streamlit requests python-dotenv
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚙️  Creating .env configuration file...${NC}"
    cat > .env << 'EOF'
# Database Configuration
DATABASE_URL=postgresql+psycopg2://pharma_user:pharma_password_123@localhost:5432/pharma_orders

# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8501

# Development Settings
DEBUG=True
ENVIRONMENT=development
EOF
    echo -e "${GREEN}✅ .env file created${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo -e "\n${GREEN}🎉 Installation completed successfully!${NC}"
echo -e "${PURPLE}=========================================================${NC}"
echo -e "${BLUE}📋 Next Steps:${NC}"
echo -e "${YELLOW}1. Setup PostgreSQL database:${NC}"
echo -e "   sudo -u postgres psql"
echo -e "   CREATE DATABASE pharma_orders;"
echo -e "   CREATE USER pharma_user WITH PASSWORD 'pharma_password_123';"
echo -e "   GRANT ALL PRIVILEGES ON DATABASE pharma_orders TO pharma_user;"
echo -e "   \\q"
echo -e ""
echo -e "${YELLOW}2. Initialize database tables:${NC}"
echo -e "   python setup_database.py"
echo -e ""
echo -e "${YELLOW}3. Start the application:${NC}"
echo -e "   ./start_app.sh"
echo -e ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo -e "   - Local Setup Guide: LOCAL_SETUP.md"
echo -e "   - AWS Deployment: DEPLOYMENT.md"
echo -e "   - Quick Start: QUICKSTART.md"
echo -e "${PURPLE}=========================================================${NC}"