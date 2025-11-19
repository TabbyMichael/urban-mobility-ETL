import jwt
import bcrypt
from datetime import datetime, timedelta
import os
from typing import Optional, Dict, Any
from src.data.database import DatabaseManager

class AuthManager:
    def __init__(self):
        self.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
        self.db_manager = DatabaseManager()
        
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self, username: str, role: str = 'user') -> str:
        """Generate a JWT token"""
        payload = {
            'username': username,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a JWT token and return payload if valid"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Invalid token
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user and return token if successful"""
        try:
            # Query user from database
            query = "SELECT id, username, password_hash, role FROM users WHERE username = %s"
            df = self.db_manager.execute_query(query, (username,))
            
            if df.empty:
                return None  # User not found
            
            user_row = df.iloc[0]
            stored_hash = user_row['password_hash']
            
            # Verify password
            if self.verify_password(password, stored_hash):
                # Update last login
                update_query = "UPDATE users SET last_login = %s WHERE username = %s"
                self.db_manager.execute_query(update_query, (datetime.utcnow(), username))
                
                # Generate token
                token = self.generate_token(username, user_row['role'])
                return {
                    "username": username,
                    "role": user_row['role'],
                    "token": token
                }
            
            return None  # Invalid password
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def create_user(self, username: str, password: str, role: str = 'user') -> bool:
        """Create a new user"""
        try:
            # Check if user already exists
            check_query = "SELECT id FROM users WHERE username = %s"
            df = self.db_manager.execute_query(check_query, (username,))
            
            if not df.empty:
                return False  # User already exists
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Insert new user
            insert_query = """
                INSERT INTO users (username, password_hash, role) 
                VALUES (%s, %s, %s)
            """
            self.db_manager.execute_query(insert_query, (username, hashed_password, role))
            
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def get_user_role(self, username: str) -> Optional[str]:
        """Get the role of a user"""
        try:
            query = "SELECT role FROM users WHERE username = %s"
            df = self.db_manager.execute_query(query, (username,))
            
            if df.empty:
                return None
            
            return df.iloc[0]['role']
        except Exception as e:
            print(f"Error getting user role: {e}")
            return None

# Global instance
auth_manager = AuthManager()