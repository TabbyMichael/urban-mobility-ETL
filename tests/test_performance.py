#!/usr/bin/env python3
"""
Performance and load tests for the Urban Mobility Analytics application
"""
import unittest
import sys
import os
import time
import pandas as pd
import threading
from concurrent.futures import ThreadPoolExecutor
import psutil
import gc

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from src.data.etl_pipeline import ETLPipeline
from src.data.database import DatabaseManager
from src.analytics.descriptive import DescriptiveAnalytics

class TestPerformance(unittest.TestCase):
    """Performance tests for the application components"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.pipeline = ETLPipeline()
        self.db_manager = DatabaseManager()
        self.analytics = DescriptiveAnalytics()
        
        # Create larger sample data for performance testing
        self.large_taxi_data = pd.DataFrame({
            'pickup_datetime': pd.date_range('2025-11-06', periods=10000, freq='H'),
            'dropoff_datetime': pd.date_range('2025-11-06 00:30:00', periods=10000, freq='H'),
            'pickup_location_id': [100 + (i % 100) for i in range(10000)],
            'dropoff_location_id': [150 + (i % 100) for i in range(10000)],
            'trip_distance': [round(1.0 + (i * 0.5) % 20, 2) for i in range(10000)],
            'fare_amount': [round(5.0 + (i * 0.3) % 50, 2) for i in range(10000)],
            'tip_amount': [round(1.0 + (i * 0.1) % 10, 2) for i in range(10000)],
            'total_amount': [round(6.0 + (i * 0.4) % 60, 2) for i in range(10000)]
        })
    
    def test_etl_pipeline_performance(self):
        """Test ETL pipeline performance with large datasets"""
        # Measure transformation time
        start_time = time.time()
        transformed_data = self.pipeline.transform_taxi_data(self.large_taxi_data)
        end_time = time.time()
        
        processing_time = end_time - start_time
        records_per_second = len(self.large_taxi_data) / processing_time
        
        print(f"ETL Pipeline Performance:")
        print(f"  Records processed: {len(self.large_taxi_data)}")
        print(f"  Processing time: {processing_time:.2f} seconds")
        print(f"  Records per second: {records_per_second:.2f}")
        
        # Assert performance requirements (adjust as needed)
        self.assertLess(processing_time, 30.0)  # Should process 10k records in under 30 seconds
        self.assertGreater(records_per_second, 100)  # Should process at least 100 records/second
        
        # Verify data integrity
        self.assertEqual(len(transformed_data), len(self.large_taxi_data))
        self.assertIn('trip_duration_minutes', transformed_data.columns)
        self.assertIn('speed_mph', transformed_data.columns)
    
    def test_database_performance(self):
        """Test database operations performance"""
        # Measure save time
        start_time = time.time()
        save_success = self.db_manager.save_data(self.large_taxi_data, "performance_test")
        end_time = time.time()
        
        save_time = end_time - start_time
        
        print(f"Database Performance:")
        print(f"  Records saved: {len(self.large_taxi_data)}")
        print(f"  Save time: {save_time:.2f} seconds")
        
        # Assert performance requirements
        self.assertTrue(save_success)
        self.assertLess(save_time, 10.0)  # Should save 10k records in under 10 seconds
        
        # Measure load time
        start_time = time.time()
        loaded_data = self.db_manager.load_data("performance_test")
        end_time = time.time()
        
        load_time = end_time - start_time
        
        print(f"  Records loaded: {len(loaded_data)}")
        print(f"  Load time: {load_time:.2f} seconds")
        
        # Assert performance requirements
        self.assertEqual(len(loaded_data), len(self.large_taxi_data))
        self.assertLess(load_time, 5.0)  # Should load 10k records in under 5 seconds
    
    def test_analytics_performance(self):
        """Test analytics performance"""
        # Transform data first
        transformed_data = self.pipeline.transform_taxi_data(self.large_taxi_data)
        
        # Measure trip statistics calculation time
        start_time = time.time()
        trip_stats = self.analytics.calculate_trip_statistics(transformed_data)
        end_time = time.time()
        
        stats_time = end_time - start_time
        
        print(f"Analytics Performance:")
        print(f"  Trip statistics calculation time: {stats_time:.2f} seconds")
        
        # Assert performance requirements
        self.assertIsInstance(trip_stats, dict)
        self.assertLess(stats_time, 5.0)  # Should calculate stats in under 5 seconds
        
        # Measure peak hours analysis time
        start_time = time.time()
        peak_hours = self.analytics.analyze_peak_hours(transformed_data)
        end_time = time.time()
        
        peak_time = end_time - start_time
        
        print(f"  Peak hours analysis time: {peak_time:.2f} seconds")
        
        # Assert performance requirements
        self.assertIsInstance(peak_hours, dict)
        self.assertLess(peak_time, 5.0)  # Should analyze peak hours in under 5 seconds

class TestMemoryUsage(unittest.TestCase):
    """Memory usage tests"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.pipeline = ETLPipeline()
        
        # Create test data
        self.test_data = pd.DataFrame({
            'pickup_datetime': pd.date_range('2025-11-06', periods=1000, freq='H'),
            'dropoff_datetime': pd.date_range('2025-11-06 00:30:00', periods=1000, freq='H'),
            'pickup_location_id': [100 + (i % 50) for i in range(1000)],
            'dropoff_location_id': [150 + (i % 50) for i in range(1000)],
            'trip_distance': [round(1.0 + (i * 0.5) % 10, 2) for i in range(1000)],
            'fare_amount': [round(5.0 + (i * 0.3) % 25, 2) for i in range(1000)],
            'tip_amount': [round(1.0 + (i * 0.1) % 5, 2) for i in range(1000)],
            'total_amount': [round(6.0 + (i * 0.4) % 30, 2) for i in range(1000)]
        })
    
    def test_memory_leaks(self):
        """Test for memory leaks in repeated operations"""
        # Get initial memory usage
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Perform repeated operations
        for i in range(100):
            transformed_data = self.pipeline.transform_taxi_data(self.test_data)
            # Force garbage collection
            gc.collect()
        
        # Get final memory usage
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Memory Usage Test:")
        print(f"  Initial memory: {initial_memory:.2f} MB")
        print(f"  Final memory: {final_memory:.2f} MB")
        print(f"  Memory increase: {memory_increase:.2f} MB")
        
        # Assert memory usage is reasonable (less than 10MB increase for 100 operations)
        self.assertLess(memory_increase, 10.0)

class TestConcurrency(unittest.TestCase):
    """Concurrency tests"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.pipeline = ETLPipeline()
        
        # Create test data
        self.test_data = pd.DataFrame({
            'pickup_datetime': pd.date_range('2025-11-06', periods=100, freq='H'),
            'dropoff_datetime': pd.date_range('2025-11-06 00:30:00', periods=100, freq='H'),
            'pickup_location_id': [100 + (i % 10) for i in range(100)],
            'dropoff_location_id': [150 + (i % 10) for i in range(100)],
            'trip_distance': [round(1.0 + (i * 0.5) % 5, 2) for i in range(100)],
            'fare_amount': [round(5.0 + (i * 0.3) % 15, 2) for i in range(100)],
            'tip_amount': [round(1.0 + (i * 0.1) % 3, 2) for i in range(100)],
            'total_amount': [round(6.0 + (i * 0.4) % 18, 2) for i in range(100)]
        })
    
    def test_concurrent_transformations(self):
        """Test concurrent data transformations"""
        def transform_data():
            return self.pipeline.transform_taxi_data(self.test_data)
        
        # Measure time for sequential processing
        start_time = time.time()
        for _ in range(10):
            result = transform_data()
        sequential_time = time.time() - start_time
        
        # Measure time for concurrent processing
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(transform_data) for _ in range(10)]
            results = [future.result() for future in futures]
        concurrent_time = time.time() - start_time
        
        print(f"Concurrency Test:")
        print(f"  Sequential processing time: {sequential_time:.2f} seconds")
        print(f"  Concurrent processing time: {concurrent_time:.2f} seconds")
        print(f"  Speedup: {sequential_time / concurrent_time:.2f}x")
        
        # Verify all results are correct
        for result in results:
            self.assertEqual(len(result), len(self.test_data))
            self.assertIn('trip_duration_minutes', result.columns)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)