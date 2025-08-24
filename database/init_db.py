import psycopg2
from psycopg2 import sql, Error
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from config.database import Base, engine
from backend.models import Order, SubOrder

load_dotenv()

def create_database():
    """Create the PostgreSQL database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (to default 'postgres' database)
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password'),
            port=os.getenv('DB_PORT', 5432),
            database='postgres'  # Connect to default database first
        )
        
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Create database
        database_name = os.getenv('DB_NAME', 'pharma_db')
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database_name,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
            print(f"Database '{database_name}' created successfully")
        else:
            print(f"Database '{database_name}' already exists")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")

def create_tables():
    """Create all tables using SQLAlchemy"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully")
        
    except Exception as e:
        print(f"Error creating tables: {e}")

def create_sample_data():
    """Create some sample data for testing"""
    try:
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if data already exists
        existing_orders = db.query(Order).count()
        if existing_orders > 0:
            print(f"Sample data already exists ({existing_orders} orders found)")
            db.close()
            return
        
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
        print("Sample data created successfully")
        
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
        print("Sample sub-orders created successfully")
        db.close()
        
    except Exception as e:
        print(f"Error creating sample data: {e}")

if __name__ == "__main__":
    create_database()
    create_tables()
    create_sample_data()