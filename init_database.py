#!/usr/bin/env python3
"""
Initialize database tables for Urban Mobility Analytics
"""
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.database import DatabaseManager

def init_database():
    """Initialize database tables"""
    print("Initializing database...")
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Connect to database
    if not db_manager.connect():
        print("Failed to connect to database")
        return False
    
    # Initialize schema
    schema_success = db_manager.initialize_schema()
    if not schema_success:
        print("Failed to initialize database schema")
        db_manager.close()
        return False
    
    # Create indexes separately
    indexes_path = os.path.join(os.path.dirname(__file__), 'src', 'data', 'indexes.sql')
    # Fix the path since we're already in the root directory
    if not os.path.exists(indexes_path):
        indexes_path = os.path.join(os.path.dirname(__file__), 'data', 'indexes.sql')
    
    if os.path.exists(indexes_path):
        indexes_success = db_manager.execute_script(indexes_path)
        if not indexes_success:
            print("Warning: Failed to create indexes, but schema was created successfully")
        else:
            print("Database indexes created successfully")
    else:
        print("Warning: Indexes script not found, but schema was created successfully")
    
    print("Database schema initialized successfully")
    db_manager.close()
    return True

if __name__ == "__main__":
    success = init_database()
    if success:
        print("Database initialization completed successfully")
        sys.exit(0)
    else:
        print("Database initialization failed")
        sys.exit(1)