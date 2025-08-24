#!/usr/bin/env python3
"""
Standalone database initialization script that can be run from any directory.
This script initializes the PostgreSQL database with tables and sample data.
"""

import os
import sys
import psycopg2
from psycopg2 import sql, Error
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

def get_database_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'database': os.getenv('DB_NAME', 'pharma_db')
    }

def create_database():
    """Create the PostgreSQL database if it doesn't exist"""
    config = get_database_config()
    
    try:
        # Connect to PostgreSQL server (to default 'postgres' database)
        connection = psycopg2.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            port=config['port'],
            database='postgres'  # Connect to default database first
        )
        
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (config['database'],))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config['database'])))
            print(f"✅ Database '{config['database']}' created successfully")
        else:
            print(f"✅ Database '{config['database']}' already exists")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error while connecting to PostgreSQL: {e}")
        return False

def create_tables():
    """Create all tables using SQLAlchemy"""
    try:
        # Get database URL
        config = get_database_config()
        database_url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        
        # Create engine
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False
        )
        
        # Import and create models
        from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
        from sqlalchemy.orm import relationship
        
        Base = declarative_base()
        
        class Order(Base):
            __tablename__ = "orders"
            
            order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
            company_name = Column(String(255), nullable=False, index=True)
            product_name = Column(String(255), nullable=False, index=True)
            molecule = Column(String(255), nullable=False)
            status = Column(String(50), nullable=False, default="Open", index=True)
            quantity = Column(Integer, nullable=False)
            pack = Column(String(100), nullable=False)
            
            # Timestamps
            created_at = Column(DateTime(timezone=True), server_default=func.now())
            updated_at = Column(DateTime(timezone=True), onupdate=func.now())
            
            # Ingredients
            carton = Column(String(10), nullable=False, default="N/A")
            label = Column(String(10), nullable=False, default="N/A")
            rm = Column(String(10), nullable=False, default="N/A")
            sterios = Column(String(10), nullable=False, default="N/A")
            bottles = Column(String(10), nullable=False, default="N/A")
            m_cups = Column(String(10), nullable=False, default="N/A")
            caps = Column(String(10), nullable=False, default="N/A")
            shippers = Column(String(10), nullable=False, default="N/A")
            
            # Relationship
            sub_orders = relationship("SubOrder", back_populates="order", cascade="all, delete-orphan")

        class SubOrder(Base):
            __tablename__ = "sub_orders"
            
            sub_order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
            order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False, index=True)
            ingredient_type = Column(String(50), nullable=False, index=True)
            status = Column(String(50), nullable=False, default="Open", index=True)
            
            # Timestamps
            created_at = Column(DateTime(timezone=True), server_default=func.now())
            updated_at = Column(DateTime(timezone=True), onupdate=func.now())
            
            # Comprehensive fields
            sub_order_date = Column(DateTime(timezone=True), nullable=True, default=func.now())
            vendor_company = Column(String(255), nullable=True)
            product_name = Column(String(255), nullable=True)
            main_order_date = Column(DateTime(timezone=True), nullable=True)
            designer_name = Column(String(255), nullable=True)
            sizes = Column(String(255), nullable=True)
            approved_by_first_name = Column(String(100), nullable=True)
            approved_by_last_name = Column(String(100), nullable=True)
            approved_date = Column(DateTime(timezone=True), nullable=True)
            remarks = Column(Text, nullable=True)
            
            # Relationship
            order = relationship("Order", back_populates="sub_orders")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
        
        return engine, Base, Order, SubOrder
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return None, None, None, None

def create_sample_data(engine, Order, SubOrder):
    """Create some sample data for testing"""
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if data already exists
        existing_orders = db.query(Order).count()
        if existing_orders > 0:
            print(f"✅ Sample data already exists ({existing_orders} orders found)")
            db.close()
            return True
        
        # Sample orders
        sample_orders = [
            Order(
                company_name="ABC Pharma",
                product_name="Paracetamol 500mg",
                molecule="Acetaminophen",
                status="Open",
                quantity=1000,
                pack="Bottle",
                carton="Y",
                label="Y",
                rm="N",
                sterios="N/A",
                bottles="Y",
                m_cups="N",
                caps="Y",
                shippers="N"
            ),
            Order(
                company_name="XYZ Healthcare",
                product_name="Vitamin C 1000mg",
                molecule="Ascorbic Acid",
                status="In-Process",
                quantity=500,
                pack="Blister",
                carton="N",
                label="Y",
                rm="Y",
                sterios="N/A",
                bottles="N",
                m_cups="Y",
                caps="N",
                shippers="Y"
            ),
            Order(
                company_name="MediCorp",
                product_name="Aspirin 100mg",
                molecule="Acetylsalicylic Acid",
                status="Open",
                quantity=2000,
                pack="Tablet",
                carton="Y",
                label="N",
                rm="Y",
                sterios="Y",
                bottles="N/A",
                m_cups="N",
                caps="Y",
                shippers="N"
            )
        ]
        
        # Add orders to database
        for order in sample_orders:
            db.add(order)
        
        db.commit()
        print("✅ Sample orders created successfully")
        
        # Create sub-orders for ingredients marked as "Y"
        orders = db.query(Order).all()
        for order in orders:
            ingredients = {
                'carton': order.carton,
                'label': order.label,
                'rm': order.rm,
                'sterios': order.sterios,
                'bottles': order.bottles,
                'm_cups': order.m_cups,
                'caps': order.caps,
                'shippers': order.shippers
            }
            
            for ingredient_type, value in ingredients.items():
                if value == "Y":
                    sub_order = SubOrder(
                        order_id=order.order_id,
                        ingredient_type=ingredient_type,
                        status="Open"
                    )
                    db.add(sub_order)
        
        db.commit()
        print("✅ Sample sub-orders created successfully")
        
        # Print summary
        total_orders = db.query(Order).count()
        total_sub_orders = db.query(SubOrder).count()
        print(f"📊 Database initialized with {total_orders} orders and {total_sub_orders} sub-orders")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def test_connection():
    """Test database connection"""
    try:
        config = get_database_config()
        database_url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        
        engine = create_engine(database_url)
        connection = engine.connect()
        result = connection.execute("SELECT version();")
        version = result.fetchone()
        
        print(f"✅ Database connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running: sudo systemctl status postgresql")
        print("2. Check if the database exists: sudo -u postgres psql -l")
        print("3. Verify connection parameters in .env file")
        print("4. Try connecting manually: psql -h localhost -U postgres -d pharma_db")
        return False

def main():
    """Main initialization function"""
    print("🚀 PostgreSQL Database Initialization")
    print("=" * 50)
    
    # Step 1: Create database
    print("\n📝 Step 1: Creating database...")
    if not create_database():
        print("❌ Failed to create database")
        return False
    
    # Step 2: Test connection
    print("\n📝 Step 2: Testing connection...")
    if not test_connection():
        print("❌ Failed to connect to database")
        return False
    
    # Step 3: Create tables
    print("\n📝 Step 3: Creating tables...")
    engine, Base, Order, SubOrder = create_tables()
    if engine is None:
        print("❌ Failed to create tables")
        return False
    
    # Step 4: Create sample data
    print("\n📝 Step 4: Creating sample data...")
    if not create_sample_data(engine, Order, SubOrder):
        print("❌ Failed to create sample data")
        return False
    
    print("\n🎉 Database initialization completed successfully!")
    print("\nNext steps:")
    print("1. Start the backend: python start_backend.py")
    print("2. Start the frontend: python start_frontend.py")
    print("3. Access the application at: https://work-1-beejymubnnozffwt.prod-runtime.all-hands.dev")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)