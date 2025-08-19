#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Pharma Order Management Application${NC}"
echo -e "${PURPLE}================================================${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found.${NC}"
    echo -e "${YELLOW}💡 Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found.${NC}"
    echo -e "${YELLOW}💡 Creating sample .env file...${NC}"
    cat > .env << 'EOF'
# Database Configuration
DATABASE_URL=mysql+pymysql://pharma_user:pharma_password_123@localhost:3306/pharma_orders

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
    echo -e "${GREEN}✅ Sample .env file created. Please update with your settings.${NC}"
fi

# Install dependencies if requirements.txt exists
if [ -f "backend/requirements.txt" ]; then
    echo -e "${YELLOW}📦 Installing backend dependencies...${NC}"
    pip install -r backend/requirements.txt
fi

if [ -f "frontend/requirements.txt" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    pip install -r frontend/requirements.txt
fi

# Setup database
echo -e "${YELLOW}🏗️  Setting up database...${NC}"
python setup_database.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Database setup failed. Please check your MySQL configuration.${NC}"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down application...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo -e "${GREEN}✅ Application stopped.${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Start backend in background
echo -e "${YELLOW}📡 Starting Backend API...${NC}"
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo -e "${YELLOW}⏳ Waiting for backend to start...${NC}"
sleep 5

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${RED}❌ Backend failed to start${NC}"
    cleanup
fi

# Start frontend
echo -e "${YELLOW}🎨 Starting Frontend UI...${NC}"
cd frontend
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo -e "${YELLOW}⏳ Waiting for frontend to start...${NC}"
sleep 3

echo -e "\n${GREEN}✅ Application started successfully!${NC}"
echo -e "${PURPLE}================================================${NC}"
echo -e "${BLUE}📱 Frontend UI:     ${NC}http://localhost:8501"
echo -e "${BLUE}🔗 Backend API:     ${NC}http://localhost:8000"
echo -e "${BLUE}📚 API Docs:        ${NC}http://localhost:8000/docs"
echo -e "${BLUE}📖 Alternative Docs:${NC}http://localhost:8000/redoc"
echo -e "${PURPLE}================================================${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop the application${NC}"

# Wait for processes
wait