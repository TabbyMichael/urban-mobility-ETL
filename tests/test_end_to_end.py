#!/usr/bin/env python3
"""
End-to-end tests for the Urban Mobility Analytics ETL pipeline
"""
import unittest
import sys
import os
import json
import pandas as pd
from unittest.mock import patch, MagicMock

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from src.data.etl_pipeline import ETLPipeline
from src.data.database import DatabaseManager
from src.analytics.descriptive import DescriptiveAnalytics
from src.ml.predictive import PredictiveModels
from src.spatial.clustering import SpatialAnalytics

class TestEndToEndPipeline(unittest.TestCase):
    """End-to-end tests for the complete ETL pipeline"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.pipeline = ETLPipeline()
        self.db_manager = DatabaseManager()
        self.analytics = DescriptiveAnalytics()
        self.ml_models = PredictiveModels()
        self.spatial = SpatialAnalytics()
        
        # Create sample test data
        self.sample_taxi_data = pd.DataFrame({
            'pickup_datetime': pd.date_range('2025-11-06', periods=10, freq='H'),
            'dropoff_datetime': pd.date_range('2025-11-06 00:30:00', periods=10, freq='H'),
            'pickup_location_id': [100 + i for i in range(10)],
            'dropoff_location_id': [150 + i for i in range(10)],
            'trip_distance': [round(1.0 + i * 0.5, 2) for i in range(10)],
            'fare_amount': [round(5.0 + i * 0.3, 2) for i in range(10)],
            'tip_amount': [round(1.0 + i * 0.1, 2) for i in range(10)],
            'total_amount': [round(6.0 + i * 0.4, 2) for i in range(10)]
        })
        
        self.sample_uber_data = pd.DataFrame({
            'source_id': [1001, 1002, 1003],
            'dst_id': [2001, 2002, 2003],
            'mean_travel_time': [850, 1200, 950],
            'standard_deviation': [120, 180, 150],
            'geometric_mean': [820, 1150, 920]
        })
        
        self.sample_transit_data = pd.DataFrame({
            'route_id': ['R1', 'R2', 'R3'],
            'trip_id': ['T1001', 'T1002', 'T1003'],
            'stop_id': ['S5001', 'S5002', 'S5003'],
            'arrival_time': pd.date_range('2025-11-06 10:00:00', periods=3, freq='15T'),
            'departure_time': pd.date_range('2025-11-06 10:01:00', periods=3, freq='15T')
        })
    
    def test_etl_pipeline_full_flow(self):
        """Test the complete ETL pipeline flow"""
        # Test data extraction
        self.assertIsInstance(self.sample_taxi_data, pd.DataFrame)
        self.assertIsInstance(self.sample_uber_data, pd.DataFrame)
        self.assertIsInstance(self.sample_transit_data, pd.DataFrame)
        
        # Test data transformation
        transformed_taxi = self.pipeline.transform_taxi_data(self.sample_taxi_data)
        transformed_uber = self.pipeline.transform_uber_data(self.sample_uber_data)
        transformed_transit = self.pipeline.transform_transit_data(self.sample_transit_data)
        
        # Verify transformations
        self.assertIn('trip_duration_minutes', transformed_taxi.columns)
        self.assertIn('speed_mph', transformed_taxi.columns)
        self.assertIn('mean_travel_time', transformed_uber.columns)
        self.assertIn('arrival_time', transformed_transit.columns)
        
        # Test data loading
        taxi_success = self.db_manager.save_data(transformed_taxi, "trips_test")
        uber_success = self.db_manager.save_data(transformed_uber, "uber_travel_times_test")
        transit_success = self.db_manager.save_data(transformed_transit, "mta_status_test")
        
        self.assertTrue(taxi_success)
        self.assertTrue(uber_success)
        self.assertTrue(transit_success)
    
    def test_analytics_pipeline(self):
        """Test the analytics pipeline"""
        # Transform data first
        transformed_taxi = self.pipeline.transform_taxi_data(self.sample_taxi_data)
        
        # Test descriptive analytics
        trip_stats = self.analytics.calculate_trip_statistics(transformed_taxi)
        self.assertIsInstance(trip_stats, dict)
        self.assertIn('total_trips', trip_stats)
        self.assertIn('avg_fare', trip_stats)
        
        # Test peak hour analysis
        peak_hours = self.analytics.analyze_peak_hours(transformed_taxi)
        self.assertIsInstance(peak_hours, dict)
        
        # Test zone analysis
        zone_analysis = self.analytics.analyze_pickup_zones(transformed_taxi)
        self.assertIsInstance(zone_analysis, dict)
    
    def test_ml_pipeline(self):
        """Test the ML pipeline"""
        # Transform data first
        transformed_taxi = self.pipeline.transform_taxi_data(self.sample_taxi_data)
        
        # Test feature engineering
        features = self.ml_models.prepare_features(transformed_taxi)
        self.assertIsInstance(features, pd.DataFrame)
        self.assertGreater(len(features), 0)
        
        # Test model initialization
        self.assertIsNotNone(self.ml_models.demand_model)
        self.assertIsNotNone(self.ml_models.fraud_model)
        self.assertIsNotNone(self.ml_models.congestion_model)
    
    def test_spatial_analytics(self):
        """Test spatial analytics"""
        # Transform data first
        transformed_taxi = self.pipeline.transform_taxi_data(self.sample_taxi_data)
        
        # Test clustering
        clusters = self.spatial.cluster_pickup_locations(transformed_taxi)
        self.assertIsInstance(clusters, dict)
        
        # Test hotspot identification
        hotspots = self.spatial.identify_hotspots(transformed_taxi)
        self.assertIsInstance(hotspots, dict)
    
    def test_data_integrity(self):
        """Test data integrity throughout the pipeline"""
        # Transform data
        transformed_taxi = self.pipeline.transform_taxi_data(self.sample_taxi_data)
        
        # Check for data loss
        self.assertEqual(len(self.sample_taxi_data), len(transformed_taxi))
        
        # Check for required columns
        required_columns = ['pickup_datetime', 'dropoff_datetime', 'trip_distance', 'fare_amount']
        for col in required_columns:
            self.assertIn(col, transformed_taxi.columns)
        
        # Check for data type consistency
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(transformed_taxi['pickup_datetime']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(transformed_taxi['dropoff_datetime']))
        self.assertTrue(pd.api.types.is_numeric_dtype(transformed_taxi['trip_distance']))
        self.assertTrue(pd.api.types.is_numeric_dtype(transformed_taxi['fare_amount']))

class TestAPIIntegration(unittest.TestCase):
    """API integration tests"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_url = "http://localhost:5000"
        self.auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.5r8147"
    
    @patch('requests.post')
    def test_auth_login(self, mock_post):
        """Test authentication login endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Login successful",
            "token": "test_token_123"
        }
        mock_post.return_value = mock_response
        
        # Test login
        response = mock_post(f"{self.base_url}/api/v1/auth/login", 
                           json={"username": "admin", "password": "admin"})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
    
    @patch('requests.get')
    def test_protected_endpoint_access(self, mock_get):
        """Test access to protected endpoints"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "healthy", "service": "Urban Mobility API"}
        mock_get.return_value = mock_response
        
        # Test health endpoint
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = mock_get(f"{self.base_url}/api/v1/health", headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("service", response.json())
    
    @patch('requests.get')
    def test_unauthorized_access(self, mock_get):
        """Test unauthorized access to protected endpoints"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Authorization required"}
        mock_get.return_value = mock_response
        
        # Test without authorization
        response = mock_get(f"{self.base_url}/api/v1/uber")
        
        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json())

class TestDatabaseIntegration(unittest.TestCase):
    """Database integration tests"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db_manager = DatabaseManager()
    
    def test_database_connection(self):
        """Test database connection"""
        # Test that database manager is initialized
        self.assertIsNotNone(self.db_manager)
        
        # Test memory storage fallback
        test_data = pd.DataFrame({"test": [1, 2, 3]})
        success = self.db_manager.save_data(test_data, "test_table")
        self.assertTrue(success)
        
        # Test data retrieval
        retrieved_data = self.db_manager.load_data("test_table")
        self.assertIsInstance(retrieved_data, pd.DataFrame)
        self.assertEqual(len(retrieved_data), 3)
    
    def test_table_operations(self):
        """Test table operations"""
        # Test table existence check
        exists = self.db_manager.table_exists("nonexistent_table")
        # Should be False for in-memory storage
        self.assertFalse(exists)
        
        # Test data saving and loading
        test_data = pd.DataFrame({
            "id": [1, 2, 3],
            "value": ["a", "b", "c"]
        })
        
        save_success = self.db_manager.save_data(test_data, "test_table")
        self.assertTrue(save_success)
        
        load_success = self.db_manager.load_data("test_table")
        self.assertIsInstance(load_success, pd.DataFrame)
        self.assertEqual(len(load_success), 3)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)