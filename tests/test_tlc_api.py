#!/usr/bin/env python3
"""
Test script for the NYC TLC API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_taxi_metadata():
    """Test the taxi metadata endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/taxi/metadata")
        print(f"Taxi Metadata: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Taxi Metadata Error: {str(e)}")

def test_taxi_trips():
    """Test the taxi trips endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/taxi/trips?limit=5")
        print(f"\nTaxi Trips: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Taxi Trips Error: {str(e)}")

def test_historical_taxi_data():
    """Test the historical taxi data endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/taxi/historical?months=1")
        print(f"\nHistorical Taxi Data: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Historical Taxi Data Error: {str(e)}")

def test_transform_taxi_data():
    """Test the transform taxi data endpoint"""
    try:
        # Sample data to transform
        sample_data = {
            "data": [
                {
                    "pickup_datetime": "2025-11-06T10:00:00Z",
                    "dropoff_datetime": "2025-11-06T10:30:00Z",
                    "pickup_location_id": 100,
                    "dropoff_location_id": 150,
                    "trip_distance": "5.2",
                    "fare_amount": "15.50",
                    "tip_amount": "3.00",
                    "total_amount": "18.50"
                }
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/taxi/transform",
            json=sample_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"\nTransform Taxi Data: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Transform Taxi Data Error: {str(e)}")

if __name__ == "__main__":
    print("Testing NYC TLC API Endpoints")
    print("=" * 40)
    
    test_taxi_metadata()
    test_taxi_trips()
    test_historical_taxi_data()
    test_transform_taxi_data()