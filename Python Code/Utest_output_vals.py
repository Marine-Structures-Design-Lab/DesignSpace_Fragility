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
from output_vals import getOutput
import unittest

"""
CLASSES
"""
class test_output_vals(unittest.TestCase):      
    
    def test_get_output(self):
        """
        Unit tests for the getOutput method
        """
        
    
    # Other methods
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_output_vals)
unittest.TextTestRunner(verbosity=2).run(suite)