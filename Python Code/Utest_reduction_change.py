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
import copy

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
        
        # Create initial exponential paramter values
        part_params = {
            "cdf_crit": [0.1, 0.1],
            "fail_crit": [0.0, 0.05],
            "dist_crit": [0.2, 0.1],
            "disc_crit": [0.2, 0.1]
            }
        
        # Create parameter and reduction keys for each discipline
        for i in range(0, len(self.Discips)):
            self.Discips[i]['force_reduction'] = [False, 0]
            self.Discips[i]['part_params'] = copy.deepcopy(part_params)
            self.Discips[i]['tp_actual'] = self.Discips[0]['space_remaining'].shape[0]
        
        # Initialize a changeReduction object
        self.cr = changeReduction(self.Discips)
        
        
    def test_estimate_space(self):
        """
        Unit tests for the estimateSpace method
        """
        
        # Ensure each discipline reports the proper space remaining
        expected_sr = np.array([1.0, float(18/27), float(12/27)])
        actual_sr = self.cr.estimateSpace()
        np.testing.assert_array_almost_equal(actual_sr, expected_sr)
        
        
    def test_force_reduction(self):
        """
        Unit tests for the forceReduction method
        """
        
        # Indicate space remaining for each discipline
        space_rem = np.array([1.0, float(18/27), float(12/27)])
        
        # Set current and max iterations
        iters = 30
        iters_max = 100
        
        # Set exponential function parameters
        p = np.array(\
            [0.2,  # p1: x-intercept
             2.0,  # p2: Steepness
             1.0,  # p3: Max percent of time to force reductions
             0.95]) # p4: Percent of space reduced at max reduction time
            
        # Execute the forceReduction method for each discipline
        self.Discips = self.cr.forceReduction(space_rem, iters, iters_max, p)
        
        # Ensure force reduction is True for Discipline 1
        self.assertTrue(self.Discips[0]['force_reduction'][0])
        
        # Ensure force reduction is False for Discipline 1 & 2
        self.assertFalse(self.Discips[1]['force_reduction'][0])
        self.assertFalse(self.Discips[1]['force_reduction'][0])
        
        
    def test_adjust_criteria(self):
        """
        Unit tests for the adjustCriteria method
        """
        
        # Ensure no parameters are changed when force reduction is False
        self.Discips = self.cr.adjustCriteria()
        self.assertEqual(self.Discips[0]['part_params']['cdf_crit'][0], 0.1)
        
        # Set force reduction to True for Discipline 1
        self.Discips[0]['force_reduction'][0] = True
        
        # Ensure cdf_crit criterion is increased
        self.Discips = self.cr.adjustCriteria()
        self.assertAlmostEqual(self.Discips[0]['part_params']['cdf_crit'][0], 0.2)
        self.assertAlmostEqual(self.Discips[0]['part_params']['fail_crit'][0], 0.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['dist_crit'][0], 0.2)
        self.assertAlmostEqual(self.Discips[0]['part_params']['disc_crit'][0], 0.2)
        
        # Ensure fail_crit criterion is increased
        self.Discips = self.cr.adjustCriteria()
        self.assertAlmostEqual(self.Discips[0]['part_params']['cdf_crit'][0], 0.2)
        self.assertAlmostEqual(self.Discips[0]['part_params']['fail_crit'][0], 0.05)
        self.assertAlmostEqual(self.Discips[0]['part_params']['dist_crit'][0], 0.2)
        self.assertAlmostEqual(self.Discips[0]['part_params']['disc_crit'][0], 0.2)
        
        # Ensure dist_crit criterion is increased
        self.Discips = self.cr.adjustCriteria()
        self.assertAlmostEqual(self.Discips[0]['part_params']['cdf_crit'][0], 0.2)
        self.assertAlmostEqual(self.Discips[0]['part_params']['fail_crit'][0], 0.05)
        self.assertAlmostEqual(self.Discips[0]['part_params']['dist_crit'][0], 0.3)
        self.assertAlmostEqual(self.Discips[0]['part_params']['disc_crit'][0], 0.2)
        
        # Ensure disc_crit criterion is increased
        self.Discips = self.cr.adjustCriteria()
        self.assertAlmostEqual(self.Discips[0]['part_params']['cdf_crit'][0], 0.2)
        self.assertAlmostEqual(self.Discips[0]['part_params']['fail_crit'][0], 0.05)
        self.assertAlmostEqual(self.Discips[0]['part_params']['dist_crit'][0], 0.3)
        self.assertAlmostEqual(self.Discips[0]['part_params']['disc_crit'][0], 0.3)
        
        # Ensure cdf_crit criterion is increased again
        self.Discips = self.cr.adjustCriteria()
        self.assertAlmostEqual(self.Discips[0]['part_params']['cdf_crit'][0], 0.3)
        self.assertAlmostEqual(self.Discips[0]['part_params']['fail_crit'][0], 0.05)
        self.assertAlmostEqual(self.Discips[0]['part_params']['dist_crit'][0], 0.3)
        self.assertAlmostEqual(self.Discips[0]['part_params']['disc_crit'][0], 0.3)
        
        # Set all criteria to 1.0 for Discipline 1
        self.Discips[0]['part_params']['cdf_crit'][0] = 1.0
        self.Discips[0]['part_params']['fail_crit'][0] = 1.0
        self.Discips[0]['part_params']['dist_crit'][0] = 1.0
        self.Discips[0]['part_params']['disc_crit'][0] = 1.0
        
        # Ensure all criteria remain at 1.0
        self.Discips = self.cr.adjustCriteria()
        self.assertAlmostEqual(self.Discips[0]['part_params']['cdf_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['fail_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['dist_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['disc_crit'][0], 1.0)
        self.Discips = self.cr.adjustCriteria()
        self.assertAlmostEqual(self.Discips[0]['part_params']['cdf_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['fail_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['dist_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['disc_crit'][0], 1.0)
        self.Discips = self.cr.adjustCriteria()
        self.assertAlmostEqual(self.Discips[0]['part_params']['cdf_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['fail_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['dist_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['disc_crit'][0], 1.0)
        self.Discips = self.cr.adjustCriteria()
        self.assertAlmostEqual(self.Discips[0]['part_params']['cdf_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['fail_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['dist_crit'][0], 1.0)
        self.assertAlmostEqual(self.Discips[0]['part_params']['disc_crit'][0], 1.0)
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_reduction_change)
unittest.TextTestRunner(verbosity=2).run(suite)