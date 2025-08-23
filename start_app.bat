@echo off
title Pharma Order Management System

echo 🚀 Starting Pharma Order Management Application
echo ================================================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found.
    echo 💡 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found.
    echo 💡 Creating sample .env file...
    (
        echo # Database Configuration
        echo DATABASE_URL=postgresql+psycopg2://pharma_user:pharma_password_123@localhost:5432/pharma_orders
        echo.
        echo # JWT Configuration
        echo SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=30
        echo.
        echo # Application Configuration
        echo BACKEND_URL=http://localhost:8000
        echo FRONTEND_URL=http://localhost:8501
        echo.
        echo # Development Settings
        echo DEBUG=True
        echo ENVIRONMENT=development
    ) > .env
    echo ✅ Sample .env file created. Please update with your settings.
)

REM Install dependencies
if exist "backend\requirements.txt" (
    echo 📦 Installing backend dependencies...
    pip install -r backend\requirements.txt
)

if exist "frontend\requirements.txt" (
    echo 📦 Installing frontend dependencies...
    pip install -r frontend\requirements.txt
)

REM Setup database
echo 🏗️ Setting up database...
python setup_database.py
if errorlevel 1 (
    echo ❌ Database setup failed. Please check your PostgreSQL configuration.
    pause
    exit /b 1
)

REM Start backend
echo 📡 Starting Backend API...
start "Backend API" cmd /k "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait for backend to start
echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend
echo 🎨 Starting Frontend UI...
start "Frontend UI" cmd /k "cd frontend && streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"

REM Wait for frontend to start
echo ⏳ Waiting for frontend to start...
timeout /t 3 /nobreak >nul

echo.
echo ✅ Application started successfully!
echo ================================================
echo 📱 Frontend UI:      http://localhost:8501
echo 🔗 Backend API:      http://localhost:8000
echo 📚 API Docs:         http://localhost:8000/docs
echo 📖 Alternative Docs: http://localhost:8000/redoc
echo ================================================
echo 💡 Close the terminal windows to stop the application

pause