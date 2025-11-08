import time
from collections import defaultdict
from functools import wraps
from flask import request, jsonify
import hashlib

class RateLimiter:
    """Rate limiter for API endpoints"""
    
    def __init__(self, max_requests=100, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)  # key -> list of timestamps
    
    def get_client_key(self):
        """Generate a key for the client based on IP and user agent"""
        ip = request.remote_addr or 'unknown'
        user_agent = request.headers.get('User-Agent', 'unknown')
        key_string = f"{ip}:{user_agent}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def is_allowed(self):
        """Check if the client is allowed to make a request"""
        client_key = self.get_client_key()
        now = time.time()
        
        # Remove old requests outside the window
        self.requests[client_key] = [
            timestamp for timestamp in self.requests[client_key]
            if now - timestamp < self.window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_key]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_key].append(now)
        return True
    
    def get_remaining_requests(self):
        """Get the number of remaining requests for the client"""
        client_key = self.get_client_key()
        now = time.time()
        
        # Remove old requests outside the window
        self.requests[client_key] = [
            timestamp for timestamp in self.requests[client_key]
            if now - timestamp < self.window_seconds
        ]
        
        return max(0, self.max_requests - len(self.requests[client_key]))
    
    def get_reset_time(self):
        """Get the time when the rate limit will reset"""
        client_key = self.get_client_key()
        if not self.requests[client_key]:
            return 0
        
        oldest_request = min(self.requests[client_key])
        return oldest_request + self.window_seconds

# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)

def rate_limit(max_requests=100, window_seconds=60):
    """Decorator to apply rate limiting to Flask routes"""
    def decorator(f):
        # Create a rate limiter for this specific route
        route_limiter = RateLimiter(max_requests, window_seconds)
        
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not route_limiter.is_allowed():
                return jsonify({
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {max_requests} requests per {window_seconds} seconds allowed",
                    "remaining": 0,
                    "reset": route_limiter.get_reset_time()
                }), 429
            
            # Add rate limit headers to response
            response = f(*args, **kwargs)
            remaining = route_limiter.get_remaining_requests()
            reset_time = route_limiter.get_reset_time()
            
            if hasattr(response, 'headers'):
                response.headers['X-RateLimit-Remaining'] = str(remaining)
                response.headers['X-RateLimit-Reset'] = str(reset_time)
            
            return response
        return wrapper
    return decorator