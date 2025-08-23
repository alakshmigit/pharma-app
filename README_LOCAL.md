# 🏠 Local Development - Quick Start

## 🚀 One-Command Setup

### For Linux/macOS:
```bash
# Clone and setup
git clone https://github.com/alakshmigit/pharma-app.git
cd pharma-app

# Install everything
./install.sh

# Setup database (after PostgreSQL is configured)
python setup_database.py

# Start application
./start_app.sh
```

### For Windows:
```batch
# Clone and setup
git clone https://github.com/alakshmigit/pharma-app.git
cd pharma-app

# Start application (installs dependencies automatically)
start_app.bat
```

## 📋 Prerequisites

### Required:
- **Python 3.8+** 
- **PostgreSQL 12+** (or compatible version)
- **Git**

### PostgreSQL Setup:
```sql
sudo -u postgres psql

CREATE DATABASE pharma_orders;
CREATE USER pharma_user WITH PASSWORD 'pharma_password_123';
GRANT ALL PRIVILEGES ON DATABASE pharma_orders TO pharma_user;
\q
```

## 🌐 Access Points

Once running:
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Manual Setup (if scripts don't work)

### 1. Create Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
pip install streamlit requests python-dotenv
```

### 3. Configure Environment:
Create `.env` file:
```env
DATABASE_URL=postgresql+psycopg2://pharma_user:pharma_password_123@localhost:5432/pharma_orders
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Setup Database:
```bash
python setup_database.py
```

### 5. Start Services:
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
streamlit run streamlit_app.py --server.port 8501
```

## 🎯 Features

### 🔐 Authentication System
- User registration and login
- JWT token-based authentication
- Secure password hashing
- Protected API endpoints

### 📊 Order Management
- Create and manage pharmaceutical orders
- Track order status (Open, In-Process, Closed)
- Automatic sub-order generation for ingredients
- Ingredient tracking (Carton, Label, RM, Sterios, Bottles, M.Cups, Caps, Shippers)

### 🎨 Modern UI
- Streamlit-based web interface
- Real-time data updates
- Responsive design
- User-friendly forms

### 🔗 RESTful API
- FastAPI backend with automatic documentation
- CRUD operations for all entities
- Input validation and error handling
- OpenAPI/Swagger documentation

## 📚 Documentation

- **LOCAL_SETUP.md** - Comprehensive local setup guide
- **DEPLOYMENT.md** - AWS deployment instructions
- **QUICKSTART.md** - Quick deployment guide

## 🆘 Troubleshooting

### Common Issues:

**PostgreSQL Connection Error:**
```bash
# Check PostgreSQL service
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS

# Test connection
psql -U pharma_user -d pharma_orders -h localhost
```

**Port Already in Use:**
```bash
# Find and kill process
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

**Dependencies Issues:**
```bash
# Reinstall in virtual environment
pip install --upgrade --force-reinstall -r requirements.txt
```

## 🔄 Development

### Project Structure:
```
pharma-app/
├── backend/           # FastAPI backend
│   ├── main.py       # Main application
│   ├── models.py     # Database models
│   ├── auth.py       # Authentication
│   └── requirements.txt
├── frontend/          # Streamlit frontend
│   ├── streamlit_app.py
│   └── requirements.txt
├── terraform/         # AWS infrastructure
├── install.sh        # Installation script
├── start_app.sh      # Startup script
└── setup_database.py # Database setup
```

### Making Changes:
- **Backend**: Edit files in `backend/`, auto-reloads with `--reload`
- **Frontend**: Edit `frontend/streamlit_app.py`, auto-reloads
- **Database**: Update `models.py` and run `python setup_database.py`

---

**Happy coding!** 🚀

For detailed instructions, see [LOCAL_SETUP.md](LOCAL_SETUP.md)