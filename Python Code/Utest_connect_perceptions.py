"""
SUMMARY:
Unit tests for the functions in connect_perceptions.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from connect_perceptions import connectPerceptions
import unittest
import sympy as sp
import numpy as np


"""
CLASSES
"""
class test_connect_perceptions(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables and object call for functions
        """
        
        # Initialize sympy design variables
        self.x = sp.symbols('x1:8')
        
        # Initialize tested and space remaining data for multiple disciplines
        self.Discips = [
            {'tested_ins': np.ones((10, 3)),
             'ins': [self.x[0], self.x[1], self.x[2]],
             'space_remaining': np.full((20, 3), 0.95),
             'Fail_Amount': np.full((10,), 0.45),
             'Pass_Amount': np.zeros(10)},
            {'tested_ins': np.full((8, 3), 0.5),
             'ins': [self.x[2], self.x[3], self.x[4]],
             'space_remaining': np.full((30, 3), 0.85),
             'Fail_Amount': np.full((8,), 0.35),
             'Pass_Amount': np.zeros(8)},
            {'tested_ins': np.zeros((5, 3)),
             'ins': [self.x[0], self.x[4], self.x[5]],
             'space_remaining': np.full((15, 3), 0.75),
             'Fail_Amount': np.full((5,), 0.25),
             'Pass_Amount': np.zeros(5)}
        ]
        
        self.Discips2 = [
            {'tested_ins': np.random.rand(10, 3),
             'ins': [self.x[0], self.x[1], self.x[2]],
             'space_remaining': np.random.rand(20, 3),
             'Fail_Amount': np.random.rand(10),
             'Pass_Amount': np.random.rand(10)},
            {'tested_ins': np.random.rand(8, 3),
             'ins': [self.x[2], self.x[3], self.x[4]],
             'space_remaining': np.random.rand(30, 3),
             'Fail_Amount': np.random.rand(8),
             'Pass_Amount': np.random.rand(8)},
            {'tested_ins': np.random.rand(5, 4),
             'ins': [self.x[0], self.x[4], self.x[5], self.x[6]],
             'space_remaining': np.random.rand(15, 4),
             'Fail_Amount': np.random.rand(5),
             'Pass_Amount': np.random.rand(5)}
        ]
        
        
    def test_pad_data(self):
        """
        Unit tests for the padData function
        """
    
    
    def test_connect_perceptions(self):
        """
        Unit tests for the connectPerceptions function
        """
        
        # Execute the function
        pf_fragility, pf_std_fragility = connectPerceptions(self.Discips2)
        
        # Check that all of the predictions are between -1 and +1
        
        
        
        # Ensure pass-fail predictions all fall between -1 and +1



"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_connect_perceptions)
unittest.TextTestRunner(verbosity=2).run(suite)