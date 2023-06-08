"""
SUMMARY:
Unit tests for the calcExponential function from exponential_reduction.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from exponential_reduction import calcExponential
import unittest
import numpy as np

"""
CLASSES
"""
class test_exponential_reduction(unittest.TestCase):
    
    def test_calc_exponential(self):
        """
        Unit tests for the calcExponential function
        """
        
        # Unit test for first assertion error
        p = np.array([0.5, 1, 0.3, 0.8]) # p[0] > p[2]
        x = 0.6
        with self.assertRaises(AssertionError) as context:
            calcExponential(x, p)
        self.assertIn("Parameter 0 must be between 0 and Parameter 2, "
                      "and Parameter 2 must be less than or equal to 1.", \
                      str(context.exception))
        
        # Unit test for second assertion error
        p = np.array([0.1, 1, 0.3, 1.5]) # p[3] > 1
        x = 0.6
        with self.assertRaises(AssertionError) as context:
            calcExponential(x, p)
        self.assertIn("Parameter 3 must be between 0 and 1.", \
                      str(context.exception))
        
        # Calculation test
        p = np.array([0.1, 2, 0.3, 0.8]) # valid parameters
        x = 0.15
        result = calcExponential(x, p)
        self.assertAlmostEqual(result, 0.17107057)
    
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_exponential_reduction)
unittest.TextTestRunner(verbosity=2).run(suite)