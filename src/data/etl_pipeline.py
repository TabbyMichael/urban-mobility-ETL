import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.database import DatabaseManager

class ETLPipeline:
    """ETL Pipeline for Urban Mobility Data"""
    
    def __init__(self):
        self.processed_data = {}
        self.db_manager = DatabaseManager()
        
    def extract(self, source: str, data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract data from source
        
        Args:
            source: Data source identifier
            data: Raw data DataFrame
            
        Returns:
            Extracted DataFrame
        """
        print(f"Extracting data from {source}")
        return data.copy()
    
    def transform_taxi_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform NYC taxi data
        
        Args:
            df: Raw taxi data
            
        Returns:
            Transformed taxi data
        """
        if df.empty:
            return df
            
        print("Transforming taxi data...")
        
        # Convert datetime columns
        datetime_columns = ['pickup_datetime', 'dropoff_datetime']
        for col in datetime_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Calculate trip duration
        if 'pickup_datetime' in df.columns and 'dropoff_datetime' in df.columns:
            df['trip_duration_minutes'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60
        
        # Calculate speed (miles per hour)
        if 'trip_distance' in df.columns and 'trip_duration_minutes' in df.columns:
            # Ensure trip_distance is numeric
            df['trip_distance'] = pd.to_numeric(df['trip_distance'], errors='coerce').fillna(0)
            df['speed_mph'] = np.where(
                df['trip_duration_minutes'] > 0,
                df['trip_distance'] / (df['trip_duration_minutes'] / 60),
                0
            )
        
        # Handle missing values and ensure numeric types
        numeric_columns = ['trip_distance', 'fare_amount', 'tip_amount', 'total_amount']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Ensure trip_duration_minutes is also numeric
        if 'trip_duration_minutes' in df.columns:
            df['trip_duration_minutes'] = pd.to_numeric(df['trip_duration_minutes'], errors='coerce').fillna(0)
        
        return df
    
    def transform_uber_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform Uber data
        
        Args:
            df: Raw Uber data
            
        Returns:
            Transformed Uber data
        """
        if df.empty:
            return df
            
        print("Transforming Uber data...")
        
        # Convert numeric columns
        numeric_columns = ['mean_travel_time', 'standard_deviation', 'geometric_mean']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    
    def transform_transit_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform public transit data
        
        Args:
            df: Raw transit data
            
        Returns:
            Transformed transit data
        """
        if df.empty:
            return df
            
        print("Transforming transit data...")
        
        # Convert time columns
        time_columns = ['arrival_time', 'departure_time']
        for col in time_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
    
    def load_to_database(self, data: pd.DataFrame, table_name: str) -> bool:
        """
        Load data to PostgreSQL database
        
        Args:
            data: Processed data
            table_name: Target table name
            
        Returns:
            Success status
        """
        try:
            print(f"Loading data to database table: {table_name}")
            
            # Connect to database
            if not self.db_manager.connect():
                print("Failed to connect to database")
                return False
            
            # Load data
            success = self.db_manager.load_dataframe(data, table_name)
            
            # Close connection
            self.db_manager.close()
            
            return success
        except Exception as e:
            print(f"Error loading data to database: {str(e)}")
            return False
    
    def load(self, data: pd.DataFrame, destination: str) -> bool:
        """
        Load data to destination (database or memory)
        
        Args:
            data: Processed data
            destination: Target destination
            
        Returns:
            Success status
        """
        try:
            print(f"Loading data to {destination}")
            
            # Try to load to database first
            if self.load_to_database(data, destination):
                print(f"Data loaded successfully to database table: {destination}")
                return True
            
            # Fallback to in-memory storage
            self.processed_data[destination] = data
            print(f"Data stored in memory: {destination}")
            
            # Example: Save to CSV
            # data.to_csv(f"{destination}.csv", index=False)
            
            return True
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def run_full_pipeline(self, taxi_data: pd.DataFrame, 
                         uber_data: pd.DataFrame, 
                         transit_data: pd.DataFrame) -> Dict[str, bool]:
        """
        Run the complete ETL pipeline
        
        Args:
            taxi_data: Raw taxi data
            uber_data: Raw Uber data
            transit_data: Raw transit data
            
        Returns:
            Dictionary with pipeline status
        """
        results = {}
        
        # Process taxi data
        extracted_taxi = self.extract("NYC_Taxi", taxi_data)
        transformed_taxi = self.transform_taxi_data(extracted_taxi)
        results['taxi'] = self.load(transformed_taxi, "trips")
        
        # Process Uber data
        extracted_uber = self.extract("Uber", uber_data)
        transformed_uber = self.transform_uber_data(extracted_uber)
        results['uber'] = self.load(transformed_uber, "uber_travel_times")
        
        # Process transit data
        extracted_transit = self.extract("Public_Transit", transit_data)
        transformed_transit = self.transform_transit_data(extracted_transit)
        results['transit'] = self.load(transformed_transit, "mta_status")
        
        return results

# Example usage
if __name__ == "__main__":
    # Create sample data
    taxi_sample = pd.DataFrame({
        'pickup_datetime': ['2025-11-06T10:00:00Z', '2025-11-06T11:00:00Z'],
        'dropoff_datetime': ['2025-11-06T10:30:00Z', '2025-11-06T11:45:00Z'],
        'pickup_location_id': [100, 200],
        'dropoff_location_id': [150, 250],
        'trip_distance': ['5.2', '12.7'],
        'fare_amount': ['15.50', '28.75'],
        'tip_amount': ['3.00', '5.00'],
        'total_amount': ['18.50', '33.75']
    })
    
    uber_sample = pd.DataFrame({
        'source_id': [1001, 1002],
        'dst_id': [2001, 2002],
        'mean_travel_time': ['850', '1200'],
        'standard_deviation': ['120', '180'],
        'geometric_mean': ['820', '1150']
    })
    
    transit_sample = pd.DataFrame({
        'route_id': ['R1', 'R2'],
        'trip_id': ['T1001', 'T1002'],
        'stop_id': ['S5001', 'S5002'],
        'arrival_time': ['2025-11-06T10:15:00Z', '2025-11-06T10:30:00Z'],
        'departure_time': ['2025-11-06T10:16:00Z', '2025-11-06T10:31:00Z']
    })
    
    # Run pipeline
    pipeline = ETLPipeline()
    results = pipeline.run_full_pipeline(taxi_sample, uber_sample, transit_sample)
    
    print("ETL Pipeline Results:")
    for source, success in results.items():
        print(f"  {source}: {'Success' if success else 'Failed'}")