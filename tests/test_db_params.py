#!/usr/bin/env python3
"""
Simple test for database parameter passing
"""
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.database import DatabaseManager

def test_db_params():
    """Test database parameter passing"""
    print("Testing database parameter passing...")
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Connect to database
    if not db_manager.connect():
        print("Failed to connect to database")
        return
    
    # Test 1: Query without parameters
    print("\nTest 1: Query without parameters")
    try:
        query = "SELECT 1 as test"
        df = db_manager.execute_query(query)
        print(f"Result: {df}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Query with tuple parameters
    print("\nTest 2: Query with tuple parameters")
    try:
        query = "SELECT %s as test"
        df = db_manager.execute_query(query, ("hello",))
        print(f"Result: {df}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Query with list parameters
    print("\nTest 3: Query with list parameters")
    try:
        query = "SELECT %s as test"
        df = db_manager.execute_query(query, ["world"])
        print(f"Result: {df}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_db_params()