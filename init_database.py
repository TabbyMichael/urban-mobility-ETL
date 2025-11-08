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
    if db_manager.initialize_schema():
        print("Database schema initialized successfully")
        db_manager.close()
        return True
    else:
        print("Failed to initialize database schema")
        db_manager.close()
        return False

if __name__ == "__main__":
    success = init_database()
    if success:
        print("Database initialization completed successfully")
        sys.exit(0)
    else:
        print("Database initialization failed")
        sys.exit(1)