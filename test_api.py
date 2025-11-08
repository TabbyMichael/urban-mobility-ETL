#!/usr/bin/env python3
"""
Test script for the Urban Mobility API
"""
import requests
import json
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:5000"

def get_auth_token():
    """Get authentication token"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json={"username": "admin", "password": "admin"}
        )
        if response.status_code == 200:
            return response.json().get("token")
        else:
            print(f"Failed to get auth token: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting auth token: {str(e)}")
        return None

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Health Check: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Health Check Error: {str(e)}")
        return False

def test_auth_login():
    """Test the authentication login endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json={"username": "admin", "password": "admin"}
        )
        print(f"Auth Login: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Auth Login Error: {str(e)}")
        return False

def test_taxi_data(token):
    """Test the taxi data endpoint"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/taxi/trips?limit=5", headers=headers)
        print(f"\nTaxi Data: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Taxi Data Error: {str(e)}")
        return False

def test_uber_data(token):
    """Test the Uber data endpoint"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/uber", headers=headers)
        print(f"\nUber Data: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Uber Data Error: {str(e)}")
        return False

def test_transit_data(token):
    """Test the transit data endpoint"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/transit", headers=headers)
        print(f"\nTransit Data: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Transit Data Error: {str(e)}")
        return False

def test_analytics_patterns(token):
    """Test the traffic patterns endpoint"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/analytics/patterns", headers=headers)
        print(f"\nTraffic Patterns: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Traffic Patterns Error: {str(e)}")
        return False

def test_analytics_demand(token):
    """Test the ride demand endpoint"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/analytics/demand", headers=headers)
        print(f"\nRide Demand: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Ride Demand Error: {str(e)}")
        return False

def test_input_validation(token):
    """Test input validation"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test limit validation
        response = requests.get(f"{BASE_URL}/api/v1/taxi/trips?limit=1500", headers=headers)
        print(f"\nLimit Validation: {response.status_code}")
        if response.status_code == 400:
            print("✓ Limit validation working correctly")
            limit_validation = True
        else:
            print("✗ Limit validation not working")
            limit_validation = False
        
        # Test unauthorized access
        response = requests.get(f"{BASE_URL}/api/v1/uber")
        print(f"\nUnauthorized Access: {response.status_code}")
        if response.status_code == 401:
            print("✓ Unauthorized access properly rejected")
            auth_validation = True
        else:
            print("✗ Unauthorized access not properly rejected")
            auth_validation = False
        
        return limit_validation and auth_validation
    except Exception as e:
        print(f"Input Validation Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Urban Mobility API Endpoints")
    print("=" * 40)
    
    # Test health check (no auth required)
    health_success = test_health_check()
    
    # Test authentication
    auth_success = test_auth_login()
    
    # Get auth token for protected endpoints
    token = get_auth_token()
    if not token:
        print("Failed to get authentication token, skipping protected endpoint tests")
        sys.exit(1)
    
    # Test protected endpoints
    taxi_success = test_taxi_data(token)
    uber_success = test_uber_data(token)
    transit_success = test_transit_data(token)
    patterns_success = test_analytics_patterns(token)
    demand_success = test_analytics_demand(token)
    
    # Test input validation
    validation_success = test_input_validation(token)
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    print(f"Health Check: {'✓ PASS' if health_success else '✗ FAIL'}")
    print(f"Auth Login: {'✓ PASS' if auth_success else '✗ FAIL'}")
    print(f"Taxi Data: {'✓ PASS' if taxi_success else '✗ FAIL'}")
    print(f"Uber Data: {'✓ PASS' if uber_success else '✗ FAIL'}")
    print(f"Transit Data: {'✓ PASS' if transit_success else '✗ FAIL'}")
    print(f"Traffic Patterns: {'✓ PASS' if patterns_success else '✗ FAIL'}")
    print(f"Ride Demand: {'✓ PASS' if demand_success else '✗ FAIL'}")
    print(f"Input Validation: {'✓ PASS' if validation_success else '✗ FAIL'}")
    
    # Overall result
    all_tests = [
        health_success, auth_success, taxi_success, uber_success, 
        transit_success, patterns_success, demand_success, validation_success
    ]
    
    if all(all_tests):
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {len([t for t in all_tests if not t])} test(s) failed")
        sys.exit(1)