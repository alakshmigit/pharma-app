# 🏥 Pharma Order Management System

A comprehensive pharmaceutical order management system built with **FastAPI backend**, **Streamlit frontend**, and **PostgreSQL database** for managing pharmaceutical orders and their sub-orders.

## 🚀 Features

### Core Functionality
- **📋 Order Management**: Create, view, update, and track pharmaceutical orders
- **🔄 Intelligent Sub-Order Management**: Automatic sub-order creation/removal based on ingredient requirements
- **📊 Real-time Dashboard**: Statistics and analytics with interactive charts
- **🔍 Advanced Filtering**: Filter orders by status, company, and other criteria
- **📈 Status Tracking**: Track order progress through Open → In-Process → Closed
- **🏥 Production-Ready**: PostgreSQL database with proper indexing and relationships

### Ingredient Management
- **8 Ingredient Types**: Carton, Label, RM, Sterios, Bottles, M.Cups, Caps, Shippers
- **Smart Sub-Order Logic**: 
  - `Y` = Creates sub-order with same quantity and pack
  - `N` = No sub-order required
  - `N/A` = Ingredient not applicable
- **Dynamic Updates**: Changing ingredient from N→Y creates sub-order, Y→N/N/A removes it

### User Interface
- **Multi-page Navigation**: Dashboard, Create Order, View Orders, Update Order, Sub-Orders
- **Expandable Order Cards**: Hierarchical view of orders and their sub-orders
- **Interactive Tables**: Sortable and filterable data displays
- **Real-time Updates**: Live data synchronization between frontend and backend

## 🛠️ Technology Stack

- **Backend**: FastAPI with SQLAlchemy ORM
- **Frontend**: Streamlit with interactive components
- **Database**: PostgreSQL 15+ with proper indexing
- **API**: RESTful endpoints with Pydantic validation
- **Charts**: Plotly for interactive visualizations
- **Deployment**: Docker support included

## 📁 Project Structure

```
pharma-app/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI application with health checks
│   ├── models.py        # SQLAlchemy models with PostgreSQL optimizations
│   ├── schemas.py       # Pydantic schemas
│   └── crud.py          # Database operations
├── frontend/
│   └── streamlit_app.py # Streamlit application
├── config/
│   └── database.py      # PostgreSQL configuration
├── database/
│   └── init_db.py       # PostgreSQL database initialization
├── docker-compose.yml   # PostgreSQL and pgAdmin setup
├── setup_postgres.py    # Automated PostgreSQL setup script
├── .env.example         # Environment variables template
├── start_backend.py     # Backend startup script
├── start_frontend.py    # Frontend startup script
├── requirements.txt     # Python dependencies (includes psycopg2)
└── README.md
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/alakshmigit/pharma-app.git
cd pharma-app

# Run the automated setup script
python setup_postgres.py
```

### Option 2: Docker Setup (Easiest)

```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Wait for PostgreSQL to be ready (about 30 seconds)
sleep 30

# Install Python dependencies
pip install -r requirements.txt

# Initialize database
python database/init_db.py

# Start the application
python start_backend.py  # Terminal 1
python start_frontend.py # Terminal 2
```

### Option 3: Manual Setup

#### Prerequisites
- Python 3.8+
- PostgreSQL 15+
- pip

#### Installation Steps

1. **Install PostgreSQL** (Ubuntu/Debian):
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

2. **Create Database and User**:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE pharma_db;
   CREATE USER pharma_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE pharma_db TO pharma_user;
   \q
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Initialize Database**:
   ```bash
   python database/init_db.py
   ```

6. **Start the Application**:
   ```bash
   # Terminal 1: Start backend
   python start_backend.py
   
   # Terminal 2: Start frontend
   python start_frontend.py
   ```

### Access the Application
- **Frontend**: https://work-1-beejymubnnozffwt.prod-runtime.all-hands.dev (port 12000)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **pgAdmin** (if using Docker): http://localhost:5050

## ⚙️ Configuration

### Environment Variables (.env)

```env
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/pharma_db

# Individual database connection parameters
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=pharma_db

# Application Configuration
DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=12000
```

### Docker Configuration

The included `docker-compose.yml` provides:
- **PostgreSQL 15**: Main database server
- **pgAdmin 4**: Web-based database administration
- **Persistent Storage**: Data survives container restarts
- **Health Checks**: Automatic service monitoring

## 📊 Database Schema

### Orders Table
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    molecule VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Open',
    quantity INTEGER NOT NULL,
    pack VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    -- Ingredients
    carton VARCHAR(10) NOT NULL DEFAULT 'N/A',
    label VARCHAR(10) NOT NULL DEFAULT 'N/A',
    rm VARCHAR(10) NOT NULL DEFAULT 'N/A',
    sterios VARCHAR(10) NOT NULL DEFAULT 'N/A',
    bottles VARCHAR(10) NOT NULL DEFAULT 'N/A',
    m_cups VARCHAR(10) NOT NULL DEFAULT 'N/A',
    caps VARCHAR(10) NOT NULL DEFAULT 'N/A',
    shippers VARCHAR(10) NOT NULL DEFAULT 'N/A'
);

-- Indexes for performance
CREATE INDEX idx_orders_company ON orders(company_name);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_product ON orders(product_name);
```

### Sub-Orders Table
```sql
CREATE TABLE sub_orders (
    sub_order_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
    ingredient_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Open',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    sub_order_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    vendor_company VARCHAR(255),
    product_name VARCHAR(255),
    main_order_date TIMESTAMP WITH TIME ZONE,
    designer_name VARCHAR(255),
    sizes VARCHAR(255),
    approved_by_first_name VARCHAR(100),
    approved_by_last_name VARCHAR(100),
    approved_date TIMESTAMP WITH TIME ZONE,
    remarks TEXT
);

-- Indexes for performance
CREATE INDEX idx_sub_orders_order_id ON sub_orders(order_id);
CREATE INDEX idx_sub_orders_ingredient ON sub_orders(ingredient_type);
CREATE INDEX idx_sub_orders_status ON sub_orders(status);
```

## 🔧 API Endpoints

### Health Check
- `GET /health` - Database connectivity and system health check

### Orders
- `GET /orders/` - List all orders with pagination
- `POST /orders/` - Create new order (auto-generates sub-orders)
- `GET /orders/{order_id}` - Get order details with sub-orders
- `PUT /orders/{order_id}` - Update order (manages sub-orders automatically)
- `DELETE /orders/{order_id}` - Delete order (cascades to sub-orders)

### Sub-Orders
- `GET /sub-orders/` - List all sub-orders
- `GET /sub-orders/order/{order_id}` - Get sub-orders for specific order
- `PUT /sub-orders/{sub_order_id}` - Update sub-order details

### Dashboard
- `GET /dashboard/stats` - Get comprehensive dashboard statistics

## 💡 Usage Examples

### Creating an Order
1. Navigate to "Create Order" page
2. Fill in company details, product information
3. Set ingredient requirements (Y/N/N/A)
4. Submit - sub-orders are automatically created for 'Y' ingredients

### Updating Orders
1. Go to "Update Order" page
2. Select order to modify
3. Change ingredient values (N→Y creates sub-order, Y→N removes it)
4. Submit changes

### Viewing Orders & Sub-Orders
1. Visit "View Orders & Sub-Orders" page
2. Use filters to narrow down results
3. Expand order cards to see detailed information and sub-orders
4. View hierarchical relationship between orders and sub-orders

## 🔄 Business Logic

### Sub-Order Management
- **Creation**: When ingredient changes from N/N/A to Y
- **Removal**: When ingredient changes from Y to N/N/A
- **Inheritance**: Sub-orders inherit quantity and pack from parent order
- **Status**: Sub-orders start with "Open" status
- **Cascade Delete**: Deleting an order removes all its sub-orders

### Order Status Flow
```
Open → In-Process → Closed
```

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### API Testing
```bash
# Test order creation
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Pharma",
    "product_name": "Test Medicine",
    "molecule": "Test Molecule",
    "quantity": 100,
    "pack": "Bottle",
    "carton": "Y",
    "label": "N"
  }'
```

### Database Testing
```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d pharma_db

# Check tables
\dt

# View orders
SELECT * FROM orders;
```

## 🚀 Production Deployment

### AWS RDS PostgreSQL
1. Create RDS PostgreSQL instance
2. Update `DATABASE_URL` in environment variables
3. Run database initialization:
   ```bash
   python database/init_db.py
   ```
4. Deploy application using your preferred method

### Environment-Specific Configuration
- **Development**: Use local PostgreSQL or Docker
- **Staging**: Use managed PostgreSQL service
- **Production**: Use AWS RDS, Google Cloud SQL, or Azure Database

## 🔍 Troubleshooting

### Database Connection Issues
1. **Check PostgreSQL Status**:
   ```bash
   sudo systemctl status postgresql
   ```

2. **Test Connection**:
   ```bash
   psql -h localhost -U postgres -d pharma_db
   ```

3. **Check Logs**:
   ```bash
   sudo journalctl -u postgresql
   ```

### Application Issues
1. **Check Health Endpoint**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **View Application Logs**:
   ```bash
   tail -f backend.log
   tail -f frontend.log
   ```

3. **Database Connection Test**:
   ```python
   python -c "from config.database import engine; print(engine.execute('SELECT 1').scalar())"
   ```

## 🔧 Development

### Adding New Features
1. Update database models in `backend/models.py`
2. Create/update schemas in `backend/schemas.py`
3. Implement CRUD operations in `backend/crud.py`
4. Add API endpoints in `backend/main.py`
5. Update frontend in `frontend/streamlit_app.py`

### Database Migrations
When updating models:
1. Create migration scripts
2. Test on development database
3. Apply to production with proper backup

### Performance Optimization
- Use database indexes for frequently queried columns
- Implement connection pooling
- Add caching for dashboard statistics
- Use database views for complex queries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the database schema
3. Test with sample data using the provided scripts
4. Use the health check endpoint for diagnostics

---

**Built with ❤️ using FastAPI, Streamlit, and PostgreSQL**