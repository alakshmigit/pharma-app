# Pharma-App: Pharmaceutical Order Management System

A comprehensive pharmaceutical order management system built with Python backend (FastAPI), Streamlit frontend, and SQLite database for managing pharmaceutical manufacturing orders and sub-orders.

## 🚀 Features

### 📦 Main Orders Management
- **Order Creation**: Create orders with comprehensive pharmaceutical details
- **Company Tracking**: Manage pharmaceutical company information
- **Product Management**: Track product names and molecular information
- **Status Workflow**: Monitor order status (In-Process, Closed, Open)
- **Quantity & Packaging**: Manage order quantities and packaging specifications

### 🧪 Ingredients & Sub-Orders System
The system supports 8 pharmaceutical ingredient types with intelligent sub-order generation:

| Ingredient | Description | Sub-Order Generation |
|------------|-------------|---------------------|
| **Carton** | Packaging containers | Y/N/N/A configurable |
| **Label** | Product labeling | Y/N/N/A configurable |
| **RM** | Raw Materials | Y/N/N/A configurable |
| **Sterios** | Sterile components | Y/N/N/A configurable |
| **Bottles** | Container bottles | Y/N/N/A configurable |
| **M.Cups** | Measuring cups | Y/N/N/A configurable |
| **Caps** | Bottle caps | Y/N/N/A configurable |
| **Shippers** | Shipping containers | Y/N/N/A configurable |

**Sub-Order Configuration:**
- **Y**: Automatically generates sub-order with comprehensive tracking
- **N**: No sub-order required for this ingredient
- **N/A**: Ingredient not applicable for this order

### 📋 Comprehensive Sub-Order Management
Each sub-order includes 10+ detailed fields:
- **Basic Info**: Sub-Order ID, Ingredient Type, Status
- **Dates**: Sub-Order Date, Main Order Date, Approved Date
- **Vendor Management**: Vendor Company details
- **Product Details**: Product Name, Designer Name, Sizes
- **Approval Workflow**: Approved By (First & Last Name)
- **Documentation**: Remarks and notes
- **Inheritance**: Quantity & Pack from main order

## 🛠 Technology Stack

- **Backend**: FastAPI (Python) - High-performance async API
- **Frontend**: Streamlit - Interactive web interface
- **Database**: SQLite with SQLAlchemy ORM
- **API Documentation**: Automatic OpenAPI/Swagger
- **Data Validation**: Pydantic schemas
- **Date Handling**: Full datetime support

## 📁 Project Structure

```
pharma-app/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI application & API endpoints
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic validation schemas
│   ├── crud.py          # Database CRUD operations
│   └── database.py      # Database configuration
├── frontend/
│   └── streamlit_app.py # Streamlit web interface
├── config/
│   └── settings.py      # Application configuration
├── database/
│   └── init.sql         # Database initialization scripts
├── requirements.txt     # Python dependencies
├── start_backend.py     # Backend startup script
├── start_frontend.py    # Frontend startup script
├── test_api.py          # API testing script
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pharma-app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   The SQLite database will be automatically created on first run.

### Running the Application

#### Option 1: Using Startup Scripts (Recommended)

1. **Start the Backend API**:
   ```bash
   python start_backend.py
   ```
   🌐 Backend available at: `http://localhost:8000`

2. **Start the Frontend** (new terminal):
   ```bash
   python start_frontend.py
   ```
   🌐 Frontend available at: `http://localhost:8501`

#### Option 2: Manual Startup

1. **Backend**:
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Frontend**:
   ```bash
   streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
   ```

## 📚 API Documentation

Access comprehensive API documentation:
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

### Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/orders/` | List all orders |
| `POST` | `/orders/` | Create new order |
| `GET` | `/orders/{order_id}` | Get specific order |
| `GET` | `/sub-orders/` | List all sub-orders |
| `GET` | `/sub-orders/{sub_order_id}` | Get specific sub-order |
| `PUT` | `/sub-orders/{sub_order_id}` | Update sub-order details |

## 💻 User Interface Guide

### 🏠 Dashboard
- Overview of system status
- Quick navigation to all features

### 📝 Create Order
1. Enter pharmaceutical company details
2. Specify product and molecular information
3. Set quantity and packaging requirements
4. Configure ingredient requirements (Y/N/N/A)
5. Submit to auto-generate sub-orders

### 👀 View Orders
- Comprehensive order listing with expandable details
- Sub-order information with full field display
- Status filtering and search capabilities
- Tabular view of sub-order summaries

### ⚙️ Sub-Orders Management
- Edit comprehensive sub-order details
- Update vendor, designer, and approval information
- Manage dates and status workflow
- Add remarks and documentation

## 🗄 Database Schema

### Orders Table
```sql
- order_id (INTEGER, Primary Key)
- company_name (VARCHAR)
- product_name (VARCHAR)
- molecule (VARCHAR)
- status (VARCHAR)
- quantity (INTEGER)
- pack (VARCHAR)
- carton, label, rm, sterios, bottles, m_cups, caps, shippers (VARCHAR)
```

### Sub-Orders Table
```sql
- sub_order_id (INTEGER, Primary Key)
- order_id (INTEGER, Foreign Key)
- ingredient_type (VARCHAR)
- quantity (INTEGER)
- pack (VARCHAR)
- status (VARCHAR)
- sub_order_date (DATETIME)
- vendor_company (VARCHAR)
- product_name (VARCHAR)
- main_order_date (DATETIME)
- designer_name (VARCHAR)
- sizes (VARCHAR)
- approved_by_first_name (VARCHAR)
- approved_by_last_name (VARCHAR)
- approved_date (DATETIME)
- remarks (TEXT)
```

## 🧪 Testing

Run the comprehensive API test suite:
```bash
python test_api.py
```

Tests include:
- Order creation and retrieval
- Sub-order generation
- Comprehensive field updates
- Data validation
- Error handling

## 🔧 Configuration

Customize application settings in `config/settings.py`:
- Database connection settings
- API configuration
- Frontend customization options

## 🚀 Development

### Adding New Features

1. **Backend**: Update models (`models.py`), schemas (`schemas.py`), and endpoints (`main.py`)
2. **Frontend**: Modify Streamlit interface (`streamlit_app.py`)
3. **Database**: Update models and handle migrations

### Code Quality
- Follow PEP 8 Python style guidelines
- Use type hints for better code documentation
- Implement proper error handling
- Add comprehensive logging

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port conflicts | Ensure ports 8000 and 8501 are available |
| Database errors | Delete `.db` files and restart to reinitialize |
| Import errors | Verify all requirements are installed |
| Date format issues | Ensure dates are in ISO format (YYYY-MM-DD) |

### Debug Information
- Check browser console for frontend errors
- Monitor backend logs for API issues
- Use API documentation for endpoint testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent async web framework
- Streamlit for the intuitive frontend framework
- SQLAlchemy for robust database ORM
- The pharmaceutical industry for inspiring this comprehensive solution

---

**Built with ❤️ for pharmaceutical manufacturing excellence**