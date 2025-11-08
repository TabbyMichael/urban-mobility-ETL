import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from typing import Dict, List, Tuple
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.database import DatabaseManager

class SpatialAnalytics:
    """Spatial analytics for urban mobility data"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.dbscan_model = None
    
    def connect_to_database(self) -> bool:
        """Connect to the database"""
        return self.db_manager.connect()
    
    def close_database(self):
        """Close database connection"""
        self.db_manager.close()
    
    def get_pickup_locations(self) -> pd.DataFrame:
        """Get pickup locations for clustering"""
        query = """
            SELECT 
                pickup_location_id,
                ST_X(pickup_geom) as longitude,
                ST_Y(pickup_geom) as latitude
            FROM trips
            WHERE pickup_geom IS NOT NULL
        """
        return self.db_manager.execute_query(query)
    
    def cluster_pickup_hotspots(self, eps: float = 0.01, min_samples: int = 10) -> Dict:
        """Cluster pickup hotspots using DBSCAN"""
        try:
            # Get pickup locations
            locations = self.get_pickup_locations()
            
            if locations.empty:
                return {"status": "failed", "message": "No location data available"}
            
            # Prepare coordinates for clustering
            coordinates = locations[['longitude', 'latitude']].values
            
            # Apply DBSCAN clustering
            self.dbscan_model = DBSCAN(eps=eps, min_samples=min_samples)
            cluster_labels = self.dbscan_model.fit_predict(coordinates)
            
            # Add cluster labels to dataframe
            locations['cluster'] = cluster_labels
            
            # Calculate cluster statistics
            cluster_stats = locations.groupby('cluster').agg({
                'longitude': ['mean', 'count'],
                'latitude': 'mean'
            }).round(6)
            
            # Flatten column names
            cluster_stats.columns = ['center_longitude', 'count', 'center_latitude']
            cluster_stats = cluster_stats.reset_index()
            
            # Identify noise points (label -1)
            noise_points = sum(cluster_labels == -1)
            
            return {
                "status": "success",
                "cluster_count": len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0),
                "noise_points": noise_points,
                "clusters": cluster_stats.to_dict('records')
            }
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def find_optimal_routes(self, source_id: int, destination_id: int) -> Dict:
        """Find optimal routes using network analysis"""
        # In a real implementation, this would integrate with osmnx and networkx
        # For now, we'll return sample data
        
        # Sample route data
        sample_routes = [
            {
                "route_id": "route_1",
                "distance": 5.2,
                "estimated_time": 15,
                "traffic_level": "low"
            },
            {
                "route_id": "route_2",
                "distance": 6.1,
                "estimated_time": 18,
                "traffic_level": "medium"
            },
            {
                "route_id": "route_3",
                "distance": 4.8,
                "estimated_time": 20,
                "traffic_level": "high"
            }
        ]
        
        # Find the optimal route (shortest time)
        optimal_route = min(sample_routes, key=lambda x: x['estimated_time'])
        
        return {
            "status": "success",
            "optimal_route": optimal_route,
            "alternative_routes": [r for r in sample_routes if r != optimal_route]
        }
    
    def analyze_surge_pricing_zones(self) -> pd.DataFrame:
        """Analyze zones with surge pricing patterns"""
        query = """
            SELECT 
                pickup_location_id,
                COUNT(*) as trip_count,
                AVG(fare_amount) as avg_fare,
                AVG(tip_amount) as avg_tip,
                (AVG(fare_amount) / AVG(trip_distance)) as fare_per_mile
            FROM trips
            WHERE fare_amount IS NOT NULL 
                AND trip_distance IS NOT NULL 
                AND trip_distance > 0
            GROUP BY pickup_location_id
            HAVING COUNT(*) >= 10
            ORDER BY fare_per_mile DESC
            LIMIT 20
        """
        return self.db_manager.execute_query(query)

# Example usage
if __name__ == "__main__":
    spatial_analytics = SpatialAnalytics()
    
    if spatial_analytics.connect_to_database():
        print("Spatial Analytics Examples:")
        print("=" * 40)
        
        # Cluster pickup hotspots
        print("Clustering pickup hotspots...")
        result = spatial_analytics.cluster_pickup_hotspots()
        print(f"Clustering result: {result}")
        
        # Analyze surge pricing zones
        print("\nAnalyzing surge pricing zones...")
        surge_zones = spatial_analytics.analyze_surge_pricing_zones()
        print(f"Top surge pricing zones:")
        print(surge_zones.head())
        
        spatial_analytics.close_database()
    else:
        print("Failed to connect to database")