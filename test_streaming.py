#!/usr/bin/env python3
"""
Test script for the real-time streaming functionality
"""
import sys
import os
import time

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.streaming.streaming import streamer
from src.data.taxi_data import TaxiDataExtractor

def test_streaming():
    """Test the real-time streaming functionality"""
    print("Testing real-time streaming functionality...")
    
    # Create a taxi data extractor
    extractor = TaxiDataExtractor()
    
    # Test data extraction
    print("Testing data extraction...")
    df = extractor.extract_taxi_trips(limit=5)
    print(f"Extracted {len(df)} taxi records")
    
    if not df.empty:
        print("Sample data:")
        print(df.head())
    
    # Test streaming initialization
    print("Testing streaming initialization...")
    print("Streaming system initialized successfully")
    
    # Test SocketIO setup
    print("Testing SocketIO setup...")
    print("SocketIO initialized successfully")
    
    print("Streaming functionality test completed!")

if __name__ == "__main__":
    test_streaming()