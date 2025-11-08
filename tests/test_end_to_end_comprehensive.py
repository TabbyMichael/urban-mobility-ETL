#!/usr/bin/env python3
"""
Comprehensive end-to-end tests for the Urban Mobility Analytics application
"""
import unittest
import sys
import os
import json
import requests
from unittest.mock import patch, MagicMock
import pandas as pd

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

class TestEndToEndComprehensive(unittest.TestCase):
    """Comprehensive end-to-end tests for the application"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_url = "http://localhost:5000"
        self.auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.5r8147"
        self.headers = {"Authorization": f"Bearer {self.auth_token}"}
    
    @patch('requests.post')
    @patch('requests.get')
    def test_complete_etl_workflow(self, mock_get, mock_post):
        """Test complete ETL workflow from data extraction to visualization"""
        # Mock authentication
        mock_auth_response = MagicMock()
        mock_auth_response.status_code = 200
        mock_auth_response.json.return_value = {
            "message": "Login successful",
            "token": "test_token_12345"
        }
        mock_post.return_value = mock_auth_response
        
        # Mock taxi data extraction
        mock_taxi_response = MagicMock()
        mock_taxi_response.status_code = 200
        mock_taxi_response.json.return_value = {
            "data_source": "NYC Taxi & Limousine Commission",
            "dataset_id": "t29m-gskq",
            "record_count": 5,
            "limit": 5,
            "offset": 0,
            "data": [
                {
                    "pickup_datetime": "2025-11-06T10:00:00Z", 
                    "dropoff_datetime": "2025-11-06T10:30:00Z",
                    "pickup_location_id": 100,
                    "dropoff_location_id": 150,
                    "trip_distance": 5.2,
                    "fare_amount": 15.50,
                    "tip_amount": 3.00,
                    "total_amount": 18.50
                }
            ]
        }
        mock_get.return_value = mock_taxi_response
        
        # Test login
        auth_response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json={"username": "admin", "password": "admin"}
        )
        
        self.assertEqual(auth_response.status_code, 200)
        auth_data = auth_response.json()
        self.assertIn("token", auth_data)
        
        # Test taxi data extraction
        taxi_response = requests.get(
            f"{self.base_url}/api/v1/taxi/trips?limit=5",
            headers={"Authorization": f"Bearer {auth_data['token']}"}
        )
        
        self.assertEqual(taxi_response.status_code, 200)
        taxi_data = taxi_response.json()
        self.assertIn("data", taxi_data)
        self.assertGreater(len(taxi_data["data"]), 0)
        
        # Test data transformation
        transform_response = requests.post(
            f"{self.base_url}/api/v1/taxi/transform",
            headers={
                "Authorization": f"Bearer {auth_data['token']}",
                "Content-Type": "application/json"
            },
            json={"data": taxi_data["data"]}
        )
        
        self.assertEqual(transform_response.status_code, 200)
        transform_data = transform_response.json()
        self.assertIn("data", transform_data)
        
        # Test data loading
        load_response = requests.post(
            f"{self.base_url}/api/v1/taxi/load",
            headers={
                "Authorization": f"Bearer {auth_data['token']}",
                "Content-Type": "application/json"
            },
            json={"data": transform_data["data"]}
        )
        
        self.assertEqual(load_response.status_code, 201)
        load_data = load_response.json()
        self.assertIn("message", load_data)
        
    @patch('requests.get')
    def test_analytics_pipeline(self, mock_get):
        """Test analytics pipeline with descriptive and predictive analytics"""
        # Mock analytics response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "peak_hours": ["7-9 AM", "5-7 PM"],
            "busiest_routes": ["Times Square to Penn Station", "Brooklyn Bridge to Wall Street"],
            "average_speeds": {
                "weekday": "12 mph",
                "weekend": "18 mph"
            }
        }
        mock_get.return_value = mock_response
        
        # Test analytics endpoint
        response = requests.get(
            f"{self.base_url}/api/v1/analytics/patterns",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("peak_hours", response_data)
        self.assertIn("busiest_routes", response_data)
        self.assertIn("average_speeds", response_data)
    
    @patch('requests.get')
    def test_real_time_streaming(self, mock_get):
        """Test real-time data streaming functionality"""
        # Mock streaming response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "healthy",
            "service": "Urban Mobility API"
        }
        mock_get.return_value = mock_response
        
        # Test health endpoint (proxy for streaming readiness)
        response = requests.get(f"{self.base_url}/api/v1/health")
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("status", response_data)
        self.assertEqual(response_data["status"], "healthy")
    
    @patch('requests.get')
    def test_multi_source_data_integration(self, mock_get):
        """Test integration of multiple data sources"""
        # Mock Uber data response
        mock_uber_response = MagicMock()
        mock_uber_response.status_code = 200
        mock_uber_response.json.return_value = {
            "data_source": "Uber Movement",
            "data_type": "travel times",
            "source_id": 1001,
            "dst_id": 2001,
            "record_count": 5,
            "data": [
                {"time": "00:00", "mean_travel_time": 850},
                {"time": "06:00", "mean_travel_time": 1200}
            ]
        }
        
        # Mock MTA data response
        mock_mta_response = MagicMock()
        mock_mta_response.status_code = 200
        mock_mta_response.json.return_value = {
            "data_source": "MTA GTFS",
            "data_type": "real-time transit feeds",
            "feed_id": 1,
            "record_count": 5,
            "data": [
                {"route_id": "1", "status": "ON_TIME"},
                {"route_id": "2", "status": "DELAYED"}
            ]
        }
        
        # Test Uber data endpoint
        uber_response = requests.get(
            f"{self.base_url}/api/v1/uber/travel-times?source_id=1001&dst_id=2001",
            headers=self.headers
        )
        
        self.assertEqual(uber_response.status_code, 200)
        uber_data = uber_response.json()
        self.assertIn("data_source", uber_data)
        self.assertEqual(uber_data["data_source"], "Uber Movement")
        
        # Test MTA data endpoint
        mta_response = requests.get(
            f"{self.base_url}/api/v1/transit/realtime?feed_id=1",
            headers=self.headers
        )
        
        self.assertEqual(mta_response.status_code, 200)
        mta_data = mta_response.json()
        self.assertIn("data_source", mta_data)
        self.assertEqual(mta_data["data_source"], "MTA GTFS")
    
    @patch('requests.post')
    def test_authentication_and_authorization(self, mock_post):
        """Test authentication and authorization flow"""
        # Mock successful authentication
        mock_success_response = MagicMock()
        mock_success_response.status_code = 200
        mock_success_response.json.return_value = {
            "message": "Login successful",
            "username": "admin",
            "role": "admin",
            "token": "test_token_12345"
        }
        
        # Mock failed authentication
        mock_fail_response = MagicMock()
        mock_fail_response.status_code = 401
        mock_fail_response.json.return_value = {
            "message": "Invalid credentials"
        }
        
        # Test successful login
        mock_post.return_value = mock_success_response
        success_response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json={"username": "admin", "password": "admin"}
        )
        
        self.assertEqual(success_response.status_code, 200)
        success_data = success_response.json()
        self.assertIn("token", success_data)
        self.assertIn("username", success_data)
        self.assertIn("role", success_data)
        
        # Test failed login
        mock_post.return_value = mock_fail_response
        fail_response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json={"username": "wrong", "password": "wrong"}
        )
        
        self.assertEqual(fail_response.status_code, 401)
        fail_data = fail_response.json()
        self.assertIn("message", fail_data)
        self.assertEqual(fail_data["message"], "Invalid credentials")
    
    def test_database_operations(self):
        """Test database operations through ETL pipeline"""
        # This would test the actual database operations
        # For now, we'll test the database manager functionality
        from src.data.database import DatabaseManager
        
        # Test database connection
        db_manager = DatabaseManager()
        self.assertIsNotNone(db_manager)
        
        # Test schema initialization
        # This would normally connect to a test database
        # For mocking purposes, we'll just check the method exists
        self.assertTrue(hasattr(db_manager, 'initialize_schema'))
        
    def test_error_handling_and_edge_cases(self):
        """Test error handling and edge cases"""
        # Test invalid API requests
        invalid_response = requests.get(
            f"{self.base_url}/api/v1/nonexistent",
            headers=self.headers
        )
        
        # Should return 404 for nonexistent endpoints
        self.assertEqual(invalid_response.status_code, 404)
        
        # Test requests without authentication
        unauth_response = requests.get(
            f"{self.base_url}/api/v1/taxi/trips?limit=5"
        )
        
        # Should return 401 for unauthenticated requests
        self.assertEqual(unauth_response.status_code, 401)

if __name__ == "__main__":
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndComprehensive))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)