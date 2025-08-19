# 🏠 Local Development Setup Guide

## 📋 Prerequisites

### System Requirements
- **Python 3.8+** (recommended: Python 3.9 or 3.10)
- **MySQL 8.0+** (or MariaDB 10.3+)
- **Git** for version control
- **pip** (Python package manager)

### Operating System Support
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Ubuntu 18.04+
- ✅ Other Linux distributions

## 🛠️ Installation Steps

### Step 1: Install MySQL Database

#### On Windows:
1. Download MySQL from: https://dev.mysql.com/downloads/mysql/
2. Run the installer and follow the setup wizard
3. Set root password (remember this!)
4. Start MySQL service

#### On macOS:
```bash
# Using Homebrew (recommended)
brew install mysql
brew services start mysql

# Set root password
mysql_secure_installation
```

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure installation
sudo mysql_secure_installation
```

#### On CentOS/RHEL:
```bash
sudo yum install mysql-server
# or for newer versions:
sudo dnf install mysql-server

sudo systemctl start mysqld
sudo systemctl enable mysqld

# Get temporary root password
sudo grep 'temporary password' /var/log/mysqld.log
mysql_secure_installation
```

### Step 2: Create Database and User

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE pharma_orders;

-- Create user for the application
CREATE USER 'pharma_user'@'localhost' IDENTIFIED BY 'pharma_password_123';

-- Grant privileges
GRANT ALL PRIVILEGES ON pharma_orders.* TO 'pharma_user'@'localhost';
FLUSH PRIVILEGES;

-- Verify database creation
SHOW DATABASES;
USE pharma_orders;

-- Exit MySQL
EXIT;
```

### Step 3: Clone and Setup Application

```bash
# Clone the repository
git clone https://github.com/alakshmigit/pharma-app.git
cd pharma-app

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 4: Install Python Dependencies

```bash
# Install backend dependencies
cd backend
pip install fastapi uvicorn sqlalchemy pymysql python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv

# Install frontend dependencies
cd ../frontend
pip install streamlit requests python-dotenv

# Return to root directory
cd ..
```

### Step 5: Configure Environment Variables

Create `.env` file in the root directory:

```bash
# Create .env file
touch .env  # On Windows: type nul > .env
```

Add the following content to `.env`:

```env
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
```

### Step 6: Initialize Database Tables

Create a database initialization script:

```bash
# Create database setup script
cat > setup_database.py << 'EOF'
import sys
import os
sys.path.append('backend')

from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in environment variables")
    sys.exit(1)

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")
    print("📋 Tables created:")
    print("   - users")
    print("   - orders") 
    print("   - sub_orders")
    
except Exception as e:
    print(f"❌ Error creating database tables: {e}")
    sys.exit(1)
EOF

# Run database setup
python setup_database.py
```

## 🚀 Running the Application

### Method 1: Using Separate Terminals (Recommended)

#### Terminal 1 - Backend API:
```bash
cd pharma-app
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 - Frontend UI:
```bash
cd pharma-app
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd frontend
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Method 2: Using Startup Script

Create a startup script:

```bash
# Create startup script
cat > start_app.sh << 'EOF'
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Pharma Order Management Application${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found. Please run setup first.${NC}"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found. Please create it first.${NC}"
    exit 1
fi

# Start backend in background
echo -e "${YELLOW}📡 Starting Backend API...${NC}"
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo -e "${YELLOW}🎨 Starting Frontend UI...${NC}"
cd frontend
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✅ Application started successfully!${NC}"
echo -e "${BLUE}📱 Frontend: http://localhost:8501${NC}"
echo -e "${BLUE}🔗 Backend API: http://localhost:8000${NC}"
echo -e "${BLUE}📚 API Docs: http://localhost:8000/docs${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down application...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Application stopped.${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for processes
wait
EOF

# Make script executable
chmod +x start_app.sh

# Run the application
./start_app.sh
```

### Method 3: Windows Batch Script

Create `start_app.bat` for Windows:

```batch
@echo off
echo 🚀 Starting Pharma Order Management Application

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found. Please create it first.
    pause
    exit /b 1
)

REM Start backend
echo 📡 Starting Backend API...
start "Backend API" cmd /k "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start frontend
echo 🎨 Starting Frontend UI...
start "Frontend UI" cmd /k "cd frontend && streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"

echo ✅ Application started successfully!
echo 📱 Frontend: http://localhost:8501
echo 🔗 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs

pause
```

## 🌐 Accessing the Application

Once both services are running:

### 🎨 Frontend (Streamlit UI)
- **URL**: http://localhost:8501
- **Features**: 
  - User registration and login
  - Order management interface
  - Real-time data updates

### 🔗 Backend API
- **URL**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

### 🔐 First Time Setup
1. **Register a new user** at http://localhost:8501
2. **Login** with your credentials
3. **Start creating orders** and managing data

## 🧪 Testing the Installation

### Comprehensive Test Script:
```bash
# Run all tests automatically
python test_local_setup.py
```

This script tests:
- ✅ Python package imports
- ✅ Environment configuration
- ✅ Database connectivity
- ✅ Database tables existence
- ✅ Backend API health
- ✅ Frontend accessibility
- ✅ API endpoint security

### Manual Tests:

#### Test Database Connection:
```bash
python -c "
import sys
sys.path.append('backend')
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))
connection = engine.connect()
print('✅ Database connection successful!')
connection.close()
"
```

#### Test Backend API:
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

#### Test Frontend:
Open http://localhost:8501 in your browser

## 🔧 Troubleshooting

### Common Issues:

#### 1. MySQL Connection Error
```bash
# Check MySQL service status
# On Linux/macOS:
sudo systemctl status mysql
# On Windows: Check Services.msc

# Test MySQL connection
mysql -u pharma_user -p pharma_orders
```

#### 2. Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # On macOS/Linux
netstat -ano | findstr :8000  # On Windows

# Kill the process
kill -9 <PID>  # On macOS/Linux
taskkill /PID <PID> /F  # On Windows
```

#### 3. Python Dependencies Issues
```bash
# Reinstall dependencies
pip install --upgrade --force-reinstall -r requirements.txt
```

#### 4. Virtual Environment Issues
```bash
# Remove and recreate virtual environment
rm -rf venv  # On Windows: rmdir /s venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
# Reinstall dependencies
```

### Environment Variables Issues:
```bash
# Check if .env file is loaded
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('DATABASE_URL:', os.getenv('DATABASE_URL'))
print('SECRET_KEY:', os.getenv('SECRET_KEY'))
"
```

## 📊 Database Management

### View Tables:
```sql
mysql -u pharma_user -p pharma_orders

SHOW TABLES;
DESCRIBE users;
DESCRIBE orders;
DESCRIBE sub_orders;
```

### Sample Data:
```sql
-- View users
SELECT id, username, email, created_at FROM users;

-- View orders
SELECT id, company_name, product_name, status, created_at FROM orders LIMIT 10;

-- View sub-orders
SELECT so.id, o.company_name, so.ingredient_type, so.quantity 
FROM sub_orders so 
JOIN orders o ON so.order_id = o.id 
LIMIT 10;
```

### Backup Database:
```bash
mysqldump -u pharma_user -p pharma_orders > pharma_backup.sql
```

### Restore Database:
```bash
mysql -u pharma_user -p pharma_orders < pharma_backup.sql
```

## 🔄 Development Workflow

### Making Changes:
1. **Backend changes**: Edit files in `backend/` directory
2. **Frontend changes**: Edit files in `frontend/` directory
3. **Database changes**: Update `models.py` and run migrations

### Hot Reload:
- **Backend**: Automatically reloads with `--reload` flag
- **Frontend**: Streamlit auto-reloads on file changes

### Adding New Dependencies:
```bash
# Backend
cd backend
pip install new-package
pip freeze > requirements.txt

# Frontend  
cd frontend
pip install new-package
pip freeze > requirements.txt
```

## 📝 Configuration Options

### Database Configuration:
- **Host**: localhost (default)
- **Port**: 3306 (default)
- **Database**: pharma_orders
- **User**: pharma_user
- **Password**: pharma_password_123

### Application Ports:
- **Backend**: 8000 (configurable)
- **Frontend**: 8501 (configurable)

### JWT Settings:
- **Secret Key**: Change in production
- **Algorithm**: HS256
- **Token Expiry**: 30 minutes (configurable)

---

## 🎉 You're Ready!

Your pharmaceutical order management application is now running locally with:
- ✅ **MySQL database** for data persistence
- ✅ **FastAPI backend** with JWT authentication
- ✅ **Streamlit frontend** with modern UI
- ✅ **Complete CRUD operations** for orders and sub-orders
- ✅ **User management** with secure authentication

**Happy coding!** 🚀