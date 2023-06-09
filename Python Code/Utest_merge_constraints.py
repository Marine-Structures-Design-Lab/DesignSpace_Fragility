"""
SUMMARY:
Unit tests for the mergeConstraints class from merge_constraints.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from merge_constraints import mergeConstraints
import unittest
import sympy as sp

"""
CLASSES
"""
class test_merge_constraints(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables to be used by multiple test methods
        """
        
        # Initialize sympy variables
        x = sp.symbols('x1:4')
        
        # Initialize an object for a noncontradictory rule list
        noncon_list = 
        
        
        
        # Initialize an object for a contradictory rule list
        
        
        
    def test_remove_contradiction(self):
        """
        Unit tests for the removeContradiction method
        """
        
        
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_merge_constraints)
unittest.TextTestRunner(verbosity=2).run(suite)