#!/usr/bin/env python3
"""
Debug database parameter passing
"""
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.database import DatabaseManager

def debug_db_params():
    """Debug database parameter passing"""
    print("Debugging database parameter passing...")
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Connect to database
    if not db_manager.connect():
        print("Failed to connect to database")
        return
    
    # Test: Query with tuple parameters
    print("\nDebug Test: Query with tuple parameters")
    query = "SELECT %s as test"
    params = ("hello",)
    
    print(f"Query: {query}")
    print(f"Params: {params}")
    print(f"Params type: {type(params)}")
    
    # Let's manually do what the database manager should do
    param_dict = {f"param_{i+1}": param for i, param in enumerate(params)}
    print(f"Param dict: {param_dict}")
    
    named_query = query
    for i in range(len(params)):
        named_query = named_query.replace("%s", f":param_{i+1}", 1)
    print(f"Named query: {named_query}")

if __name__ == "__main__":
    debug_db_params()