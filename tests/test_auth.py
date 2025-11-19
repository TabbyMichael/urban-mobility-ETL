#!/usr/bin/env python3
"""
Test script for the new authentication system
"""
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.auth.auth import auth_manager

def test_auth_system():
    """Test the authentication system"""
    print("Testing authentication system...")
    
    # Test password hashing
    password = "testpassword123"
    hashed = auth_manager.hash_password(password)
    print(f"Original password: {password}")
    print(f"Hashed password: {hashed}")
    
    # Test password verification
    is_valid = auth_manager.verify_password(password, hashed)
    print(f"Password verification: {is_valid}")
    
    # Test invalid password
    is_invalid = auth_manager.verify_password("wrongpassword", hashed)
    print(f"Invalid password verification: {is_invalid}")
    
    # Test JWT token generation
    token = auth_manager.generate_token("testuser", "admin")
    print(f"Generated token: {token}")
    
    # Test token verification
    payload = auth_manager.verify_token(token)
    print(f"Token payload: {payload}")
    
    # Test invalid token
    invalid_payload = auth_manager.verify_token("invalid.token.here")
    print(f"Invalid token payload: {invalid_payload}")
    
    print("Authentication system test completed!")

if __name__ == "__main__":
    test_auth_system()