# 🏥 Pharma-App: Pharmaceutical Order Management System

A comprehensive pharmaceutical order management system built with Python backend (FastAPI), Streamlit frontend, and PostgreSQL database. Features complete authentication system, AWS deployment infrastructure, and automated local development setup.

## ✨ Key Features

### 🔐 **Authentication System**
- **User Registration & Login**: Secure JWT-based authentication
- **Password Security**: Bcrypt hashing for password protection
- **Protected Routes**: All API endpoints secured with authentication
- **User Management**: Complete user profile and session management

### 📦 **Order Management**
- **Order Creation**: Create orders with comprehensive pharmaceutical details
- **Company Tracking**: Manage pharmaceutical company information
- **Product Management**: Track product names and molecular information
- **Status Workflow**: Monitor order status (In-Process, Closed, Open)
- **Quantity & Packaging**: Manage order quantities and packaging specifications
- **Audit Trails**: Track created_by and modified_by for all records

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

### **Core Technologies**
- **Backend**: FastAPI (Python) - High-performance async API
- **Frontend**: Streamlit - Interactive web interface  
- **Database**: PostgreSQL 12+ with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **API Documentation**: Automatic OpenAPI/Swagger
- **Data Validation**: Pydantic schemas

### **Deployment & Infrastructure**
- **Cloud Platform**: AWS (ECS Fargate, RDS, ALB, VPC)
- **Containerization**: Docker with multi-stage builds
- **Infrastructure as Code**: Terraform
- **Monitoring**: CloudWatch
- **Security**: VPC isolation, security groups, encryption

## 📁 Project Structure

```
pharma-app/
├── backend/
│   ├── main.py              # FastAPI application & API endpoints
│   ├── models.py            # SQLAlchemy database models
│   ├── auth.py              # JWT authentication system
│   ├── schemas.py           # Pydantic validation schemas
│   ├── crud.py              # Database CRUD operations
│   ├── Dockerfile           # Backend container configuration
│   └── requirements.txt     # Backend Python dependencies
├── frontend/
│   ├── streamlit_app.py     # Streamlit web interface
│   ├── Dockerfile           # Frontend container configuration
│   └── requirements.txt     # Frontend Python dependencies
├── terraform/               # AWS Infrastructure as Code
│   ├── main.tf              # Main Terraform configuration
│   ├── ecs.tf               # ECS Fargate configuration
│   ├── rds.tf               # RDS PostgreSQL configuration
│   ├── alb.tf               # Application Load Balancer
│   ├── ecr.tf               # Container registry
│   ├── variables.tf         # Terraform variables
│   └── outputs.tf           # Terraform outputs
├── install.sh               # Automated installation script
├── start_app.sh             # Linux/macOS startup script
├── start_app.bat            # Windows startup script
├── setup_database.py        # Database initialization
├── test_local_setup.py      # Comprehensive testing script
├── deploy.sh                # AWS deployment script
├── validate-deployment.sh   # Deployment validation
├── LOCAL_SETUP.md           # Local development guide
├── DEPLOYMENT.md            # AWS deployment guide
├── INSTALLATION_SUMMARY.md  # Complete setup summary
└── README.md                # This file
```

## 🚀 Quick Start

### 🏠 **Local Development Setup**

#### **One-Command Setup (Recommended)**

##### Linux/macOS:
```bash
git clone https://github.com/alakshmigit/pharma-app.git
cd pharma-app
./install.sh          # Install all dependencies
./start_app.sh         # Start the application
```

##### Windows:
```batch
git clone https://github.com/alakshmigit/pharma-app.git
cd pharma-app
start_app.bat          # Install and start automatically
```

#### **Prerequisites**
- **Python 3.8+** (recommended: Python 3.9 or 3.10)
- **PostgreSQL 12+** (or compatible version)
- **Git** for version control

#### **PostgreSQL Database Setup**
```sql
sudo -u postgres psql

CREATE DATABASE pharma_orders;
CREATE USER pharma_user WITH PASSWORD 'pharma_password_123';
GRANT ALL PRIVILEGES ON DATABASE pharma_orders TO pharma_user;
\q
```

#### **Manual Setup (if scripts don't work)**

1. **Clone and Setup Environment**:
   ```bash
   git clone https://github.com/alakshmigit/pharma-app.git
   cd pharma-app
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt
   ```

3. **Configure Environment** (create `.env` file):
   ```env
   DATABASE_URL=postgresql+psycopg2://pharma_user:pharma_password_123@localhost:5432/pharma_orders
   SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Initialize Database**:
   ```bash
   python setup_database.py
   ```

5. **Start Services**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   
   # Terminal 2 - Frontend  
   cd frontend
   streamlit run streamlit_app.py --server.port 8501
   ```

#### **Testing Your Setup**
```bash
python test_local_setup.py  # Comprehensive testing
```

### ☁️ **AWS Production Deployment**

#### **One-Command Deployment**
```bash
# Configure AWS credentials first
aws configure

# Deploy to AWS
./deploy.sh

# Validate deployment
./validate-deployment.sh
```

#### **Cost Estimation**
- **Small Production**: ~$55-80/month
- **Includes**: ECS Fargate, RDS PostgreSQL, ALB, VPC

### 🌐 **Access Points**

#### **Local Development**:
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

#### **Production (AWS)**:
- **Application**: `https://your-alb-url.amazonaws.com`
- **API Docs**: `https://your-alb-url.amazonaws.com/docs`

## 📚 API Documentation

Access comprehensive API documentation:
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

### Key API Endpoints

#### **Authentication**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register` | Register new user |
| `POST` | `/login` | User login (returns JWT token) |
| `GET` | `/me` | Get current user info |

#### **Orders Management**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/orders/` | List all orders (protected) |
| `POST` | `/orders/` | Create new order (protected) |
| `GET` | `/orders/{order_id}` | Get specific order (protected) |
| `PUT` | `/orders/{order_id}` | Update order (protected) |
| `DELETE` | `/orders/{order_id}` | Delete order (protected) |

#### **Sub-Orders Management**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/sub-orders/` | List all sub-orders (protected) |
| `GET` | `/sub-orders/{sub_order_id}` | Get specific sub-order (protected) |
| `PUT` | `/sub-orders/{sub_order_id}` | Update sub-order details (protected) |

## 💻 User Interface Guide

### 🔐 **Authentication**
- **Registration**: Create new user account with username, email, password
- **Login**: Secure login with JWT token generation
- **Session Management**: Automatic token refresh and logout

### 🏠 **Dashboard**
- Overview of system status and user information
- Quick navigation to all features
- User profile display and logout option

### 📝 **Create Order**
1. **Authentication Required**: Must be logged in
2. Enter pharmaceutical company details
3. Specify product and molecular information
4. Set quantity and packaging requirements
5. Configure ingredient requirements (Y/N/N/A)
6. Submit to auto-generate sub-orders with audit trail

### 👀 **View Orders**
- **Protected Access**: Authentication required
- Comprehensive order listing with expandable details
- Sub-order information with full field display
- Status filtering and search capabilities
- User-specific data based on authentication
- Audit information (created by, modified by)

### ⚙️ **Sub-Orders Management**
- **Secure Updates**: All changes tracked with user information
- Edit comprehensive sub-order details
- Update vendor, designer, and approval information
- Manage dates and status workflow
- Add remarks and documentation with audit trails

## 🗄 Database Schema

### Users Table
```sql
- id (INTEGER, Primary Key)
- username (VARCHAR, Unique)
- email (VARCHAR, Unique)
- hashed_password (VARCHAR)
- created_at (DATETIME)
- updated_at (DATETIME)
```

### Orders Table
```sql
- id (INTEGER, Primary Key)
- company_name (VARCHAR)
- product_name (VARCHAR)
- molecule (VARCHAR)
- status (VARCHAR)
- quantity (INTEGER)
- pack (VARCHAR)
- order_date (DATETIME)
- carton, label, rm, sterios, bottles, m_cups, caps, shippers (VARCHAR)
- created_by (INTEGER, Foreign Key -> Users)
- modified_by (INTEGER, Foreign Key -> Users)
- created_at (DATETIME)
- updated_at (DATETIME)
```

### Sub-Orders Table
```sql
- id (INTEGER, Primary Key)
- order_id (INTEGER, Foreign Key -> Orders)
- ingredient_type (VARCHAR)
- quantity (INTEGER)
- pack (VARCHAR)
- status (VARCHAR)
- sub_order_date (DATETIME)
- main_order_date (DATETIME)
- vendor_company (VARCHAR)
- product_name (VARCHAR)
- designer_name (VARCHAR)
- sizes (VARCHAR)
- approved_by_first_name (VARCHAR)
- approved_by_last_name (VARCHAR)
- approved_date (DATETIME)
- remarks (TEXT)
- created_by (INTEGER, Foreign Key -> Users)
- modified_by (INTEGER, Foreign Key -> Users)
- created_at (DATETIME)
- updated_at (DATETIME)
```

## 🧪 Testing

### **Comprehensive Local Setup Testing**
```bash
python test_local_setup.py
```

Tests include:
- ✅ Python package imports validation
- ✅ Environment configuration verification
- ✅ Database connectivity testing
- ✅ Database tables existence check
- ✅ Backend API health monitoring
- ✅ Frontend accessibility verification
- ✅ API endpoint security validation

### **API Testing**
```bash
python test_api.py
```

Tests include:
- Authentication system (register, login, protected routes)
- Order creation and retrieval with user context
- Sub-order generation with audit trails
- Comprehensive field updates
- Data validation and error handling
- JWT token validation

## 🔧 Configuration

### **Environment Variables** (`.env` file)

#### **Database Configuration**
```env
DATABASE_URL=postgresql+psycopg2://pharma_user:pharma_password_123@localhost:5432/pharma_orders
```

#### **JWT Authentication**
```env
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### **Application Settings**
```env
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8501
DEBUG=True
ENVIRONMENT=development
```

### **AWS Deployment Configuration**
Configure in `terraform/terraform.tfvars`:
```hcl
aws_region = "us-east-1"
environment = "production"
app_name = "pharma-app"
db_username = "pharma_admin"
db_password = "your-secure-password"
```

## 🚀 Development

### **Development Workflow**

#### **Making Changes**
- **Backend**: Edit files in `backend/` directory (auto-reloads with `--reload`)
- **Frontend**: Edit `frontend/streamlit_app.py` (auto-reloads)
- **Database**: Update `models.py` and run `python setup_database.py`

#### **Adding New Features**
1. **Backend**: Update models (`models.py`), auth (`auth.py`), and endpoints (`main.py`)
2. **Frontend**: Modify Streamlit interface (`streamlit_app.py`)
3. **Database**: Update models and handle migrations
4. **Authentication**: Ensure new endpoints are properly protected

#### **Adding Dependencies**
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

### **Code Quality Standards**
- Follow PEP 8 Python style guidelines
- Use type hints for better code documentation
- Implement proper error handling and logging
- Add authentication to all sensitive endpoints
- Include audit trails for data modifications
- Write comprehensive tests for new features

## 🐛 Troubleshooting

### **Common Issues & Solutions**

#### **Installation Issues**
| Issue | Solution |
|-------|----------|
| PostgreSQL connection error | Check PostgreSQL service: `sudo systemctl status postgresql` |
| Port conflicts (8000, 8501) | Kill processes: `lsof -i :8000` then `kill -9 <PID>` |
| Python dependencies | Reinstall: `pip install --upgrade --force-reinstall -r requirements.txt` |
| Virtual environment issues | Recreate: `rm -rf venv && python -m venv venv` |

#### **Authentication Issues**
| Issue | Solution |
|-------|----------|
| JWT token errors | Check SECRET_KEY in `.env` file |
| Login failures | Verify user exists and password is correct |
| Protected route access | Ensure valid JWT token in request headers |

#### **Database Issues**
| Issue | Solution |
|-------|----------|
| Connection refused | Verify PostgreSQL is running and credentials are correct |
| Table doesn't exist | Run `python setup_database.py` to initialize |
| Migration errors | Drop tables and reinitialize database |

### **Debug Information**
- **Frontend Errors**: Check browser console and Streamlit logs
- **Backend Errors**: Monitor FastAPI logs and `/docs` endpoint
- **Database Errors**: Check PostgreSQL logs and connection parameters
- **Authentication**: Test endpoints with `/docs` interactive interface

### **Getting Help**
- **Local Setup**: See `LOCAL_SETUP.md` for detailed instructions
- **AWS Deployment**: See `DEPLOYMENT.md` for cloud setup
- **Testing**: Run `python test_local_setup.py` for diagnostics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 **Documentation**

### **Complete Guides Available**
- **`LOCAL_SETUP.md`** - Comprehensive local development setup (50+ pages)
- **`README_LOCAL.md`** - Quick start guide for local development
- **`INSTALLATION_SUMMARY.md`** - Complete installation overview
- **`DEPLOYMENT.md`** - AWS deployment guide with Terraform
- **`QUICKSTART.md`** - AWS quick start instructions

### **Key Features Summary**
- ✅ **Complete Authentication System** with JWT tokens
- ✅ **PostgreSQL Database** with comprehensive schema
- ✅ **AWS Deployment Ready** with Terraform infrastructure
- ✅ **Local Development Setup** with automated scripts
- ✅ **Comprehensive Testing** with validation scripts
- ✅ **Production Ready** with security best practices

## 🙏 Acknowledgments

- **FastAPI** for the excellent async web framework
- **Streamlit** for the intuitive frontend framework
- **SQLAlchemy** for robust database ORM
- **PostgreSQL** for reliable database management
- **AWS** for scalable cloud infrastructure
- **Terraform** for infrastructure as code
- **JWT** for secure authentication
- The pharmaceutical industry for inspiring this comprehensive solution

---

## 🎯 **Next Steps**

1. **Start Local Development**: Use `./install.sh` and `./start_app.sh`
2. **Test Your Setup**: Run `python test_local_setup.py`
3. **Deploy to AWS**: Use `./deploy.sh` for production deployment
4. **Customize**: Modify the application for your specific needs

**Built with ❤️ for pharmaceutical manufacturing excellence**

---

### 🔗 **Quick Links**
- **GitHub Repository**: https://github.com/alakshmigit/pharma-app
- **Local Setup Guide**: [LOCAL_SETUP.md](LOCAL_SETUP.md)
- **AWS Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Installation Summary**: [INSTALLATION_SUMMARY.md](INSTALLATION_SUMMARY.md)