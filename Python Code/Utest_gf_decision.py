"""
SUMMARY:
Unit tests for the gfDecider class from gf_decision.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from gf_decision import gfDecider
import unittest


"""
CLASSES
"""
class test_gf_decision(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables and object call for methods
        """
        
    
    def test_fixed(self):
        """
        Unit tests for the Fixed method
        """
        
    
    def test_linear(self):
        """
        Unit tests for the Linear method
        """
    
    
    def test_quadratic(self):
        """
        Unit tests for the Quadratic method
        """
        
        
        


"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_gf_decision)
unittest.TextTestRunner(verbosity=2).run(suite)