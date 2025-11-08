#!/usr/bin/env python3
"""
Run the ETL pipeline to process urban mobility data
"""
import sys
import os
import pandas as pd

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.etl_pipeline import ETLPipeline
from src.data.taxi_data import TaxiDataExtractor
from src.data.database import db_manager

def run_etl_pipeline():
    """Run the complete ETL pipeline"""
    print("Starting ETL Pipeline...")
    
    # Initialize pipeline
    pipeline = ETLPipeline()
    
    # Initialize data extractor
    extractor = TaxiDataExtractor()
    
    # Extract sample taxi data
    print("Extracting sample taxi data...")
    try:
        taxi_data = extractor.extract_taxi_trips(limit=100)
        print(f"Extracted {len(taxi_data)} taxi records")
    except Exception as e:
        print(f"Error extracting taxi data: {str(e)}")
        # Create sample data if extraction fails
        taxi_data = pd.DataFrame({
            'pickup_datetime': pd.date_range('2025-11-06', periods=100, freq='H'),
            'dropoff_datetime': pd.date_range('2025-11-06 00:30:00', periods=100, freq='H'),
            'pickup_location_id': [100 + i % 50 for i in range(100)],
            'dropoff_location_id': [150 + i % 50 for i in range(100)],
            'trip_distance': [round(1.0 + i * 0.5 % 10, 2) for i in range(100)],
            'fare_amount': [round(5.0 + i * 0.3 % 20, 2) for i in range(100)],
            'tip_amount': [round(1.0 + i * 0.1 % 5, 2) for i in range(100)],
            'total_amount': [round(6.0 + i * 0.4 % 25, 2) for i in range(100)]
        })
        print("Using sample data for demonstration")
    
    # Create sample Uber and transit data
    print("Creating sample Uber data...")
    uber_data = pd.DataFrame({
        'source_id': [1001, 1002, 1003, 1004, 1005] * 20,
        'dst_id': [2001, 2002, 2003, 2004, 2005] * 20,
        'mean_travel_time': [850 + i % 200 for i in range(100)],
        'standard_deviation': [120 + i % 50 for i in range(100)],
        'geometric_mean': [820 + i % 180 for i in range(100)]
    })
    
    print("Creating sample transit data...")
    transit_data = pd.DataFrame({
        'route_id': ['R1', 'R2', 'R3', 'R4', 'R5'] * 20,
        'trip_id': [f'T{i}' for i in range(100)],
        'stop_id': [f'S{i}' for i in range(100)],
        'arrival_time': pd.date_range('2025-11-06 08:00:00', periods=100, freq='15min'),
        'departure_time': pd.date_range('2025-11-06 08:01:00', periods=100, freq='15min')
    })
    
    # Transform data
    print("Transforming data...")
    transformed_taxi = pipeline.transform_taxi_data(taxi_data)
    transformed_uber = pipeline.transform_uber_data(uber_data)
    transformed_transit = pipeline.transform_transit_data(transit_data)
    
    # Load data
    print("Loading data...")
    taxi_success = db_manager.save_data(transformed_taxi, "trips")
    uber_success = db_manager.save_data(transformed_uber, "uber_travel_times")
    transit_success = db_manager.save_data(transformed_transit, "mta_status")
    
    print("ETL Pipeline Results:")
    print(f"  Taxi data: {'Success' if taxi_success else 'Failed'}")
    print(f"  Uber data: {'Success' if uber_success else 'Failed'}")
    print(f"  Transit data: {'Success' if transit_success else 'Failed'}")
    
    return {
        'taxi': transformed_taxi,
        'uber': transformed_uber,
        'transit': transformed_transit
    }

if __name__ == "__main__":
    try:
        data = run_etl_pipeline()
        print("\nETL pipeline completed successfully!")
        print(f"Processed {len(data['taxi'])} taxi records")
        print(f"Processed {len(data['uber'])} Uber records")
        print(f"Processed {len(data['transit'])} transit records")
    except Exception as e:
        print(f"Error running ETL pipeline: {str(e)}")
        sys.exit(1)