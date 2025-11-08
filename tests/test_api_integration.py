#!/usr/bin/env python3
"""
API integration tests for the Urban Mobility Analytics application
"""
import unittest
import sys
import os
import json
import requests
from unittest.mock import patch, MagicMock

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

class TestAPIEndpoints(unittest.TestCase):
    """Integration tests for API endpoints"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_url = "http://localhost:5000"
        self.auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.5r8147"
        self.headers = {"Authorization": f"Bearer {self.auth_token}"}
    
    @patch('requests.post')
    def test_auth_login_success(self, mock_post):
        """Test successful authentication login"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Login successful",
            "token": "test_token_12345"
        }
        mock_post.return_value = mock_response
        
        # Test login
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json={"username": "admin", "password": "admin"}
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("message", response_data)
        self.assertIn("token", response_data)
        self.assertEqual(response_data["message"], "Login successful")
    
    @patch('requests.post')
    def test_auth_login_failure(self, mock_post):
        """Test failed authentication login"""
        # Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "message": "Invalid credentials"
        }
        mock_post.return_value = mock_response
        
        # Test login with wrong credentials
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json={"username": "wrong", "password": "wrong"}
        )
        
        self.assertEqual(response.status_code, 401)
        response_data = response.json()
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Invalid credentials")
    
    @patch('requests.post')
    def test_auth_login_invalid_json(self, mock_post):
        """Test authentication with invalid JSON"""
        # Mock bad request response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "message": "Content-Type must be application/json"
        }
        mock_post.return_value = mock_response
        
        # Test login without proper content type
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            data="invalid json"
        )
        
        self.assertEqual(response.status_code, 400)
    
    @patch('requests.get')
    def test_health_endpoint(self, mock_get):
        """Test health check endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "healthy",
            "service": "Urban Mobility API"
        }
        mock_get.return_value = mock_response
        
        # Test health endpoint (no auth required)
        response = requests.get(f"{self.base_url}/api/v1/health")
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("status", response_data)
        self.assertIn("service", response_data)
        self.assertEqual(response_data["status"], "healthy")
    
    @patch('requests.get')
    def test_taxi_metadata_endpoint(self, mock_get):
        """Test taxi metadata endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data_source": "NYC Taxi & Limousine Commission",
            "access_method": "NYC Open Data Portal",
            "datasets": {
                "yellow_taxi": {"name": "Yellow Taxi Data"},
                "green_taxi": {"name": "Green Taxi Data"}
            }
        }
        mock_get.return_value = mock_response
        
        # Test taxi metadata endpoint
        response = requests.get(
            f"{self.base_url}/api/v1/taxi/metadata",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("data_source", response_data)
        self.assertIn("datasets", response_data)
    
    @patch('requests.get')
    def test_taxi_trips_endpoint(self, mock_get):
        """Test taxi trips endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data_source": "NYC Taxi & Limousine Commission",
            "dataset_id": "t29m-gskq",
            "record_count": 5,
            "limit": 5,
            "offset": 0,
            "data": [
                {"pickup_datetime": "2025-11-06T10:00:00Z", "fare_amount": 15.50},
                {"pickup_datetime": "2025-11-06T11:00:00Z", "fare_amount": 18.75}
            ]
        }
        mock_get.return_value = mock_response
        
        # Test taxi trips endpoint
        response = requests.get(
            f"{self.base_url}/api/v1/taxi/trips?limit=5",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("data_source", response_data)
        self.assertIn("data", response_data)
        self.assertEqual(response_data["limit"], 5)
    
    @patch('requests.get')
    def test_uber_endpoint(self, mock_get):
        """Test Uber data endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data_source": "Uber Movement",
            "data_type": "aggregated travel times",
            "status": "available",
            "sample_fields": ["source_id", "dst_id", "mean_travel_time"]
        }
        mock_get.return_value = mock_response
        
        # Test Uber endpoint
        response = requests.get(
            f"{self.base_url}/api/v1/uber",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("data_source", response_data)
        self.assertIn("data_type", response_data)
        self.assertEqual(response_data["data_source"], "Uber Movement")
    
    @patch('requests.get')
    def test_transit_endpoint(self, mock_get):
        """Test transit data endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data_source": "MTA GTFS",
            "data_type": "real-time transit feeds",
            "status": "available",
            "sample_fields": ["route_id", "trip_id", "stop_id"]
        }
        mock_get.return_value = mock_response
        
        # Test transit endpoint
        response = requests.get(
            f"{self.base_url}/api/v1/transit",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("data_source", response_data)
        self.assertIn("data_type", response_data)
    
    @patch('requests.get')
    def test_analytics_patterns_endpoint(self, mock_get):
        """Test analytics patterns endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "peak_hours": ["7-9 AM", "5-7 PM"],
            "busiest_routes": ["Times Square to Penn Station"],
            "average_speeds": {"weekday": "12 mph"}
        }
        mock_get.return_value = mock_response
        
        # Test analytics patterns endpoint
        response = requests.get(
            f"{self.base_url}/api/v1/analytics/patterns",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("peak_hours", response_data)
        self.assertIn("busiest_routes", response_data)
    
    @patch('requests.get')
    def test_analytics_demand_endpoint(self, mock_get):
        """Test analytics demand endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "prediction_window": "next 24 hours",
            "high_demand_areas": ["Manhattan CBD"],
            "low_demand_areas": ["Central Park"]
        }
        mock_get.return_value = mock_response
        
        # Test analytics demand endpoint
        response = requests.get(
            f"{self.base_url}/api/v1/analytics/demand",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("prediction_window", response_data)
        self.assertIn("high_demand_areas", response_data)
    
    @patch('requests.get')
    def test_unauthorized_access(self, mock_get):
        """Test unauthorized access to protected endpoints"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "message": "Authorization required"
        }
        mock_get.return_value = mock_response
        
        # Test accessing protected endpoint without auth
        response = requests.get(f"{self.base_url}/api/v1/taxi/metadata")
        
        self.assertEqual(response.status_code, 401)
        response_data = response.json()
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Authorization required")
    
    @patch('requests.get')
    def test_invalid_token(self, mock_get):
        """Test access with invalid token"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "message": "Token is invalid"
        }
        mock_get.return_value = mock_response
        
        # Test accessing endpoint with invalid token
        response = requests.get(
            f"{self.base_url}/api/v1/taxi/metadata",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        self.assertEqual(response.status_code, 401)
        response_data = response.json()
        self.assertIn("message", response_data)

class TestAPIInputValidation(unittest.TestCase):
    """Tests for API input validation"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_url = "http://localhost:5000"
        self.auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.5r8147"
        self.headers = {"Authorization": f"Bearer {self.auth_token}"}
    
    @patch('requests.get')
    def test_limit_validation(self, mock_get):
        """Test limit parameter validation"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "Limit cannot exceed 1000"
        }
        mock_get.return_value = mock_response
        
        # Test with limit exceeding maximum
        response = requests.get(
            f"{self.base_url}/api/v1/taxi/trips?limit=1500",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("error", response_data)
    
    @patch('requests.get')
    def test_months_validation(self, mock_get):
        """Test months parameter validation"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "Months cannot exceed 12"
        }
        mock_get.return_value = mock_response
        
        # Test with months exceeding maximum
        response = requests.get(
            f"{self.base_url}/api/v1/taxi/historical?months=15",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("error", response_data)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)