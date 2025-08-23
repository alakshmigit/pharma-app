@echo off
REM Dependency installation script with pyarrow fix for Windows
REM This script tries multiple approaches to install dependencies

echo 🔧 Installing Pharma App Dependencies
echo ==================================

REM Upgrade pip first
echo 📦 Upgrading pip...
pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)
echo ✅ Pip upgraded

REM Try to install pyarrow with pre-built wheel first
echo 🏗️  Attempting to install pyarrow with pre-built wheel...
pip install --only-binary=pyarrow pyarrow
if %errorlevel% equ 0 (
    echo ✅ PyArrow installed successfully with pre-built wheel
    set PYARROW_SUCCESS=true
) else (
    echo ⚠️  Pre-built wheel installation failed, trying alternative approach...
    set PYARROW_SUCCESS=false
)

REM Install core backend dependencies
echo 📦 Installing core backend dependencies...
pip install fastapi==0.104.1 uvicorn==0.24.0 sqlalchemy==2.0.23 pydantic==2.5.0 python-multipart==0.0.6 requests==2.31.0 python-dotenv==1.0.0 psycopg2-binary python-jose[cryptography] passlib[bcrypt]
if %errorlevel% neq 0 (
    echo ❌ Failed to install core dependencies
    pause
    exit /b 1
)
echo ✅ Core backend dependencies installed

REM Try to install pandas
echo 📊 Installing pandas...
pip install pandas==2.1.3
if %errorlevel% neq 0 (
    echo ⚠️  Pandas 2.1.3 failed, trying latest version...
    pip install pandas
    if %errorlevel% neq 0 (
        echo ❌ Failed to install pandas
        pause
        exit /b 1
    )
)
echo ✅ Pandas installed

REM Try to install streamlit if pyarrow worked
if "%PYARROW_SUCCESS%"=="true" (
    echo 🎨 Installing Streamlit...
    pip install streamlit==1.28.1
    if %errorlevel% neq 0 (
        echo ⚠️  Streamlit 1.28.1 failed, trying older version...
        pip install streamlit==1.25.0
        if %errorlevel% neq 0 (
            echo ❌ Failed to install Streamlit
        ) else (
            echo ✅ Streamlit installed (older version)
        )
    ) else (
        echo ✅ Streamlit installed successfully
    )
) else (
    echo ⚠️  Skipping Streamlit installation due to pyarrow issues
    echo    You can install it later with: pip install streamlit
)

echo.
echo 🎉 Installation Summary
echo ======================

REM Test installations
echo 🧪 Testing installations...

python -c "import fastapi; print('FastAPI: OK')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ FastAPI is working
) else (
    echo ❌ FastAPI installation failed
)

python -c "import uvicorn; print('Uvicorn: OK')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Uvicorn is working
) else (
    echo ❌ Uvicorn installation failed
)

python -c "import sqlalchemy; print('SQLAlchemy: OK')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ SQLAlchemy is working
) else (
    echo ❌ SQLAlchemy installation failed
)

python -c "import psycopg2; print('PostgreSQL driver: OK')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL driver is working
) else (
    echo ❌ PostgreSQL driver installation failed
)

python -c "import streamlit; print('Streamlit: OK')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Streamlit is working
) else (
    echo ⚠️  Streamlit is not available (this is OK for backend-only usage)
)

echo.
echo 🚀 Next Steps:
echo 1. Run the backend: uvicorn backend.main:app --host 0.0.0.0 --port 8000
if "%PYARROW_SUCCESS%"=="true" (
    echo 2. Run the frontend: streamlit run frontend/app.py --server.port 8501
) else (
    echo 2. Fix pyarrow issue to enable Streamlit frontend (see PYARROW_FIX.md)
)
echo 3. Set up PostgreSQL database
echo.
echo ✅ Installation complete!
pause