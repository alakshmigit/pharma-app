# 📦 Order Management System

A comprehensive order management system built with **Python FastAPI backend**, **Streamlit frontend**, and **SQLite database** for managing pharmaceutical orders and their sub-orders.

## 🚀 Features

### Core Functionality
- **📋 Order Management**: Create, view, update, and track orders
- **🔄 Intelligent Sub-Order Management**: Automatic sub-order creation/removal based on ingredient requirements
- **📊 Real-time Dashboard**: Statistics and analytics with interactive charts
- **🔍 Advanced Filtering**: Filter orders by status, company, and other criteria
- **📈 Status Tracking**: Track order progress through Open → In-Process → Closed

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
- **Database**: SQLite with relational schema
- **API**: RESTful endpoints with Pydantic validation
- **Charts**: Plotly for interactive visualizations

## 📁 Project Structure

```
order-management-system/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── crud.py          # Database operations
├── frontend/
│   └── streamlit_app.py # Streamlit application
├── config/
│   └── database.py      # Database configuration
├── database/
│   └── init_db.py       # Database initialization
├── start_backend.py     # Backend startup script
├── start_frontend.py    # Frontend startup script
├── requirements.txt     # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd order-management-system
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Initialize the database**:
```bash
python database/init_db.py
```

### Running the Application

#### Option 1: Using startup scripts (Recommended)
```bash
# Start backend (Terminal 1)
python start_backend.py

# Start frontend (Terminal 2)
python start_frontend.py
```

#### Option 2: Manual startup
```bash
# Start backend
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start frontend
streamlit run frontend/streamlit_app.py --server.port 8501
```

### Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 Database Schema

### Orders Table
- `order_id` (Primary Key)
- `company_name`, `product_name`, `molecule`
- `status` (Open/In-Process/Closed)
- `quantity`, `pack`
- Ingredient flags: `carton`, `label`, `rm`, `sterios`, `bottles`, `m_cups`, `caps`, `shippers`

### Sub-Orders Table
- `sub_order_id` (Primary Key)
- `order_id` (Foreign Key)
- `ingredient_type`, `quantity`, `pack`, `status`

## 🔧 API Endpoints

### Orders
- `GET /orders/` - List all orders
- `POST /orders/` - Create new order
- `GET /orders/{order_id}` - Get order details
- `PUT /orders/{order_id}` - Update order
- `DELETE /orders/{order_id}` - Delete order

### Sub-Orders
- `GET /sub-orders/` - List all sub-orders
- `PUT /sub-orders/{sub_order_id}` - Update sub-order status

### Dashboard
- `GET /dashboard/stats` - Get dashboard statistics

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

### Order Status Flow
```
Open → In-Process → Closed
```

## 🧪 Testing

The system includes comprehensive testing capabilities:

```bash
# Test API endpoints
python test_api.py

# Manual testing through frontend
# 1. Create sample orders
# 2. Verify sub-order creation
# 3. Test order updates
# 4. Check dashboard statistics
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the database schema
3. Test with sample data using the provided scripts

---

**Built with ❤️ using FastAPI and Streamlit**