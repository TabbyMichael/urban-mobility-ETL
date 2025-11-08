import logging
import traceback
from functools import wraps
from flask import jsonify
import json
from datetime import datetime

class CentralizedExceptionHandler:
    """Centralized exception handling for the application"""
    
    def __init__(self, logger_name="urban_mobility"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def log_exception(self, exception, context=""):
        """Log an exception with full traceback"""
        self.logger.error(f"Exception occurred {context}: {str(exception)}")
        self.logger.error(traceback.format_exc())
    
    def log_info(self, message):
        """Log informational message"""
        self.logger.info(message)
    
    def log_warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def log_error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def handle_exception(self, exception, context=""):
        """Handle exception and return appropriate response"""
        self.log_exception(exception, context)
        
        # Return generic error response
        return {
            "error": "An internal error occurred",
            "timestamp": datetime.utcnow().isoformat(),
            "context": context
        }, 500

# Global exception handler instance
exception_handler = CentralizedExceptionHandler()

def handle_exceptions(f):
    """Decorator to handle exceptions in Flask routes"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Log the exception
            exception_handler.log_exception(e, f" in route {f.__name__}")
            
            # Return JSON error response
            return jsonify({
                "error": "An internal error occurred",
                "message": str(e) if not isinstance(e, ValueError) else "Invalid input data",
                "timestamp": datetime.utcnow().isoformat()
            }), 500
    return wrapper

def handle_validation_errors(f):
    """Decorator to handle validation errors specifically"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            # Log the validation error
            exception_handler.log_warning(f"Validation error in {f.__name__}: {str(e)}")
            
            # Return validation error response
            return jsonify({
                "error": "Validation failed",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }), 400
        except Exception as e:
            # Log the exception
            exception_handler.log_exception(e, f" in route {f.__name__}")
            
            # Return JSON error response
            return jsonify({
                "error": "An internal error occurred",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }), 500
    return wrapper