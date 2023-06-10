"""
SUMMARY:
Unit tests for the changeReduction class from reduction_change.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from reduction_change import changeReduction
import unittest
from vars_def import setProblem
import numpy as np

"""
CLASSES
"""
class test_reduction_change(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables to be used by multiple test methods
        """
        
        # Initialize the SBD problem
        prob = setProblem()
        self.Discips, self.Input_Rules, self.Output_Rules = \
            getattr(prob, 'SBD1')()
        
        # Create space remaining matrices for each discipline
        self.Discips[0]['space_remaining'] = np.array([[0.0, 0.0, 0.0],
                                                       [0.0, 0.0, 0.5],
                                                       [0.0, 0.0, 1.0],
                                                       [0.0, 0.5, 0.0],
                                                       [0.0, 0.5, 0.5],
                                                       [0.0, 0.5, 1.0],
                                                       [0.0, 1.0, 0.0],
                                                       [0.0, 1.0, 0.5],
                                                       [0.0, 1.0, 1.0],
                                                       [0.5, 0.0, 0.0],
                                                       [0.5, 0.0, 0.5],
                                                       [0.5, 0.0, 1.0],
                                                       [0.5, 0.5, 0.0],
                                                       [0.5, 0.5, 0.5],
                                                       [0.5, 0.5, 1.0],
                                                       [0.5, 1.0, 0.0],
                                                       [0.5, 1.0, 0.5],
                                                       [0.5, 1.0, 1.0],
                                                       [1.0, 0.0, 0.0],
                                                       [1.0, 0.0, 0.5],
                                                       [1.0, 0.0, 1.0],
                                                       [1.0, 0.5, 0.0],
                                                       [1.0, 0.5, 0.5],
                                                       [1.0, 0.5, 1.0],
                                                       [1.0, 1.0, 0.0],
                                                       [1.0, 1.0, 0.5],
                                                       [1.0, 1.0, 1.0]])
        self.Discips[1]['space_remaining'] = np.array([[0.5, 0.0, 0.0],
                                                       [0.5, 0.0, 0.5],
                                                       [0.5, 0.0, 1.0],
                                                       [0.5, 0.5, 0.0],
                                                       [0.5, 0.5, 0.5],
                                                       [0.5, 0.5, 1.0],
                                                       [0.5, 1.0, 0.0],
                                                       [0.5, 1.0, 0.5],
                                                       [0.5, 1.0, 1.0],
                                                       [1.0, 0.0, 0.0],
                                                       [1.0, 0.0, 0.5],
                                                       [1.0, 0.0, 1.0],
                                                       [1.0, 0.5, 0.0],
                                                       [1.0, 0.5, 0.5],
                                                       [1.0, 0.5, 1.0],
                                                       [1.0, 1.0, 0.0],
                                                       [1.0, 1.0, 0.5],
                                                       [1.0, 1.0, 1.0]])
        self.Discips[2]['space_remaining'] = np.array([[0.5, 0.0, 0.0],
                                                       [0.5, 0.0, 0.5],
                                                       [0.5, 0.0, 1.0],
                                                       [0.5, 1.0, 0.0],
                                                       [0.5, 1.0, 0.5],
                                                       [0.5, 1.0, 1.0],
                                                       [1.0, 0.0, 0.0],
                                                       [1.0, 0.0, 0.5],
                                                       [1.0, 0.0, 1.0],
                                                       [1.0, 1.0, 0.0],
                                                       [1.0, 1.0, 0.5],
                                                       [1.0, 1.0, 1.0]])
        
        # Initialize the starting size of each space remaining array
        self.tp_actual = self.Discips[0]['space_remaining'].shape[0]
        
        # Initialize a changeReduction object
        self.cr = changeReduction(self.Discips)
        
        
    def test_estimate_space(self):
        """
        Unit tests for the estimateSpace method
        """
        
        # Ensure each discipline reports the proper space remaining
        expected_sr = np.array([1.0, float(18/27), float(12/27)])
        actual_sr = self.cr.estimateSpace(self.tp_actual)
        np.testing.assert_array_almost_equal(actual_sr, expected_sr)
        
        
    def test_force_reduction(self):
        """
        Unit tests for the forceReduction method
        """
        
        
    def test_adjust_criteria(self):
        """
        Unit tests for the adjustCriteria method
        """
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_reduction_change)
unittest.TextTestRunner(verbosity=2).run(suite)