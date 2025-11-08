"""
Security module for authentication and authorization
"""
import os
import hashlib
import secrets
from functools import wraps
from datetime import datetime, timedelta
import jwt

class SecurityManager:
    """Security manager for authentication and authorization"""
    
    def __init__(self):
        # In production, these should be stored in environment variables
        self.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
        self.admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        self.admin_password_hash = os.getenv('ADMIN_PASSWORD_HASH', 
                                           self._hash_password('admin'))
    
    def _hash_password(self, password):
        """Hash a password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, password_hash):
        """Verify a password against its hash"""
        return self._hash_password(password) == password_hash
    
    def generate_token(self, username, expires_in=3600):
        """Generate a JWT token for authentication"""
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        """Verify a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['username']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def authenticate(self, username, password):
        """Authenticate a user"""
        if (username == self.admin_username and 
            self.verify_password(password, self.admin_password_hash)):
            return self.generate_token(username)
        return None

# Global security manager instance
security_manager = SecurityManager()

def require_auth(f):
    """Decorator to require authentication for API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This is a simplified version for demonstration
        # In a real implementation, you would check for actual tokens
        return f(*args, **kwargs)
    
    return decorated_function

def validate_json(f):
    """Decorator to validate JSON input"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This is a simplified version for demonstration
        # In a real implementation, you would validate actual JSON
        return f(*args, **kwargs)
    
    return decorated_function