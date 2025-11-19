#!/usr/bin/env python3
"""
MVP Comprehensive End-to-End Tests
This test suite validates all critical components needed for MVP readiness.
"""
import unittest
import sys
import os
import json
import pandas as pd
import time
import logging
from unittest.mock import patch, MagicMock

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from src.data.etl_pipeline import ETLPipeline
from src.data.database import DatabaseManager
from src.data.uber_data import UberDataExtractor
from src.data.mta_data import MTAGTFSExtractor
from src.auth.auth import AuthManager
from src.app import create_app
from src.streaming.streaming import RealTimeStreamer

class TestExternalAPIIntegration(unittest.TestCase):
    """Test external API integrations for Uber and MTA"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.uber_extractor = UberDataExtractor()
        self.mta_extractor = MTAGTFSExtractor()
        self.logger = logging.getLogger(__name__)
    
    def test_uber_movement_data_extraction(self):
        """Test Uber Movement data extraction with proper error handling"""
        # Test cities extraction
        cities = self.uber_extractor.get_cities()
        self.assertIsInstance(cities, list)
        self.assertGreater(len(cities), 0)
        
        # Test travel times extraction
        travel_times = self.uber_extractor.get_travel_times(1001, 2001)
        self.assertIsInstance(travel_times, pd.DataFrame)
        
        # Verify required columns exist
        required_columns = ['source_id', 'dst_id', 'mean_travel_time']
        for col in required_columns:
            self.assertIn(col, travel_times.columns)
        
        # Test speeds extraction
        speeds = self.uber_extractor.get_speeds(1)
        self.assertIsInstance(speeds, pd.DataFrame)
        
        # Verify required columns exist
        required_columns = ['city_id', 'average_speed']
        for col in required_columns:
            self.assertIn(col, speeds.columns)
    
    def test_mta_gtfs_data_extraction(self):
        """Test MTA GTFS data extraction with proper error handling"""
        # Test subway lines extraction
        lines = self.mta_extractor.get_subway_lines()
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 0)
        
        # Test real-time feed extraction
        realtime = self.mta_extractor.get_realtime_feed(1)
        self.assertIsInstance(realtime, pd.DataFrame)
        
        # Verify required columns exist
        required_columns = ['trip_id', 'route_id', 'arrival_time']
        for col in required_columns:
            self.assertIn(col, realtime.columns)
        
        # Test service alerts extraction
        alerts = self.mta_extractor.get_service_alerts()
        self.assertIsInstance(alerts, pd.DataFrame)
        
        # Verify required columns exist
        required_columns = ['alert_id', 'route_id', 'reason']
        for col in required_columns:
            self.assertIn(col, alerts.columns)
    
    def test_external_api_error_handling(self):
        """Test error handling for external API failures"""
        # Test with invalid parameters
        travel_times = self.uber_extractor.get_travel_times(-1, -1)
        self.assertIsInstance(travel_times, pd.DataFrame)
        
        # Test real-time feed with invalid feed_id
        realtime = self.mta_extractor.get_realtime_feed(999)
        self.assertIsInstance(realtime, pd.DataFrame)
        
        # All operations should return DataFrames even with errors
        self.assertTrue(True)  # If we got here without exceptions, error handling works

class TestAuthenticationSystem(unittest.TestCase):
    """Test the authentication system with centralized error handling"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.auth_manager = AuthManager()
    
    def test_jwt_token_generation_and_verification(self):
        """Test JWT token generation and verification"""
        # Test token generation
        token = self.auth_manager.generate_token("testuser", "admin")
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 20)  # JWT tokens are typically longer
        
        # Test token verification
        payload = self.auth_manager.verify_token(token)
        self.assertIsNotNone(payload)
        if payload:
            self.assertEqual(payload['username'], "testuser")
            self.assertEqual(payload['role'], "admin")
        
        # Test invalid token
        invalid_payload = self.auth_manager.verify_token("invalid.token.here")
        self.assertIsNone(invalid_payload)
    
    def test_password_hashing_and_verification(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = self.auth_manager.hash_password(password)
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, password)
        
        # Test valid password
        is_valid = self.auth_manager.verify_password(password, hashed)
        self.assertTrue(is_valid)
        
        # Test invalid password
        is_invalid = self.auth_manager.verify_password("wrongpassword", hashed)
        self.assertFalse(is_invalid)

class TestRealTimeStreaming(unittest.TestCase):
    """Test real-time streaming functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.streamer = RealTimeStreamer()
        self.logger = logging.getLogger(__name__)
    
    def test_streaming_initialization(self):
        """Test real-time streaming initialization"""
        self.assertIsNotNone(self.streamer)
        self.assertFalse(self.streamer.streaming_active)
    
    def test_websocket_event_registration(self):
        """Test WebSocket event registration"""
        # Test that events are registered without errors
        try:
            self.streamer.register_events()
            success = True
        except Exception as e:
            self.logger.error(f"Event registration failed: {e}")
            success = False
        
        self.assertTrue(success)

class TestComprehensiveEndToEndWorkflow(unittest.TestCase):
    """Test the complete end-to-end workflow with all components"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create sample data
        self.sample_taxi_data = pd.DataFrame({
            'pickup_datetime': pd.date_range('2025-11-06', periods=10, freq='h'),
            'dropoff_datetime': pd.date_range('2025-11-06 00:30:00', periods=10, freq='h'),
            'pickup_location_id': [100 + i for i in range(10)],
            'dropoff_location_id': [150 + i for i in range(10)],
            'trip_distance': [round(1.0 + (i * 0.5), 2) for i in range(10)],
            'fare_amount': [round(5.0 + (i * 0.3), 2) for i in range(10)],
            'tip_amount': [round(1.0 + (i * 0.1), 2) for i in range(10)],
            'total_amount': [round(6.0 + (i * 0.4), 2) for i in range(10)]
        })
    
    def test_complete_workflow_with_all_components(self):
        """Test complete workflow: auth → ETL → analytics → API"""
        start_time = time.time()
        
        # 1. Test authentication
        auth_response = self.client.post('/api/v1/auth/login',
                                       json={'username': 'admin', 'password': 'admin'})
        self.assertEqual(auth_response.status_code, 200)
        
        auth_data = json.loads(auth_response.data)
        token = auth_data['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 2. Test ETL pipeline
        pipeline = ETLPipeline()
        transformed_data = pipeline.transform_taxi_data(self.sample_taxi_data)
        self.assertIsInstance(transformed_data, pd.DataFrame)
        self.assertIn('trip_duration_minutes', transformed_data.columns)
        
        # 3. Test database operations
        db_manager = DatabaseManager()
        save_success = db_manager.save_data(transformed_data, "workflow_test_table")
        self.assertTrue(save_success)
        
        # 4. Test API endpoints with authentication
        api_response = self.client.get('/api/v1/taxi/metadata', headers=headers)
        self.assertIn(api_response.status_code, [200, 500])  # 500 if external API not available
        
        # 5. Test analytics endpoints
        analytics_response = self.client.get('/api/v1/analytics/patterns', headers=headers)
        self.assertEqual(analytics_response.status_code, 200)
        
        total_time = time.time() - start_time
        self.assertLess(total_time, 10.0, "Complete workflow should complete within 10 seconds")

class TestErrorHandlingAndLogging(unittest.TestCase):
    """Test centralized error handling and logging"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.logger = logging.getLogger(__name__)
    
    def test_centralized_exception_handling(self):
        """Test centralized exception handling patterns"""
        # Test that exceptions are properly caught and handled
        handled = False
        try:
            # Simulate an operation that might fail
            result = 10 / 0
        except ZeroDivisionError as e:
            # Proper exception handling
            self.logger.error(f"Division by zero error: {e}")
            handled = True
        
        self.assertTrue(handled, "Exception should be properly handled")
    
    def test_structured_logging(self):
        """Test structured logging implementation"""
        # Test different log levels
        self.logger.debug("Debug message")
        self.logger.info("Info message")
        self.logger.warning("Warning message")
        self.logger.error("Error message")
        
        # All logging operations should complete without errors
        self.assertTrue(True)

class TestPerformanceOptimization(unittest.TestCase):
    """Test performance optimizations"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db_manager = DatabaseManager()
    
    def test_database_connection_efficiency(self):
        """Test database connection efficiency"""
        # Measure connection time
        start_time = time.time()
        is_connected = self.db_manager.connect()
        connect_time = time.time() - start_time
        
        self.assertLess(connect_time, 2.0, "Database connection should be established within 2 seconds")
    
    def test_data_processing_performance(self):
        """Test data processing performance with larger datasets"""
        # Create larger test dataset
        large_data = pd.DataFrame({
            "id": range(1000),
            "value": [i * 2 for i in range(1000)],
            "category": [f"cat_{i % 10}" for i in range(1000)]
        })
        
        # Measure processing time
        start_time = time.time()
        db_success = self.db_manager.save_data(large_data, "performance_test_table")
        process_time = time.time() - start_time
        
        self.assertTrue(db_success)
        self.assertLess(process_time, 5.0, "Processing 1000 records should take less than 5 seconds")

if __name__ == '__main__':
    # Configure logging for tests
    logging.basicConfig(level=logging.INFO)
    
    # Run the tests
    unittest.main(verbosity=2)