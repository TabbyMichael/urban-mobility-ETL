from flask import Flask, jsonify, request
import pandas as pd
import os
import sys
import logging

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.routes import api_bp
from src.config.settings import Config
from src.config.logging import logger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Set up logging
    if not app.debug:
        logger.info("Starting Urban Mobility Analytics API")
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    @app.route('/')
    def index():
        logger.info("Root endpoint accessed")
        return jsonify({
            "message": "Urban Mobility & Transportation Analytics ETL API",
            "version": "1.0",
            "endpoints": {
                "authentication": "/api/v1/auth",
                "taxi_data": "/api/v1/taxi",
                "uber_data": "/api/v1/uber",
                "transit_data": "/api/v1/transit"
            }
        })
    
    @app.route('/api/v1/auth/login', methods=['POST'])
    def login():
        """User login endpoint"""
        logger.info("Login endpoint accessed")
        
        if not request.is_json:
            logger.warning("Invalid content type for login request")
            return jsonify({"message": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            logger.warning("Missing username or password in login request")
            return jsonify({"message": "Username and password are required"}), 400
        
        # Simple authentication for demo purposes
        if username == 'admin' and password == 'admin':
            logger.info(f"Successful login for user: {username}")
            return jsonify({
                "message": "Login successful",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.5r8147"
            }), 200
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            return jsonify({"message": "Invalid credentials"}), 401
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)