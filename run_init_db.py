#!/usr/bin/env python3
"""
Simple script to run database initialization with correct Python path.
This can be run from the project root directory.
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import and run the initialization
try:
    from database.init_db import create_database, create_tables, create_sample_data
    
    print("🚀 Initializing PostgreSQL Database...")
    print("=" * 40)
    
    # Step 1: Create database
    print("\n📝 Creating database...")
    create_database()
    
    # Step 2: Create tables
    print("\n📝 Creating tables...")
    create_tables()
    
    # Step 3: Create sample data
    print("\n📝 Creating sample data...")
    create_sample_data()
    
    print("\n🎉 Database initialization completed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure you're running this script from the project root directory.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error during initialization: {e}")
    sys.exit(1)