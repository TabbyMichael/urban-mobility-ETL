import pandas as pd
import numpy as np
from typing import Dict, List
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.database import DatabaseManager

class DescriptiveAnalytics:
    """Perform descriptive analytics on urban mobility data"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def connect_to_database(self) -> bool:
        """Connect to the database"""
        return self.db_manager.connect()
    
    def close_database(self):
        """Close database connection"""
        self.db_manager.close()
    
    def trip_volume_by_hour(self) -> pd.DataFrame:
        """Get trip volume by hour of day"""
        query = """
            SELECT 
                EXTRACT(HOUR FROM pickup_datetime) as hour,
                COUNT(*) as trip_count
            FROM trips
            WHERE pickup_datetime IS NOT NULL
            GROUP BY EXTRACT(HOUR FROM pickup_datetime)
            ORDER BY hour
        """
        return self.db_manager.execute_query(query)
    
    def trip_volume_by_day(self) -> pd.DataFrame:
        """Get trip volume by day of week"""
        query = """
            SELECT 
                EXTRACT(DOW FROM pickup_datetime) as day_of_week,
                COUNT(*) as trip_count
            FROM trips
            WHERE pickup_datetime IS NOT NULL
            GROUP BY EXTRACT(DOW FROM pickup_datetime)
            ORDER BY day_of_week
        """
        return self.db_manager.execute_query(query)
    
    def peak_pickup_zones(self, limit: int = 10) -> pd.DataFrame:
        """Get peak pickup zones"""
        query = f"""
            SELECT 
                pickup_location_id,
                COUNT(*) as pickup_count
            FROM trips
            WHERE pickup_location_id IS NOT NULL
            GROUP BY pickup_location_id
            ORDER BY pickup_count DESC
            LIMIT {limit}
        """
        return self.db_manager.execute_query(query)
    
    def average_trip_distance_by_borough(self) -> pd.DataFrame:
        """Get average trip distance by borough"""
        query = """
            SELECT 
                z.borough,
                AVG(t.trip_distance) as avg_trip_distance
            FROM trips t
            JOIN zones z ON t.pickup_location_id = z.location_id
            WHERE t.trip_distance IS NOT NULL AND t.trip_distance > 0
            GROUP BY z.borough
            ORDER BY avg_trip_distance DESC
        """
        return self.db_manager.execute_query(query)
    
    def fare_analysis(self) -> pd.DataFrame:
        """Analyze fare patterns"""
        query = """
            SELECT 
                AVG(fare_amount) as avg_fare,
                MIN(fare_amount) as min_fare,
                MAX(fare_amount) as max_fare,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fare_amount) as median_fare
            FROM trips
            WHERE fare_amount IS NOT NULL AND fare_amount >= 0
        """
        return self.db_manager.execute_query(query)
    
    def generate_heatmap_data(self) -> pd.DataFrame:
        """Generate data for heatmap visualization"""
        query = """
            SELECT 
                pickup_location_id,
                COUNT(*) as trip_count,
                AVG(trip_distance) as avg_distance,
                AVG(fare_amount) as avg_fare
            FROM trips
            WHERE pickup_location_id IS NOT NULL
            GROUP BY pickup_location_id
            ORDER BY trip_count DESC
        """
        return self.db_manager.execute_query(query)

# Example usage
if __name__ == "__main__":
    analytics = DescriptiveAnalytics()
    
    if analytics.connect_to_database():
        print("Descriptive Analytics Examples:")
        print("=" * 40)
        
        # Trip volume by hour
        hour_data = analytics.trip_volume_by_hour()
        print("Trip Volume by Hour:")
        print(hour_data.head())
        
        # Peak pickup zones
        peak_zones = analytics.peak_pickup_zones(5)
        print("\nPeak Pickup Zones:")
        print(peak_zones)
        
        analytics.close_database()
    else:
        print("Failed to connect to database")