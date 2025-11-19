#!/usr/bin/env python3
"""
Example of how to properly implement a MockConnection class that works with context managers
and passes Pyright type checking.
"""

class MockConnection:
    """
    A properly implemented mock connection that can be used with 'with' statements.
    """
    
    def __init__(self, should_fail=False):
        self.should_fail = should_fail
        self.closed = False
    
    def __enter__(self):
        """
        Enter the runtime context. Required for 'with' statement usage.
        Returns self to be used in the 'with' block.
        """
        if self.should_fail:
            raise Exception("Failed to establish connection")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context. Required for 'with' statement usage.
        
        Args:
            exc_type: Exception type if an exception occurred, otherwise None
            exc_val: Exception value if an exception occurred, otherwise None
            exc_tb: Traceback if an exception occurred, otherwise None
            
        Returns:
            False to propagate any exceptions, True to suppress them
        """
        self.closed = True
        # Return False to propagate any exceptions that occurred in the 'with' block
        return False
    
    def execute(self, query, params=None):
        """Mock execute method"""
        if self.should_fail:
            raise Exception("Query execution failed")
        return MockResult()

class MockResult:
    """Mock result class"""
    
    def fetchall(self):
        """Mock fetchall method"""
        return [("mock_result",)]
    
    def keys(self):
        """Mock keys method"""
        return ["column1"]

# Example usage that would pass Pyright type checking:
if __name__ == "__main__":
    # This will work without Pyright errors
    try:
        with MockConnection() as conn:
            result = conn.execute("SELECT 1")
            print(result.fetchall())
    except Exception as e:
        print(f"Error: {e}")