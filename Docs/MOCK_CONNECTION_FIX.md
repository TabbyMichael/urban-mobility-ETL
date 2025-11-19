# Fixing Pyright Type Checking Issues with MockConnection

## Problem Description

When using Pyright for static type checking in test files, you may encounter the following errors:

```
Object of type "MockConnection" cannot be used with "with" because it does not correctly implement __enter__
Object of type "MockConnection" cannot be used with "with" because it does not correctly implement __exit__
```

## Root Cause

This error occurs because Pyright's type checker requires objects used in `with` statements to properly implement the context manager protocol, which includes:

1. `__enter__` method - Called when entering the `with` block
2. `__exit__` method - Called when exiting the `with` block

If a mock connection class doesn't implement these methods, Pyright will flag it as a type error, even though the code might work at runtime.

## Solutions

### Solution 1: Implement Context Manager Protocol Properly

Create a mock connection class that properly implements both required methods:

```python
class MockConnection:
    def __init__(self, should_fail=False):
        self.should_fail = should_fail
        self.closed = False
    
    def __enter__(self):
        """Enter the runtime context. Required for 'with' statement usage."""
        if self.should_fail:
            raise Exception("Failed to establish connection")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context. Required for 'with' statement usage."""
        self.closed = True
        # Return False to propagate any exceptions that occurred in the 'with' block
        return False
    
    def execute(self, query, params=None):
        """Mock execute method"""
        if self.should_fail:
            raise Exception("Query execution failed")
        return MockResult()
```

### Solution 2: Use MagicMock with Proper Configuration

Configure MagicMock to properly support context managers:

```python
from unittest.mock import MagicMock

def test_with_magic_mock():
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.__exit__.return_value = None
    mock_conn.execute.return_value = [("result",)]
    
    # This approach works with Pyright
    with mock_conn as conn:
        result = conn.execute("SELECT 1")
        assert result == [("result",)]
```

### Solution 3: Simplify Test Logic

Sometimes the best approach is to simplify test logic to avoid complex type annotations that confuse Pyright:

```python
# Instead of complex mocking, use simpler approaches
def test_database_operation():
    # Direct test without complex mocking
    result = some_function_that_returns_data()
    assert result is not None
```

## Best Practices

1. **Always implement both `__enter__` and `__exit__`** when creating mock classes for use with context managers
2. **Return `self` from `__enter__`** to enable assignment in the `with` statement
3. **Handle exceptions properly in `__exit__`** by returning `False` to propagate exceptions
4. **Use MagicMock appropriately** when you need flexible mocking behavior
5. **Consider simplifying test logic** when facing persistent type checking issues

## Example Implementation

See [test_mock_connection.py](../tests/test_mock_connection.py) for a complete working example of properly implemented mock connections that pass Pyright type checking.