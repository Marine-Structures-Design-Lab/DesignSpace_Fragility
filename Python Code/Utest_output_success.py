"""
SUMMARY:
Unit tests for the getOutput class from output_vals.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_success import checkOutput
import unittest

"""
CLASSES
"""
class test_output_success(unittest.TestCase):

    def setUp(self):
        
    
    def test_check_output(self):
        """
        Unit tests for the checkOutput method
        """
        
        # Check that only testing new output points
        
        # Check there is not rewriting of previous "pass?" values
        
    
    # Other methods
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_output_success)
unittest.TextTestRunner(verbosity=2).run(suite)