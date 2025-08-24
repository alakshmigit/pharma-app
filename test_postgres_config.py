#!/usr/bin/env python3
"""
Test PostgreSQL configuration without requiring a running PostgreSQL instance.
This script validates the configuration and imports.
"""

import sys
import os

def test_imports():
    """Test that all PostgreSQL-related imports work"""
    print("🧪 Testing PostgreSQL imports...")
    
    try:
        import psycopg2
        print("✅ psycopg2 imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import psycopg2: {e}")
        return False
    
    try:
        from sqlalchemy import create_engine
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import SQLAlchemy: {e}")
        return False
    
    try:
        from config.database import Base, engine, get_db
        print("✅ Database configuration imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import database config: {e}")
        return False
    
    try:
        from backend.models import Order, SubOrder
        print("✅ Database models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import models: {e}")
        return False
    
    return True

def test_database_url():
    """Test database URL configuration"""
    print("\n🔗 Testing database URL configuration...")
    
    from config.database import engine
    
    # Get the database URL from the engine
    db_url = str(engine.url)
    print(f"Database URL: {db_url}")
    
    if "postgresql" in db_url:
        print("✅ PostgreSQL URL detected")
        return True
    else:
        print("❌ PostgreSQL URL not detected")
        return False

def test_model_definitions():
    """Test that models are properly defined for PostgreSQL"""
    print("\n📋 Testing model definitions...")
    
    from backend.models import Order, SubOrder
    from sqlalchemy import inspect
    
    # Test Order model
    order_columns = [column.name for column in inspect(Order).columns]
    expected_order_columns = [
        'order_id', 'company_name', 'product_name', 'molecule', 
        'status', 'quantity', 'pack', 'created_at', 'updated_at',
        'carton', 'label', 'rm', 'sterios', 'bottles', 'm_cups', 'caps', 'shippers'
    ]
    
    missing_columns = set(expected_order_columns) - set(order_columns)
    if missing_columns:
        print(f"❌ Missing columns in Order model: {missing_columns}")
        return False
    else:
        print("✅ Order model has all expected columns")
    
    # Test SubOrder model
    suborder_columns = [column.name for column in inspect(SubOrder).columns]
    expected_suborder_columns = [
        'sub_order_id', 'order_id', 'ingredient_type', 'status',
        'created_at', 'updated_at', 'sub_order_date'
    ]
    
    missing_suborder_columns = set(expected_suborder_columns) - set(suborder_columns)
    if missing_suborder_columns:
        print(f"❌ Missing columns in SubOrder model: {missing_suborder_columns}")
        return False
    else:
        print("✅ SubOrder model has all expected columns")
    
    return True

def test_environment_variables():
    """Test environment variable configuration"""
    print("\n🌍 Testing environment variables...")
    
    # Check if .env.example exists
    if os.path.exists('.env.example'):
        print("✅ .env.example file exists")
    else:
        print("❌ .env.example file missing")
        return False
    
    # Check default DATABASE_URL
    from config.database import engine
    db_url = str(engine.url)
    
    if "postgresql" in db_url and "pharma_db" in db_url:
        print("✅ Default PostgreSQL configuration detected")
        return True
    else:
        print("❌ PostgreSQL configuration not properly set")
        return False

def main():
    """Run all tests"""
    print("🚀 PostgreSQL Configuration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Database URL Test", test_database_url),
        ("Model Definition Test", test_model_definitions),
        ("Environment Variables Test", test_environment_variables)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📝 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! PostgreSQL configuration is ready.")
        print("\nNext steps:")
        print("1. Install PostgreSQL: sudo apt install postgresql postgresql-contrib")
        print("2. Start PostgreSQL: sudo systemctl start postgresql")
        print("3. Create database: python database/init_db.py")
        print("4. Start application: python start_backend.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)