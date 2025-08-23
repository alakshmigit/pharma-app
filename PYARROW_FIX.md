# PyArrow Installation Fix

## Problem
`ERROR: Failed building wheel for pyarrow` - This is a common issue when installing Streamlit dependencies.

## Solutions (Try in order)

### Solution 1: Use Pre-built Wheel (Recommended)
```bash
# Upgrade pip first
pip install --upgrade pip

# Install pyarrow with pre-built wheel
pip install --only-binary=pyarrow pyarrow

# Then install other requirements
pip install -r requirements.txt
```

### Solution 2: Install System Dependencies (Linux/Ubuntu)
```bash
# Install build dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake

# Install Arrow C++ libraries
sudo apt-get install -y libarrow-dev

# Then try installing again
pip install pyarrow
```

### Solution 3: Install System Dependencies (macOS)
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install cmake
brew install apache-arrow

# Then try installing again
pip install pyarrow
```

### Solution 4: Use Conda (Alternative Package Manager)
```bash
# Install conda/miniconda if not available
# Then use conda instead of pip for pyarrow
conda install -c conda-forge pyarrow

# Install other requirements with pip
pip install fastapi uvicorn sqlalchemy pydantic python-multipart requests pandas python-dotenv psycopg2-binary python-jose[cryptography] passlib[bcrypt]
```

### Solution 5: Minimal Installation (Skip Streamlit temporarily)
If you just want to run the backend API without the Streamlit frontend:

```bash
# Install only backend dependencies
pip install fastapi==0.104.1 uvicorn==0.24.0 sqlalchemy==2.0.23 pydantic==2.5.0 python-multipart==0.0.6 requests==2.31.0 pandas==2.1.3 python-dotenv==1.0.0 psycopg2-binary python-jose[cryptography] passlib[bcrypt]

# Skip streamlit for now - you can add it later
```

### Solution 6: Use Different Streamlit Version
```bash
# Try an older version of streamlit that might not require the problematic pyarrow version
pip install streamlit==1.25.0
```

## Quick Test
After fixing pyarrow, test the installation:

```bash
python -c "import pyarrow; print('PyArrow installed successfully')"
python -c "import streamlit; print('Streamlit installed successfully')"
```

## Alternative: Docker Installation
If all else fails, you can use Docker to avoid dependency issues:

```bash
# Build and run with Docker
docker build -t pharma-app .
docker run -p 8000:8000 -p 8501:8501 pharma-app
```

## Recommended Approach
1. Try Solution 1 first (pre-built wheel)
2. If that fails, try Solution 5 (minimal installation) to get the backend running
3. Add Streamlit later once pyarrow is resolved