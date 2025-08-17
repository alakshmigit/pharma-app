import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'password'),
            port=os.getenv('DB_PORT', 3306)
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            database_name = os.getenv('DB_NAME', 'order_management')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"Database '{database_name}' created successfully or already exists")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

def create_sample_data():
    """Create some sample data for testing"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'password'),
            database=os.getenv('DB_NAME', 'order_management'),
            port=os.getenv('DB_PORT', 3306)
        )
        
        if connection.is_connected():
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
        print(f"Error while connecting to MySQL: {e}")

if __name__ == "__main__":
    create_database()
    create_sample_data()