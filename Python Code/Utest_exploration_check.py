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
from sklearn.tree import DecisionTreeClassifier

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
        
        # Initialize variables
        x = sp.symbols('x1:3')
        
        # Create X and Y data for training a decsion tree
        X = np.array([[0.2, 0.2],
                      [0.2, 0.3],
                      [0.3, 0.3],
                      [0.3, 0.2],
                      [0.2, 0.7],
                      [0.2, 0.8],
                      [0.3, 0.8],
                      [0.3, 0.7],
                      [0.7, 0.7],
                      [0.7, 0.8],
                      [0.8, 0.8],
                      [0.8, 0.7],
                      [0.7, 0.2],
                      [0.7, 0.3],
                      [0.8, 0.3],
                      [0.8, 0.2]])
        X = X.astype(np.float32)
        y = np.array(['bad', 'bad', 'bad', 'bad', \
                      'good', 'good', 'good', 'good', \
                      'good', 'good', 'good', 'good', \
                      'good', 'good', 'good', 'good'])
        
        # Instantiate a DecisionTreeClassifier object
        clf = DecisionTreeClassifier(random_state=0)
        
        # Fit the classifier to the data
        clf.fit(X, y)
        
        # Initialize lists to be affected by the recurse function
        paths = []
        bad_tot = []
        bad_frac = []
        
        # Run the recurse function
        recurse(clf.tree_, 0, [], [x[0], x[1]], paths, bad_tot, bad_frac, X, y)
        
        # Expected list information
        exp_paths = [[x[1] <= 0.5, x[0] <= 0.5], 
                          [x[1] <= 0.5, x[0] > 0.5], 
                          [x[1] > 0.5]]
        exp_bad_tot = [4, 0, 0]
        exp_bad_frac = [1.0, 0.0, 0.0]
        
        # Check that actual lists match up with expected lists
        self.assertEqual(paths, exp_paths)
        self.assertEqual(bad_tot, exp_bad_tot)
        self.assertEqual(bad_frac, exp_bad_frac)
    
    
    def test_get_inequalities(self):
        """
        Unit tests for the getInequalities function
        """
        
        # Initialize variables
        x = sp.symbols('x1:3')
        
        # Create X and Y data for training a decsion tree
        X = np.array([[0.2, 0.2],
                      [0.2, 0.3],
                      [0.3, 0.3],
                      [0.3, 0.2],
                      [0.2, 0.7],
                      [0.2, 0.8],
                      [0.3, 0.8],
                      [0.3, 0.7],
                      [0.7, 0.7],
                      [0.7, 0.8],
                      [0.8, 0.8],
                      [0.8, 0.7],
                      [0.7, 0.2],
                      [0.7, 0.3],
                      [0.8, 0.3],
                      [0.8, 0.2]])
        X = X.astype(np.float32)
        y = np.array(['bad', 'bad', 'bad', 'bad', \
                      'good', 'good', 'good', 'good', \
                      'good', 'good', 'good', 'good', \
                      'good', 'good', 'good', 'good'])
        
        # Instantiate a DecisionTreeClassifier object
        clf = DecisionTreeClassifier(random_state=0)
        
        # Fit the classifier to the data
        clf.fit(X, y)
        
        # Run the getInequalities function
        paths, bad_tot, bad_frac = getInequalities(clf, [x[0], x[1]], X, y)
        
        # Ensure that the length of each list is greater than 0
        self.assertGreater(len(paths), 0)
        self.assertGreater(len(bad_tot), 0)
        self.assertGreater(len(bad_frac), 0)
        
        
    def test_redundant_ineqs(self):
        """
        Unit tests for the redundantIneqs function
        """
        
        # Initialize variables
        x = sp.symbols('x1:4')
        
        # Ensure no inequalities are removed when no redundancies
        ### > or <= signs only!!!
        ineqs = [x[0] > 0.5, x[1] <= 0.4, x[2] <= 0.8,
                 x[0] <= 0.2, x[1] > 0.1, x[2] > 0.8]
        uniq_ineqs = redundantIneqs(ineqs)
        exp_ineqs = [x[0] <= 0.2, x[0] > 0.5, x[1] <= 0.4,
                     x[1] > 0.1, x[2] <= 0.8, x[2] > 0.8]
        self.assertEqual(uniq_ineqs, exp_ineqs)
        
        # Ensure an inequality is removed when there is redundancy
        ### > or <= signs only!!!
        ineqs = [x[0] > 0.5, x[1] <= 0.4, x[2] <= 0.8,
                 x[0] > 0.7, x[1] > 0.1, x[2] <= 0.8]
        uniq_ineqs = redundantIneqs(ineqs)
        exp_ineqs = [x[0] > 0.7, x[1] <= 0.4, x[1] > 0.1, x[2] <= 0.8]
        self.assertEqual(uniq_ineqs, exp_ineqs)
        
        
    def test_filter_points(self):
        """
        Unit tests for the filterPoints function
        """
        
        # Define symbols
        x = sp.symbols('x1:4')
        
        # Check correct points are filtered for rule with one inequality
        ### > or <= signs only!!!
        pot_rule = [sp.Gt(x[0], 0.4)]
        actual_X, actual_FA = filterPoints(self.Discips[0]['tested_ins'], \
            self.Discips[0]['Fail_Amount'], pot_rule, self.Discips[0]['ins'])
        expected_X = np.array([[0.7, 0.9, 1.0],
                               [0.8, 0.2, 0.4]])
        expected_FA = np.array([0.0, 0.8])
        np.testing.assert_array_almost_equal(actual_X, expected_X)
        np.testing.assert_array_almost_equal(actual_FA, expected_FA)
        
        # Check correct points are filtered for rule with many inequalities
        ### > or <= signs only!!!
        pot_rule = [sp.Gt(x[0], 0.3), sp.Le(x[1], 0.9), sp.Gt(x[2], 0.4)]
        actual_X, actual_FA = filterPoints(self.Discips[0]['tested_ins'], \
            self.Discips[0]['Fail_Amount'], pot_rule, self.Discips[0]['ins'])
        expected_X = np.array([[0.7, 0.9, 1.0]])
        expected_FA = np.array([0.0])
        np.testing.assert_array_almost_equal(actual_X, expected_X)
        np.testing.assert_array_almost_equal(actual_FA, expected_FA)
        
        
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
        
        # Initialize variables
        x = sp.symbols('x1:3')
        
        # Create X and Y data for training a decsion tree
        X = np.array([[0.2, 0.2],
                      [0.2, 0.3],
                      [0.3, 0.3],
                      [0.3, 0.2],
                      [0.2, 0.7],
                      [0.2, 0.8],
                      [0.3, 0.8],
                      [0.3, 0.7],
                      [0.7, 0.7],
                      [0.7, 0.8],
                      [0.8, 0.8],
                      [0.8, 0.7],
                      [0.7, 0.2],
                      [0.7, 0.3],
                      [0.8, 0.3],
                      [0.8, 0.2]])
        X = X.astype(np.float32)
        y = np.array(['bad', 'bad', 'bad', 'bad', \
                      'good', 'good', 'good', 'good', \
                      'good', 'good', 'good', 'good', \
                      'good', 'good', 'good', 'good'])
        
        # Initialize a class
        cs = checkSpace([x[0], x[1]], max_depth = 2)
        
        # Build the decision tree
        cs.buildTree(X, y)
        
        # Gather inequalities for potential rule
        pot_rule = cs.extractRules(X, y)
        
        # Check that inequalities list matches up with expected list
        self.assertIn(x[1] <= 0.5, pot_rule)
        self.assertIn(x[0] <= 0.5, pot_rule)
        self.assertEqual(len(pot_rule), 2)
        
        # Create new X and y data for the decision tree
        # Create X and Y data for training a decsion tree
        X = np.array([[0.2, 0.45],
                      [0.2, 0.55],
                      [0.3, 0.55],
                      [0.3, 0.45],
                      [0.45, 0.45],
                      [0.45, 0.55],
                      [0.55, 0.55],
                      [0.55, 0.45],
                      [0.7, 0.45],
                      [0.7, 0.55],
                      [0.8, 0.55],
                      [0.8, 0.45],
                      [0.75, 0.5]])
        X = X.astype(np.float32)
        y = np.array(['bad', 'bad', 'bad', 'bad',
                      'good', 'good', 'good', 'good',
                      'bad', 'bad', 'bad', 'bad', 'bad'])
            
        # Build the decision tree
        cs.buildTree(X, y)
        
        # Gather inequalities for potential rule
        pot_rule = cs.extractRules(X, y)
        
        # Check that inequalities list matches up with expected list
        self.assertEqual(pot_rule, [x[0] > 0.625])
        
        
    def test_review_partitions(self):
        """
        Unit tests for the reviewPartions method
        """
        
        # Define symbols
        x = sp.symbols('x1:4')
        
        # Check that False returned if no rules being proposed
        fail_crit = 1.0
        dist_crit = 1.0
        disc_crit = 1.0
        pot_rule = []
        actual_bool = self.cs.reviewPartitions(self.Discips[0]['tested_ins'], \
            pot_rule, self.Discips[0]['Fail_Amount'], fail_crit, dist_crit, \
            disc_crit)
        expected_bool = False
        self.assertEqual(actual_bool, expected_bool)
        
        # Check that False returned if failure criterion not satisfied
        fail_crit = 0.0
        pot_rule = [x[2] > 0.9]
        actual_bool = self.cs.reviewPartitions(self.Discips[0]['tested_ins'], \
            pot_rule, self.Discips[0]['Fail_Amount'], fail_crit, dist_crit, \
            disc_crit)
        expected_bool = False
        self.assertEqual(actual_bool, expected_bool)
        
        # Check that False returned if distance criterion not satisfied
        fail_crit = 1.0
        dist_crit = 0.2
        X = np.array([[0.1, 0.1, 0.0],
                      [0.1, 0.9, 0.0],
                      [0.9, 0.9, 0.0],
                      [0.9, 0.1, 0.0]])
        FA = np.array([0.1, 0.1, 0.1, 0.1])
        pot_rule = [x[0] > 0.5]
        actual_bool = self.cs.reviewPartitions(X, pot_rule, FA, fail_crit, \
            dist_crit, disc_crit)
        expected_bool = False
        self.assertEqual(actual_bool, expected_bool)
        
        # Check that True returned if points outside of the eliminated region
        ### meet distance criterion while points inside alone do not meet it
        dist_crit = 0.05
        cs = checkSpace([x[0], x[1]], max_depth=2)
        X = np.array([[0.49, 0.1],
                      [0.49, 0.9],
                      [0.51, 0.9],
                      [0.52, 0.1]])
        actual_bool = cs.reviewPartitions(X, pot_rule, FA, fail_crit, \
            dist_crit, disc_crit)
        expected_bool = True
        self.assertEqual(actual_bool, expected_bool)
        
        # Check False returned if cannot normalize points in eliminated region
        X = np.array([[0.49, 0.1],
                      [0.49, 0.9],
                      [0.51, 0.9],
                      [0.51, 0.1]])
        actual_bool = cs.reviewPartitions(X, pot_rule, FA, fail_crit, \
            dist_crit, disc_crit)
        expected_bool = False
        self.assertEqual(actual_bool, expected_bool)
        
        # Check that False returned if discrepancy criterion not satisfied
        ### Discrepancy of X is 0.26736111111111094
        X = np.array([[0.49, 0.1],
                      [0.49, 0.9],
                      [0.51, 0.9],
                      [0.52, 0.1]])
        dist_crit = 1.0
        disc_crit = 0.2
        actual_bool = cs.reviewPartitions(X, pot_rule, FA, fail_crit, \
            dist_crit, disc_crit)
        expected_bool = False
        self.assertEqual(actual_bool, expected_bool)
        
        # Check that True returned if all criteria are satisfied
        disc_crit = 1.0
        actual_bool = cs.reviewPartitions(X, pot_rule, FA, fail_crit, \
            dist_crit, disc_crit)
        expected_bool = True
        self.assertEqual(actual_bool, expected_bool)
        
        
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