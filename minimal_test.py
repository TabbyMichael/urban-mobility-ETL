#!/usr/bin/env python3
"""
Minimal test for SQLAlchemy parameter passing
"""
import os
from sqlalchemy import create_engine, text

# Create engine
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'urban_mobility')
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'postgres')

db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(db_url)

# Test with positional parameters
print("Testing with positional parameters...")
try:
    with engine.connect() as conn:
        # In SQLAlchemy 2.0, we need to use named parameters
        result = conn.execute(text("SELECT :param as test"), {"param": "hello"})
        print("Success with named parameters!")
        print(result.fetchall())
except Exception as e:
    print(f"Error with named parameters: {e}")

# Test with named parameters
print("\nTesting with named parameters...")
try:
    with engine.connect() as conn:
        # This is the SQLAlchemy 2.0 way
        result = conn.execute(text("SELECT :param as test"), {"param": "world"})
        print("Success with dictionary!")
        print(result.fetchall())
except Exception as e:
    print(f"Error with dictionary: {e}")