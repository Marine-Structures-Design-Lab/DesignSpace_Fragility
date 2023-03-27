"""
SUMMARY:
Unit tests for the getInput class from input_vals.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from input_vals import getInput
import unittest

"""
CLASSES
"""
class test_input_vals(unittest.TestCase):

    def setUp(self):
        
        
    
    def test_get_uniform(self):
        """
        Unit tests for the getUniform method
        """
        
    
    # Other methods
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_input_vals)
unittest.TextTestRunner(verbosity=2).run(suite)