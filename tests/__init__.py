"""for unit test, get all files start with tests"""
import unittest

def get_tests():
    """get all files start with tests"""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite
