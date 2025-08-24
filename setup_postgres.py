#!/usr/bin/env python3
"""
PostgreSQL Setup Script for Pharma Order Management System
This script helps set up PostgreSQL database and initialize the application.
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2 import sql, Error
from dotenv import load_dotenv

load_dotenv()

def check_postgres_installed():
    """Check if PostgreSQL is installed"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL is not installed")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL is not installed")
        return False

def install_postgres_ubuntu():
    """Install PostgreSQL on Ubuntu/Debian"""
    print("Installing PostgreSQL on Ubuntu/Debian...")
    commands = [
        "sudo apt update",
        "sudo apt install -y postgresql postgresql-contrib",
        "sudo systemctl start postgresql",
        "sudo systemctl enable postgresql"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Failed to run: {cmd}")
            print(f"Error: {result.stderr}")
            return False
    
    print("✅ PostgreSQL installed successfully")
    return True

def setup_postgres_user():
    """Set up PostgreSQL user and database"""
    try:
        # Connect as postgres user
        print("Setting up PostgreSQL user and database...")
        
        # Create user and database using sudo -u postgres
        commands = [
            "sudo -u postgres createuser --interactive --pwprompt pharma_user",
            "sudo -u postgres createdb -O pharma_user pharma_db"
        ]
        
        for cmd in commands:
            print(f"Running: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0 and "already exists" not in result.stderr:
                print(f"Warning: {result.stderr}")
        
        print("✅ PostgreSQL user and database setup completed")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up PostgreSQL: {e}")
        return False

def test_connection():
    """Test database connection"""
    try:
        db_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', 5432),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'database': os.getenv('DB_NAME', 'pharma_db')
        }
        
        print(f"Testing connection to {db_params['host']}:{db_params['port']}/{db_params['database']}...")
        
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Database connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running: sudo systemctl status postgresql")
        print("2. Check if the database exists: sudo -u postgres psql -l")
        print("3. Verify connection parameters in .env file")
        print("4. Try connecting manually: psql -h localhost -U postgres -d pharma_db")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def initialize_database():
    """Initialize database with tables and sample data"""
    print("Initializing database...")
    try:
        from database.init_db import create_database, create_tables, create_sample_data
        
        create_database()
        create_tables()
        create_sample_data()
        
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 PostgreSQL Setup for Pharma Order Management System")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        if os.path.exists('.env.example'):
            subprocess.run(['cp', '.env.example', '.env'])
            print("✅ .env file created. Please update it with your database credentials.")
        else:
            print("❌ .env.example not found. Please create .env file manually.")
            return False
    
    # Step 1: Check PostgreSQL installation
    if not check_postgres_installed():
        if input("Would you like to install PostgreSQL? (y/n): ").lower() == 'y':
            if not install_postgres_ubuntu():
                print("❌ PostgreSQL installation failed")
                return False
        else:
            print("Please install PostgreSQL manually and run this script again.")
            return False
    
    # Step 2: Install Python dependencies
    if not install_python_dependencies():
        return False
    
    # Step 3: Test database connection
    if not test_connection():
        print("\n🔧 Database connection failed. You may need to:")
        print("1. Start PostgreSQL: sudo systemctl start postgresql")
        print("2. Create database: sudo -u postgres createdb pharma_db")
        print("3. Update .env file with correct credentials")
        return False
    
    # Step 4: Initialize database
    if not initialize_database():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the backend: python start_backend.py")
    print("2. Start the frontend: python start_frontend.py")
    print("3. Access the application at: https://work-1-beejymubnnozffwt.prod-runtime.all-hands.dev")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)