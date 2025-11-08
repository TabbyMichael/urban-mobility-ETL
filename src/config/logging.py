"""
Logging configuration for the Urban Mobility Analytics application
"""
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Set up application logging"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                'logs/app.log',
                maxBytes=1024*1024*15,  # 15MB
                backupCount=10
            )
        ]
    )
    
    # Set logging level based on environment
    if os.getenv('FLASK_ENV') == 'development':
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    
    return logging.getLogger(__name__)

# Initialize logging
logger = setup_logging()