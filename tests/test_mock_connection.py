#!/usr/bin/env python3
"""
Test file demonstrating proper MockConnection implementation that passes Pyright type checking.
"""

from unittest.mock import Mock, MagicMock
import pytest

class MockConnection:
    """
    Properly implemented mock connection that works with context managers.
    """
    
    def __init__(self, should_fail=False):
        self.should_fail = should_fail
        self.closed = False
        self.execute = Mock()
    
    def __enter__(self):
        """Enter the runtime context."""
        if self.should_fail:
            raise Exception("Failed to establish connection")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context."""
        self.closed = True
        return False

def test_mock_connection_with_context_manager():
    """Test that MockConnection works properly with 'with' statement."""
    # This should not raise any Pyright type checking errors
    with MockConnection() as conn:
        conn.execute.return_value = [("test",)]
        result = conn.execute("SELECT 1")
        assert result == [("test",)]

def test_mock_connection_exception_handling():
    """Test that MockConnection properly handles exceptions."""
    with pytest.raises(Exception):
        with MockConnection(should_fail=True) as conn:
            pass  # This should raise an exception

# Alternative approach using MagicMock with proper context manager support
def test_magic_mock_as_context_manager():
    """Demonstrate using MagicMock with proper context manager setup."""
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.__exit__.return_value = None
    mock_conn.execute.return_value = [("magic_mock_result",)]
    
    # This approach also works with Pyright
    with mock_conn as conn:
        result = conn.execute("SELECT 1")
        assert result == [("magic_mock_result",)]

if __name__ == "__main__":
    test_mock_connection_with_context_manager()
    test_mock_connection_exception_handling()
    test_magic_mock_as_context_manager()
    print("All tests passed!")