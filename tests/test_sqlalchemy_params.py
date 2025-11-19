#!/usr/bin/env python3
"""
Detailed test for SQLAlchemy parameter passing
"""
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os

def test_sqlalchemy_params():
    """Test SQLAlchemy parameter passing directly"""
    print("Testing SQLAlchemy parameter passing directly...")
    
    # Create engine
    try:
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'urban_mobility')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'postgres')
        
        db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = create_engine(db_url, echo=True)
        print(f"Connected to database: {db_url}")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return
    
    # Test 1: Query without parameters
    print("\nTest 1: Query without parameters")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            df = pd.DataFrame(result.fetchall())
            if not df.empty:
                df.columns = list(result.keys())
            print(f"Result: {df}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Query with tuple parameters
    print("\nTest 2: Query with tuple parameters")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT :param as test"), {"param": "hello"})
            df = pd.DataFrame(result.fetchall())
            if not df.empty:
                df.columns = list(result.keys())
            print(f"Result: {df}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Query with list parameters
    print("\nTest 3: Query with list parameters")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT :param as test"), {"param": "world"})
            df = pd.DataFrame(result.fetchall())
            if not df.empty:
                df.columns = list(result.keys())
            print(f"Result: {df}")
    except Exception as e:
        print(f"Error: {e}")

# Import pandas here to avoid issues
import pandas as pd

if __name__ == "__main__":
    test_sqlalchemy_params()