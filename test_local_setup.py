#!/usr/bin/env python3
"""
Test script to verify local development setup
This script tests database connectivity, API endpoints, and basic functionality.
"""

import sys
import os
import time
import requests
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing Python imports...")
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import psycopg2
        import streamlit
        import requests
        from dotenv import load_dotenv
        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("🧪 Testing environment configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.getenv("DATABASE_URL")
        secret_key = os.getenv("SECRET_KEY")
        
        if not database_url:
            print("❌ DATABASE_URL not found in environment")
            return False
            
        if not secret_key:
            print("❌ SECRET_KEY not found in environment")
            return False
            
        print("✅ Environment configuration loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Environment error: {e}")
        return False

def test_database_connection():
    """Test database connectivity"""
    print("🧪 Testing database connection...")
    
    try:
        from sqlalchemy import create_engine, text
        from dotenv import load_dotenv
        
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        
        engine = create_engine(database_url)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_database_tables():
    """Test if database tables exist"""
    print("🧪 Testing database tables...")
    
    try:
        from sqlalchemy import create_engine, text
        from dotenv import load_dotenv
        
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        
        engine = create_engine(database_url)
        with engine.connect() as connection:
            # Check for tables
            tables_query = text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
            """)
            result = connection.execute(tables_query)
            tables = [row[0] for row in result]
            
            required_tables = ['users', 'orders', 'sub_orders']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                print("💡 Run: python setup_database.py")
                return False
            
            print(f"✅ All required tables exist: {tables}")
            return True
    except Exception as e:
        print(f"❌ Database tables error: {e}")
        return False

def test_backend_api():
    """Test if backend API is running"""
    print("🧪 Testing backend API...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running and healthy")
            return True
        else:
            print(f"❌ Backend API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend API is not running")
        print("💡 Start with: cd backend && uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Backend API error: {e}")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    print("🧪 Testing frontend accessibility...")
    
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running")
        print("💡 Start with: cd frontend && streamlit run streamlit_app.py")
        return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False

def test_api_endpoints():
    """Test basic API endpoints"""
    print("🧪 Testing API endpoints...")
    
    try:
        # Test registration endpoint
        response = requests.post("http://localhost:8000/register", 
                               json={"username": "testuser", "email": "test@example.com", "password": "testpass123"},
                               timeout=5)
        
        if response.status_code in [200, 400]:  # 400 if user already exists
            print("✅ Registration endpoint working")
        else:
            print(f"❌ Registration endpoint error: {response.status_code}")
            return False
            
        # Test orders endpoint (should require auth)
        response = requests.get("http://localhost:8000/orders", timeout=5)
        if response.status_code == 401:  # Should be unauthorized without token
            print("✅ Orders endpoint properly protected")
            return True
        else:
            print(f"❌ Orders endpoint security issue: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API endpoints error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Local Development Setup Tests")
    print("=" * 50)
    
    tests = [
        ("Python Imports", test_imports),
        ("Environment Config", test_environment),
        ("Database Connection", test_database_connection),
        ("Database Tables", test_database_tables),
        ("Backend API", test_backend_api),
        ("Frontend", test_frontend),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your local setup is working perfectly!")
        print("\n🚀 Ready to start development:")
        print("   Frontend: http://localhost:8501")
        print("   Backend:  http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the issues above.")
        print("\n💡 Common solutions:")
        print("   - Make sure PostgreSQL is running")
        print("   - Run: python setup_database.py")
        print("   - Start services: ./start_app.sh")
        print("   - Check .env configuration")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)