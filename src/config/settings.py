import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = os.environ.get('FLASK_DEBUG') or True
    
    # Data source configurations
    NYC_TAXI_DATA_URL = "https://data.cityofnewyork.us/resource/"
    UBER_DATA_URL = "https://movement.uber.com/explore/new_york_city/travel-times"
    MTA_GTFS_URL = "https://api.mta.info/"
    
    # Database configuration (placeholder)
    DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///urban_mobility.db'