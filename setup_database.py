#!/usr/bin/env python3
"""
Database Setup Script for Pharma Order Management System
This script creates the necessary database tables for local development.
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    from sqlalchemy import create_engine, text
    from models import Base
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing required packages. Please install dependencies first:")
    print(f"   pip install sqlalchemy pymysql python-dotenv")
    print(f"   Error: {e}")
    sys.exit(1)

def main():
    print("🏗️  Setting up Pharma Order Management Database...")
    
    # Load environment variables
    load_dotenv()
    
    # Get database URL
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in environment variables")
        print("   Please create a .env file with DATABASE_URL")
        print("   Example: DATABASE_URL=mysql+pymysql://pharma_user:pharma_password_123@localhost:3306/pharma_orders")
        sys.exit(1)
    
    print(f"📡 Connecting to database...")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL, echo=True)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Create all tables
        print("📋 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ Database setup completed successfully!")
        print("📋 Tables created:")
        print("   - users (for authentication)")
        print("   - orders (main orders)")
        print("   - sub_orders (ingredient sub-orders)")
        
        # Show table info
        with engine.connect() as connection:
            # Check if tables exist
            tables_query = text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
            """)
            result = connection.execute(tables_query)
            tables = [row[0] for row in result]
            
            print(f"\n📊 Database contains {len(tables)} tables:")
            for table in tables:
                print(f"   ✓ {table}")
        
        print("\n🚀 Ready to start the application!")
        print("   Backend: cd backend && uvicorn main:app --reload")
        print("   Frontend: cd frontend && streamlit run streamlit_app.py")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Make sure MySQL is running")
        print("   2. Verify database credentials in .env file")
        print("   3. Ensure the database 'pharma_orders' exists")
        print("   4. Check if user has proper permissions")
        sys.exit(1)

if __name__ == "__main__":
    main()