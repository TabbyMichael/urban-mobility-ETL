from flask import Blueprint, jsonify, request
import pandas as pd
import os
import sys

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.taxi_data import TaxiDataExtractor
from src.data.etl_pipeline import ETLPipeline

api_bp = Blueprint('api', __name__)

# Initialize data extractor and ETL pipeline
taxi_extractor = TaxiDataExtractor()
etl_pipeline = ETLPipeline()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Urban Mobility API"}), 200

@api_bp.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Simple authentication for demo purposes
    # In production, use proper password hashing and database lookup
    if username == 'admin' and password == 'admin':
        return jsonify({
            "message": "Login successful",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.5r8147"  # Mock token
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@api_bp.route('/taxi/metadata', methods=['GET'])
def get_taxi_metadata():
    """Get metadata for NYC TLC datasets"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:
        # Common NYC TLC dataset IDs
        dataset_ids = {
            "yellow_taxi": "t29m-gskq",
            "green_taxi": "gkne-dk5p",
            "fhv_taxi": "9b9u-2p9y"
        }
        
        metadata = {}
        for name, dataset_id in dataset_ids.items():
            metadata[name] = taxi_extractor.get_dataset_metadata(dataset_id)
        
        return jsonify({
            "data_source": "NYC Taxi & Limousine Commission",
            "access_method": "NYC Open Data Portal",
            "datasets": metadata
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/taxi/trips', methods=['GET'])
def get_taxi_trips():
    """Retrieve NYC taxi trip data with filtering options"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:
        # Get query parameters
        dataset_id = request.args.get('dataset_id', 't29m-gskq')  # Default to yellow taxi
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        order = request.args.get('order', 'pickup_datetime DESC')
        
        # Validate limit to prevent abuse
        if limit > 1000:
            return jsonify({"error": "Limit cannot exceed 1000"}), 400
        
        # Extract data
        df = taxi_extractor.extract_taxi_trips(dataset_id, limit, offset)
        
        # Convert to JSON-serializable format
        data = df.to_dict('records') if not df.empty else []
        
        return jsonify({
            "data_source": "NYC Taxi & Limousine Commission",
            "dataset_id": dataset_id,
            "record_count": len(data),
            "limit": limit,
            "offset": offset,
            "data": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/taxi/historical', methods=['GET'])
def get_historical_taxi_data():
    """Retrieve historical NYC taxi data"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:
        # Get query parameters
        dataset_id = request.args.get('dataset_id', 't29m-gskq')
        months = int(request.args.get('months', 1))
        
        # Validate months to prevent abuse
        if months > 12:
            return jsonify({"error": "Months cannot exceed 12"}), 400
        
        # Extract historical data
        df = taxi_extractor.extract_historical_data(dataset_id, months)
        
        # Convert to JSON-serializable format
        data = df.to_dict('records') if not df.empty else []
        
        return jsonify({
            "data_source": "NYC Taxi & Limousine Commission",
            "dataset_id": dataset_id,
            "months_requested": months,
            "record_count": len(data),
            "data": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/taxi/transform', methods=['POST'])
def transform_taxi_data():
    """Transform raw taxi data through ETL pipeline"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json"}), 400
    
    try:
        # Get raw data from request
        raw_data = request.get_json()
        
        if not raw_data or 'data' not in raw_data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate data size to prevent abuse
        if len(raw_data['data']) > 10000:
            return jsonify({"error": "Data size cannot exceed 10,000 records"}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(raw_data['data'])
        
        # Transform data
        transformed_df = etl_pipeline.transform_taxi_data(df)
        
        # Convert back to JSON
        transformed_data = transformed_df.to_dict('records')
        
        return jsonify({
            "message": "Taxi data transformed successfully",
            "record_count": len(transformed_data),
            "data": transformed_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/taxi/load', methods=['POST'])
def load_taxi_data():
    """Load transformed taxi data to warehouse"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json"}), 400
    
    try:
        # Get transformed data from request
        data = request.get_json()
        
        if not data or 'data' not in data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate data size to prevent abuse
        if len(data['data']) > 10000:
            return jsonify({"error": "Data size cannot exceed 10,000 records"}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(data['data'])
        
        # Load data
        success = etl_pipeline.load(df, "taxi_warehouse")
        
        if success:
            return jsonify({
                "message": "Taxi data loaded successfully",
                "record_count": len(df),
                "destination": "taxi_warehouse"
            }), 201
        else:
            return jsonify({"error": "Failed to load data"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/uber', methods=['GET'])
def get_uber_data():
    """Retrieve Uber data"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:
        sample_data = {
            "data_source": "Uber Movement",
            "data_type": "aggregated travel times",
            "access_method": "API",
            "sample_fields": [
                "source_id",
                "dst_id", 
                "mean_travel_time",
                "standard_deviation",
                "geometric_mean"
            ],
            "status": "available",
            "last_updated": "2025-11-06"
        }
        return jsonify(sample_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/transit', methods=['GET'])
def get_transit_data():
    """Retrieve public transit data"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:
        sample_data = {
            "data_source": "MTA GTFS",
            "data_type": "real-time transit feeds",
            "access_method": "GTFS Realtime API",
            "sample_fields": [
                "route_id",
                "trip_id",
                "stop_id",
                "arrival_time",
                "departure_time"
            ],
            "status": "available",
            "last_updated": "2025-11-06"
        }
        return jsonify(sample_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/analytics/patterns', methods=['GET'])
def get_traffic_patterns():
    """Get traffic patterns analysis"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:
        # Placeholder for actual analytics
        patterns = {
            "peak_hours": ["7-9 AM", "5-7 PM"],
            "busiest_routes": ["Times Square to Penn Station", "Brooklyn Bridge to Wall Street"],
            "average_speeds": {
                "weekday": "12 mph",
                "weekend": "18 mph"
            }
        }
        return jsonify(patterns), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/analytics/demand', methods=['GET'])
def predict_ride_demand():
    """Predict ride demand"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:
        # Placeholder for actual prediction model
        demand_forecast = {
            "prediction_window": "next 24 hours",
            "high_demand_areas": ["Manhattan CBD", "LaGuardia Airport", "Times Square"],
            "low_demand_areas": ["Central Park", "Financial District (night)", "Residential Brooklyn"]
        }
        return jsonify(demand_forecast), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500