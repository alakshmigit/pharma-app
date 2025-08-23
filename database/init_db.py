import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (to postgres database)
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password'),
            port=os.getenv('DB_PORT', 5432),
            database='postgres'
        )
        
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        
        # Create database
        database_name = os.getenv('DB_NAME', 'pharma_orders')
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database '{database_name}' created successfully")
        else:
            print(f"Database '{database_name}' already exists")
        
        cursor.close()
        connection.close()
            
    except Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")

def create_sample_data():
    """Create some sample data for testing"""
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'pharma_user'),
            password=os.getenv('DB_PASSWORD', 'pharma_password_123'),
            database=os.getenv('DB_NAME', 'pharma_orders'),
            port=os.getenv('DB_PORT', 5432)
        )
        
        if connection:
            cursor = connection.cursor()
            
            # Sample orders
            sample_orders = [
                ("ABC Pharma", "Paracetamol 500mg", "Acetaminophen", "Open", 1000, "Bottle", "Y", "Y", "N", "N/A", "Y", "N", "Y", "N"),
                ("XYZ Healthcare", "Vitamin C 1000mg", "Ascorbic Acid", "In-Process", 500, "Blister", "N", "Y", "Y", "N/A", "N", "Y", "N", "Y"),
                ("MediCorp", "Aspirin 100mg", "Acetylsalicylic Acid", "Open", 2000, "Tablet", "Y", "N", "Y", "Y", "N/A", "N", "Y", "N")
            ]
            
            # Note: This is just for reference. The actual table creation and data insertion
            # will be handled by SQLAlchemy when the FastAPI app starts
            print("Sample data structure prepared")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")

if __name__ == "__main__":
    create_database()
    create_sample_data()