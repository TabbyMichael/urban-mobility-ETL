#!/usr/bin/env python3
"""
Test script for the database schema and initialization
"""
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.database import DatabaseManager

def test_database():
    """Test the database connection and schema"""
    print("Testing database connection and schema...")
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Test connection
    is_connected = db_manager.connect()
    print(f"Database connection: {is_connected}")
    
    if not is_connected:
        print("Failed to connect to database. Please check your database configuration.")
        return
    
    # Test schema initialization
    schema_initialized = db_manager.initialize_schema()
    print(f"Schema initialization: {schema_initialized}")
    
    # Test if tables exist
    tables_to_check = ["trips", "zones", "users", "weather", "uber_travel_times", "mta_status", "features_ml"]
    
    for table in tables_to_check:
        exists = db_manager.table_exists(table)
        print(f"Table '{table}' exists: {exists}")
    
    # Test user table specifically
    if db_manager.table_exists("users"):
        df = db_manager.execute_query("SELECT id, username, role FROM users")
        print(f"Users in database: {len(df)}")
        if not df.empty:
            print("User data:")
            print(df)
    
    # Close connection
    db_manager.close()
    print("Database test completed!")

if __name__ == "__main__":
    test_database()