"""
SUMMARY:
Unit tests for the functions and checkSpace class from exploration_check.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from exploration_check import checkSpace, filterPoints, redundantIneqs, \
    getInequalities, recurse
import unittest
from vars_def import setProblem
import numpy as np
import sympy as sp


"""
CLASSES
"""
class test_exploration_check(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables to be used by multiple test methods
        """
        
        # Initialize the SBD problem
        prob = setProblem()
        self.Discips, self.Input_Rules, self.Output_Rules = \
            getattr(prob,'SBD1')()
        
        # Initialize tested input and failure amount arrays for one discipline
        self.Discips[0]['tested_ins'] = np.array([[0.0, 0.0, 0.0],
                                                  [0.2, 0.5, 0.8],
                                                  [0.4, 0.1, 0.1],
                                                  [0.7, 0.9, 1.0],
                                                  [0.8, 0.2, 0.4]])
        self.Discips[0]['Fail_Amount'] = np.array([0.0, 0.2, 0.4, 0.0, 0.8])
        
        # Initialize an object call for the discipline
        self.cs = checkSpace(self.Discips[0]['ins'])
        
        
    def test_recurse(self):
        """
        Unit tests for the recurse function
        """
        
    
    def test_get_inequalities(self):
        """
        Unit tests for the getInequalities function
        """
        
        
        
        
    def test_redundant_ineqs(self):
        """
        Unit tests for the redundantIneqs function
        """
        
        
        
    def test_filter_points(self):
        """
        Unit tests for the filterPoints function
        """
        
    
    
    def test_good_bad(self):
        """
        Unit tests for the goodBad method
        """
        
        # Check for a low cdf threshold
        actual_labels = self.cs.goodBad(self.Discips[0]['Fail_Amount'], 0.25)
        expected_labels = np.array(['good', 'good', 'good', 'good', 'bad'])
        np.testing.assert_array_equal(actual_labels, expected_labels)
        
        # Check for a medium cdf threshold
        actual_labels = self.cs.goodBad(self.Discips[0]['Fail_Amount'], 0.5)
        expected_labels = np.array(['good', 'good', 'bad', 'good', 'bad'])
        np.testing.assert_array_equal(actual_labels, expected_labels)
        
        # Check for a high cdf threshold
        actual_labels = self.cs.goodBad(self.Discips[0]['Fail_Amount'], 1.0)
        expected_labels = ['good', 'bad', 'bad', 'good', 'bad']
        np.testing.assert_array_equal(actual_labels, expected_labels)
        
    
    def test_extract_rules(self):
        """
        Unit tests for the extractRules method
        """
        
        
        
    def test_review_partitions(self):
        """
        Unit tests for the reviewPartions method
        """
        
        
        
    def test_prepare_rule(self):
        """
        Unit tests for the prepareRules method
        """
        
        # Define symbols
        x = sp.symbols('x1:4')
        
        # Check prepared rule consisting of one inequality
        pot_rule = [sp.Gt(x[0], 0.4)]
        actual_rule = self.cs.prepareRule(pot_rule)
        expected_rule = sp.Le(x[0], 0.4)
        self.assertEqual(actual_rule, expected_rule)
        
        # Check prepared rule consisting of multiple inequalities
        pot_rule = [sp.Lt(x[0], 0.3), sp.Ge(x[1], 0.9), sp.Le(x[2], 0.0)]
        actual_rule = self.cs.prepareRule(pot_rule)
        expected_rule = \
            sp.Or(sp.Ge(x[0], 0.3), sp.Lt(x[1], 0.9), sp.Gt(x[2], 0.0))
        self.assertEqual(actual_rule, expected_rule)
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_exploration_check)
unittest.TextTestRunner(verbosity=2).run(suite)