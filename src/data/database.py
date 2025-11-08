import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

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
            self.engine = create_engine(db_url, echo=False)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.logger.info("Successfully connected to PostgreSQL database")
        except Exception as e:
            self.logger.warning(f"Failed to connect to PostgreSQL: {e}")
            self.logger.info("Using in-memory storage as fallback")
            self.engine = None
    
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
    
    def execute_query(self, query):
        """Execute a SQL query"""
        if self.engine:
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(text(query))
                    return pd.DataFrame(result.fetchall(), columns=result.keys())
            except Exception as e:
                self.logger.error(f"Query execution error: {e}")
                return pd.DataFrame()
        else:
            self.logger.warning("Cannot execute query: No database connection")
            return pd.DataFrame()

# Global instance
db_manager = DatabaseManager()