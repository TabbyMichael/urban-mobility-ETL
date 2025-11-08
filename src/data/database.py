import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool
import logging
from functools import lru_cache
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.memory_storage = {}
        self.logger = logging.getLogger(__name__)
        
        # Try to connect to PostgreSQL using environment variables
        try:
            db_host = os.getenv('DB_HOST', 'localhost')
            db_port = os.getenv('DB_PORT', '5432')
            db_name = os.getenv('DB_NAME', 'urban_mobility')
            db_user = os.getenv('DB_USER', 'postgres')
            db_password = os.getenv('DB_PASSWORD', 'postgres')
            
            db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
            # Create engine with connection pooling
            self.engine = create_engine(
                db_url, 
                echo=False,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.logger.info("Successfully connected to PostgreSQL database")
        except Exception as e:
            self.logger.warning(f"Failed to connect to PostgreSQL: {e}")
            self.logger.info("Using in-memory storage as fallback")
            self.engine = None
    
    def connect(self):
        """Connect to the database"""
        return self.engine is not None
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
    
    def store_in_memory(self, table_name, data):
        """Store data in memory when database is not available"""
        self.memory_storage[table_name] = data
        self.logger.info(f"Data stored in memory: {table_name}")
        return True
    
    def load_from_memory(self, table_name):
        """Load data from memory"""
        return self.memory_storage.get(table_name, pd.DataFrame())
    
    def table_exists(self, table_name):
        """Check if table exists in database or memory"""
        if self.engine:
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')"))
                    return result.scalar()
            except:
                return False
        else:
            return table_name in self.memory_storage
    
    def save_data(self, data, table_name):
        """Save data to database or memory"""
        if self.engine:
            try:
                # Save to database
                data.to_sql(table_name, self.engine, if_exists='replace', index=False)
                self.logger.info(f"Data saved to database table: {table_name}")
                return True
            except SQLAlchemyError as e:
                self.logger.error(f"Database error: {e}")
                # Fallback to memory storage
                return self.store_in_memory(table_name, data)
        else:
            # Use memory storage
            return self.store_in_memory(table_name, data)
    
    def load_data(self, table_name):
        """Load data from database or memory"""
        if self.engine and self.table_exists(table_name):
            try:
                # Load from database
                data = pd.read_sql_table(table_name, self.engine)
                self.logger.info(f"Data loaded from database table: {table_name}")
                return data
            except Exception as e:
                self.logger.error(f"Error loading from database: {e}")
                # Fallback to memory
                return self.load_from_memory(table_name)
        else:
            # Load from memory
            return self.load_from_memory(table_name)
    
    @lru_cache(maxsize=128)
    def execute_query_cached(self, query, params=None):
        """Execute a SQL query with caching"""
        return self._execute_query_internal(query, params)
    
    def execute_query(self, query, params=None):
        """Execute a SQL query without caching"""
        return self._execute_query_internal(query, params)
    
    def _execute_query_internal(self, query, params=None):
        """Internal method to execute a SQL query"""
        if self.engine:
            try:
                with self.engine.connect() as conn:
                    if params:
                        result = conn.execute(text(query), **params)
                    else:
                        result = conn.execute(text(query))
                    # Convert result to DataFrame using pandas built-in method
                    df = pd.DataFrame(result.fetchall())
                    if not df.empty:
                        df.columns = list(result.keys())
                    return df
            except Exception as e:
                self.logger.error(f"Query execution error: {e}")
                return pd.DataFrame()
        else:
            self.logger.warning("Cannot execute query: No database connection")
            return pd.DataFrame()
    
    def execute_script(self, script_path):
        """Execute a SQL script file"""
        if not self.engine:
            self.logger.warning("Cannot execute script: No database connection")
            return False
            
        try:
            with open(script_path, 'r') as file:
                script = file.read()
            
            # Split script into individual statements
            statements = script.split(';')
            
            with self.engine.connect() as conn:
                for statement in statements:
                    statement = statement.strip()
                    if statement:
                        conn.execute(text(statement))
                conn.commit()
            
            self.logger.info(f"Successfully executed script: {script_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error executing script {script_path}: {e}")
            return False
    
    def initialize_schema(self):
        """Initialize database schema"""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_path):
            return self.execute_script(schema_path)
        else:
            self.logger.error(f"Schema file not found: {schema_path}")
            return False

# Global instance
db_manager = DatabaseManager()