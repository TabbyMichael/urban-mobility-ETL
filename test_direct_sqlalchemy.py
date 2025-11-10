#!/usr/bin/env python3
"""
Direct SQLAlchemy test
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

# Test what we're trying to do in our database manager
print("Testing direct SQLAlchemy approach...")

# This is what our database manager is trying to do
query = "SELECT %s as test"
params = ("hello",)

print(f"Original query: {query}")
print(f"Params: {params}")

# Convert to named parameters like we do in our database manager
param_dict = {f"param_{i+1}": param for i, param in enumerate(params)}
print(f"Param dict: {param_dict}")

named_query = query
for i in range(len(params)):
    named_query = named_query.replace("%s", f":param_{i+1}", 1)
print(f"Named query: {named_query}")

# Try to execute
try:
    with engine.connect() as conn:
        result = conn.execute(text(named_query), param_dict)
        print("Success!")
        print(result.fetchall())
except Exception as e:
    print(f"Error: {e}")