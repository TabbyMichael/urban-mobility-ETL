#!/usr/bin/env python3
"""
Test runner for executing all test suites
"""
import unittest
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Run all test suites"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test modules
    test_modules = [
        'test_api_integration',
        'test_end_to_end',
        'test_performance',
        'test_comprehensive_end_to_end',
        'test_end_to_end_comprehensive',
        'test_improvements'
    ]
    
    for module_name in test_modules:
        try:
            # Import the test module
            module = __import__(f'tests.{module_name}', fromlist=[module_name])
            # Load tests from the module
            loaded_tests = loader.loadTestsFromModule(module)
            # Add to suite
            suite.addTests(loaded_tests)
            print(f"Loaded tests from {module_name}")
        except ImportError as e:
            print(f"Warning: Could not import {module_name}: {e}")
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)