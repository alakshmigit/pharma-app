# 🗄️ Database Setup Guide

This guide provides multiple ways to initialize your PostgreSQL database for the Pharma Order Management System.

## 🚀 Quick Setup Options

### Option 1: Standalone Script (Recommended)
```bash
# From any directory, run:
python init_database.py
```

### Option 2: From Project Root
```bash
# Make sure you're in the project root directory
python run_init_db.py
```

### Option 3: Using Python Path
```bash
# Set PYTHONPATH and run
export PYTHONPATH=$PWD:$PYTHONPATH
python database/init_db.py
```

### Option 4: Direct Module Execution
```bash
# From project root
python -m database.init_db
```

## 📋 Prerequisites

1. **PostgreSQL Installation**:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # macOS
   brew install postgresql
   
   # Start PostgreSQL
   sudo systemctl start postgresql  # Linux
   brew services start postgresql   # macOS
   ```

2. **Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   ```bash
   # Copy and edit environment file
   cp .env.example .env
   # Edit .env with your database credentials
   ```

## ⚙️ Configuration

### Environment Variables (.env)
```env
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/pharma_db

# Individual parameters
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=pharma_db
```

### Docker Setup (Alternative)
```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Wait for startup (30 seconds)
sleep 30

# Initialize database
python init_database.py
```

## 🔧 Troubleshooting

### Import Errors
If you get `ModuleNotFoundError`, try:

1. **Check Current Directory**:
   ```bash
   pwd  # Should be in project root
   ls   # Should see backend/, config/, database/ folders
   ```

2. **Use Standalone Script**:
   ```bash
   python init_database.py  # Works from any directory
   ```

3. **Set Python Path**:
   ```bash
   export PYTHONPATH=$PWD:$PYTHONPATH
   python database/init_db.py
   ```

### Database Connection Errors

1. **Check PostgreSQL Status**:
   ```bash
   sudo systemctl status postgresql
   ```

2. **Test Connection**:
   ```bash
   psql -h localhost -U postgres -d postgres
   ```

3. **Create Database Manually**:
   ```bash
   sudo -u postgres createdb pharma_db
   ```

### Permission Errors
```bash
# Fix PostgreSQL permissions
sudo -u postgres psql
ALTER USER postgres PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE pharma_db TO postgres;
```

## 📊 What Gets Created

### Database Structure
- **Database**: `pharma_db`
- **Tables**: `orders`, `sub_orders`
- **Indexes**: Performance-optimized indexes on key columns
- **Relationships**: Foreign key constraints with CASCADE delete

### Sample Data
- **3 Sample Orders**: ABC Pharma, XYZ Healthcare, MediCorp
- **Auto-generated Sub-orders**: Based on ingredient requirements
- **Realistic Data**: Company names, products, molecules

### Verification
After successful initialization, you should see:
```
✅ Database 'pharma_db' created successfully
✅ All tables created successfully
✅ Sample orders created successfully
✅ Sample sub-orders created successfully
📊 Database initialized with 3 orders and X sub-orders
```

## 🧪 Testing the Setup

### 1. Database Connection Test
```bash
python -c "
from config.database import engine
print('Database URL:', engine.url)
conn = engine.connect()
result = conn.execute('SELECT COUNT(*) FROM orders')
print('Orders count:', result.scalar())
conn.close()
print('✅ Database connection successful!')
"
```

### 2. API Health Check
```bash
# Start backend first
python start_backend.py

# In another terminal, test health endpoint
curl http://localhost:8000/health
```

### 3. Frontend Test
```bash
# Start frontend
python start_frontend.py

# Access at: https://work-1-beejymubnnozffwt.prod-runtime.all-hands.dev
```

## 🔄 Resetting the Database

### Complete Reset
```bash
# Drop and recreate database
sudo -u postgres dropdb pharma_db
python init_database.py
```

### Clear Data Only
```bash
python -c "
from config.database import engine
engine.execute('TRUNCATE TABLE sub_orders, orders RESTART IDENTITY CASCADE')
print('✅ All data cleared')
"

# Re-add sample data
python init_database.py
```

## 📝 Next Steps

After successful database setup:

1. **Start Backend**:
   ```bash
   python start_backend.py
   ```

2. **Start Frontend**:
   ```bash
   python start_frontend.py
   ```

3. **Access Application**:
   - Frontend: https://work-1-beejymubnnozffwt.prod-runtime.all-hands.dev
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

4. **Optional - pgAdmin** (if using Docker):
   - URL: http://localhost:5050
   - Email: admin@pharma.com
   - Password: admin123

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify PostgreSQL is running
3. Check environment variables in `.env`
4. Try the standalone `init_database.py` script
5. Review the logs for specific error messages

For persistent issues, ensure:
- PostgreSQL is properly installed and running
- Python dependencies are installed
- Environment variables are correctly set
- You have proper database permissions