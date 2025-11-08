from flask import Blueprint, jsonify, request, g
import pandas as pd
import os
import sys

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.taxi_data import TaxiDataExtractor
from src.data.uber_data import UberDataExtractor
from src.data.mta_data import MTAGTFSExtractor
from src.data.etl_pipeline import ETLPipeline
from src.auth.auth import auth_manager
from src.monitoring.health import health_checker
from src.utils.exception_handler import handle_exceptions, handle_validation_errors
from src.utils.rate_limiter import rate_limit

api_bp = Blueprint('api', __name__)

# Initialize data extractors and ETL pipeline
taxi_extractor = TaxiDataExtractor()
uber_extractor = UberDataExtractor()
mta_extractor = MTAGTFSExtractor()
etl_pipeline = ETLPipeline()

def require_auth(role=None):
    """Decorator to require authentication and optional role check"""
    def decorator(f):
        @handle_exceptions
        def wrapper(*args, **kwargs):
            # Check for authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"message": "Authorization required"}), 401
            
            # Extract token
            token = auth_header.split(' ')[1]
            
            # Verify token
            payload = auth_manager.verify_token(token)
            if not payload:
                return jsonify({"message": "Invalid or expired token"}), 401
            
            # Check role if specified
            if role and payload.get('role') != role and payload.get('role') != 'admin':
                return jsonify({"message": "Insufficient permissions"}), 403
            
            # Store user info in g object
            g.current_user = payload
            
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@api_bp.route('/health', methods=['GET'])
@handle_exceptions
@rate_limit(max_requests=50, window_seconds=60)
def health_check():
    """Health check endpoint"""
    return jsonify(health_checker.get_system_health()), 200

@api_bp.route('/health/database', methods=['GET'])
@handle_exceptions
@rate_limit(max_requests=50, window_seconds=60)
def database_health_check():
    """Database-specific health check endpoint"""
    return jsonify(health_checker.check_database_health()), 200

@api_bp.route('/health/auth', methods=['GET'])
@handle_exceptions
@rate_limit(max_requests=50, window_seconds=60)
def auth_health_check():
    """Authentication-specific health check endpoint"""
    return jsonify(health_checker.check_auth_health()), 200

@api_bp.route('/auth/login', methods=['POST'])
@handle_validation_errors
@rate_limit(max_requests=20, window_seconds=60)
def login():
    """User login endpoint"""
    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        raise ValueError("Username and password are required")
    
    # Authenticate user
    auth_result = auth_manager.authenticate_user(username, password)
    if auth_result:
        return jsonify({
            "message": "Login successful",
            "username": auth_result["username"],
            "role": auth_result["role"],
            "token": auth_result["token"]
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@api_bp.route('/taxi/metadata', methods=['GET'])
@require_auth()
@handle_exceptions
@rate_limit(max_requests=100, window_seconds=60)
def get_taxi_metadata():
    """Get metadata for NYC TLC datasets"""
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

@api_bp.route('/taxi/trips', methods=['GET'])
@require_auth()
@handle_validation_errors
@rate_limit(max_requests=50, window_seconds=60)
def get_taxi_trips():
    """Retrieve NYC taxi trip data with filtering options"""
    # Get query parameters
    dataset_id = request.args.get('dataset_id', 't29m-gskq')  # Default to yellow taxi
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    order = request.args.get('order', 'pickup_datetime DESC')
    
    # Validate limit to prevent abuse
    if limit > 1000:
        raise ValueError("Limit cannot exceed 1000")
    
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

@api_bp.route('/taxi/historical', methods=['GET'])
@require_auth()
@handle_validation_errors
@rate_limit(max_requests=30, window_seconds=60)
def get_historical_taxi_data():
    """Retrieve historical NYC taxi data"""
    # Get query parameters
    dataset_id = request.args.get('dataset_id', 't29m-gskq')
    months = int(request.args.get('months', 1))
    
    # Validate months to prevent abuse
    if months > 12:
        raise ValueError("Months cannot exceed 12")
    
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

@api_bp.route('/taxi/transform', methods=['POST'])
@require_auth()
@handle_validation_errors
@rate_limit(max_requests=20, window_seconds=60)
def transform_taxi_data():
    """Transform raw taxi data through ETL pipeline"""
    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json"}), 400
    
    # Get raw data from request
    raw_data = request.get_json()
    
    if not raw_data or 'data' not in raw_data:
        raise ValueError("No data provided")
    
    # Validate data size to prevent abuse
    if len(raw_data['data']) > 10000:
        raise ValueError("Data size cannot exceed 10,000 records")
    
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

@api_bp.route('/taxi/load', methods=['POST'])
@require_auth()
@handle_validation_errors
@rate_limit(max_requests=10, window_seconds=60)
def load_taxi_data():
    """Load transformed taxi data to warehouse"""
    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json"}), 400
    
    # Get transformed data from request
    data = request.get_json()
    
    if not data or 'data' not in data:
        raise ValueError("No data provided")
    
    # Validate data size to prevent abuse
    if len(data['data']) > 10000:
        raise ValueError("Data size cannot exceed 10,000 records")
    
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

@api_bp.route('/uber/travel-times', methods=['GET'])
@require_auth()
@handle_validation_errors
@rate_limit(max_requests=50, window_seconds=60)
def get_uber_travel_times():
    """Retrieve Uber travel times data"""
    # Get query parameters
    source_id = int(request.args.get('source_id', 1001))
    dst_id = int(request.args.get('dst_id', 2001))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Extract data
    df = uber_extractor.get_travel_times(source_id, dst_id, start_date, end_date)
    
    # Convert to JSON-serializable format
    data = df.to_dict('records') if not df.empty else []
    
    return jsonify({
        "data_source": "Uber Movement",
        "data_type": "travel times",
        "source_id": source_id,
        "dst_id": dst_id,
        "record_count": len(data),
        "data": data
    }), 200

@api_bp.route('/uber/speeds', methods=['GET'])
@require_auth()
@handle_validation_errors
@rate_limit(max_requests=50, window_seconds=60)
def get_uber_speeds():
    """Retrieve Uber speed data"""
    # Get query parameters
    city_id = int(request.args.get('city_id', 1))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Extract data
    df = uber_extractor.get_speeds(city_id, start_date, end_date)
    
    # Convert to JSON-serializable format
    data = df.to_dict('records') if not df.empty else []
    
    return jsonify({
        "data_source": "Uber Movement",
        "data_type": "speeds",
        "city_id": city_id,
        "record_count": len(data),
        "data": data
    }), 200

@api_bp.route('/transit/realtime', methods=['GET'])
@require_auth()
@handle_validation_errors
@rate_limit(max_requests=50, window_seconds=60)
def get_transit_realtime():
    """Retrieve real-time transit data"""
    # Get query parameters
    feed_id = int(request.args.get('feed_id', 1))
    
    # Extract data
    df = mta_extractor.get_realtime_feed(feed_id)
    
    # Convert to JSON-serializable format
    data = df.to_dict('records') if not df.empty else []
    
    return jsonify({
        "data_source": "MTA GTFS",
        "data_type": "real-time transit feeds",
        "feed_id": feed_id,
        "record_count": len(data),
        "data": data
    }), 200

@api_bp.route('/transit/alerts', methods=['GET'])
@require_auth()
@handle_exceptions
@rate_limit(max_requests=50, window_seconds=60)
def get_transit_alerts():
    """Retrieve transit service alerts"""
    # Extract data
    df = mta_extractor.get_service_alerts()
    
    # Convert to JSON-serializable format
    data = df.to_dict('records') if not df.empty else []
    
    return jsonify({
        "data_source": "MTA GTFS",
        "data_type": "service alerts",
        "record_count": len(data),
        "data": data
    }), 200

@api_bp.route('/analytics/patterns', methods=['GET'])
@require_auth()
@handle_exceptions
@rate_limit(max_requests=30, window_seconds=60)
def get_traffic_patterns():
    """Get traffic patterns analysis"""
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

@api_bp.route('/analytics/demand', methods=['GET'])
@require_auth()
@handle_exceptions
@rate_limit(max_requests=30, window_seconds=60)
def predict_ride_demand():
    """Predict ride demand"""
    # Placeholder for actual prediction model
    demand_forecast = {
        "prediction_window": "next 24 hours",
        "high_demand_areas": ["Manhattan CBD", "LaGuardia Airport", "Times Square"],
        "low_demand_areas": ["Central Park", "Financial District (night)", "Residential Brooklyn"]
    }
    return jsonify(demand_forecast), 200