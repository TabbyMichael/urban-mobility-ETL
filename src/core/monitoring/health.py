import logging
import time
from datetime import datetime
from src.core.data.database import DatabaseManager
from src.core.auth.auth import auth_manager

class HealthChecker:
    """Health check and monitoring for the Urban Mobility application"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.logger = logging.getLogger(__name__)
    
    def check_database_health(self):
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            
            # Test database connection
            if not self.db_manager.connect():
                return {
                    "status": "unhealthy",
                    "component": "database",
                    "message": "Failed to connect to database",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            # Test simple query
            df = self.db_manager.execute_query("SELECT 1 as test")
            query_time = time.time() - start_time
            
            # Check if required tables exist
            required_tables = ["trips", "zones", "users"]
            missing_tables = []
            
            for table in required_tables:
                if not self.db_manager.table_exists(table):
                    missing_tables.append(table)
            
            self.db_manager.close()
            
            if missing_tables:
                return {
                    "status": "degraded",
                    "component": "database",
                    "message": f"Missing required tables: {missing_tables}",
                    "query_time_ms": round(query_time * 1000, 2),
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            return {
                "status": "healthy",
                "component": "database",
                "message": "Database is healthy",
                "query_time_ms": round(query_time * 1000, 2),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "component": "database",
                "message": f"Database health check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def check_auth_health(self):
        """Check authentication system health"""
        try:
            # Test JWT token generation
            test_token = auth_manager.generate_token("health_check")
            
            # Test token verification
            payload = auth_manager.verify_token(test_token)
            
            if payload and payload.get("username") == "health_check":
                return {
                    "status": "healthy",
                    "component": "authentication",
                    "message": "Authentication system is healthy",
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "status": "unhealthy",
                    "component": "authentication",
                    "message": "Token verification failed",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Authentication health check failed: {e}")
            return {
                "status": "unhealthy",
                "component": "authentication",
                "message": f"Authentication health check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def check_external_services(self):
        """Check external service health (NYC TLC, Uber, MTA)"""
        # This would be implemented with actual API calls in production
        # For now, we'll return a mock response
        return {
            "status": "unknown",
            "component": "external_services",
            "message": "External service health check not implemented",
            "services": {
                "nyc_tlc": "unknown",
                "uber_movement": "unknown",
                "mta_gtfs": "unknown"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_system_health(self):
        """Get overall system health"""
        database_health = self.check_database_health()
        auth_health = self.check_auth_health()
        external_health = self.check_external_services()
        
        # Determine overall status
        statuses = [database_health["status"], auth_health["status"]]
        
        if "unhealthy" in statuses:
            overall_status = "unhealthy"
        elif "degraded" in statuses:
            overall_status = "degraded"
        else:
            overall_status = "healthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": database_health,
                "authentication": auth_health,
                "external_services": external_health
            }
        }

# Global instance
health_checker = HealthChecker()