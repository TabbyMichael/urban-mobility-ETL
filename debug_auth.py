#!/usr/bin/env python3
"""
Debug script for authentication issues
"""
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.auth.auth import auth_manager
from src.data.database import DatabaseManager

def debug_auth():
    """Debug authentication issues"""
    print("Debugging authentication...")
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Connect to database
    if not db_manager.connect():
        print("Failed to connect to database")
        return
    
    # Check if users table exists
    if not db_manager.table_exists("users"):
        print("Users table does not exist")
        return
    
    # Query all users
    query = "SELECT id, username, password_hash, role FROM users"
    df = db_manager.execute_query(query)
    
    print("Users in database:")
    print(df)
    
    # Test authentication for each user
    for index, row in df.iterrows():
        username = row['username']
        password_hash = row['password_hash']
        role = row['role']
        
        print(f"\nTesting user: {username}")
        print(f"Password hash: {password_hash}")
        print(f"Role: {role}")
        
        # Test authentication with a known password
        if username == "testuser":
            result = auth_manager.authenticate_user(username, "testpassword")
            print(f"Auth result: {result}")
        elif username == "admin":
            result = auth_manager.authenticate_user(username, "admin123")
            print(f"Auth result: {result}")

if __name__ == "__main__":
    debug_auth()