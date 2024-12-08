"""
SUMMARY:
Unit tests for the functions from point_sorter.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from point_sorter import checkPoints, updatePoints, elimDicts, testPoints, \
    sortPoints
from vars_def import setProblem
from create_key import createDict, createNumpy2, createKey, createNumpy
from uniform_grid import uniformGrid
import unittest
import numpy as np
import sympy as sp

"""
CLASSES
"""
class test_point_sorter(unittest.TestCase):
    
    def setUp(self):
        """
        Initialize variables to be used by multiple test methods
        """
        
        # Initialize the SBD problem
        prob = setProblem()
        self.Discips, self.Input_Rules, self.Output_Rules = \
            getattr(prob,'SBD1')()
        
        # Initialize sympy variables
        self.y = sp.symbols('y1:6')
        
        # Create an array of tested input points
        self.Discips[0]['tested_ins'] = np.array([[0.1, 0.1, 0.1],
                                                  [1.0, 1.0, 1.0],
                                                  [0.3, 0.2, 0.4],
                                                  [0.0, 0.0, 1.0],
                                                  [0.5, 1.0, 0.0]])
        
        # Create an array of tested output points
        self.Discips[0]['tested_outs'] = np.array([[1.0],
                                                   [1.1],
                                                   [1.2],
                                                   [1.3],
                                                   [1.4]])
        
        # Create a vector of failure amounts
        self.Discips[0]['Fail_Amount'] = np.array([0.0, 0.1, 0.2, 0.3, 0.4])
        
        # Create a vector of pass amounts
        self.Discips[0]['Pass_Amount'] = np.array([0.0, 0.1, 0.2, 0.3, 0.4])
        
        # Create a boolean list of pass/fail values
        self.Discips[0]['pass?'] = [True, False, True, False, True]
        
        # Create a dictionary for output inequalities
        self.Discips[0]['out_ineqs'] = {
            self.y[0] < 0.32: np.array([0.0, 0.1, 0.2, 0.3, 0.4])
            }
        
        # Create an array of space remaining points (3x3x3)
        self.Discips[0]['space_remaining'], self.tp_actual, self.index_list = \
            uniformGrid(27, self.Discips[0]['ins'], self.Input_Rules)
        
        # Create a list of space remaining indices
        self.Discips[0]['space_remaining_ind'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                                  10, 11, 12, 13, 14, 15, 16,
                                                  17, 18, 19, 20, 21, 22, 23,
                                                  24, 25, 26]
        
        # Create a nested dictionary and keys for eliminated points
        self.Discips[0] = createDict('eliminated', self.Discips[0])
        self.Discips[0]['eliminated'] = createNumpy2('tested_ins', \
            self.Discips[0]['eliminated'], len(self.Discips[0]['ins']))
        self.Discips[0]['eliminated'] = createNumpy2('tested_outs', \
            self.Discips[0]['eliminated'], len(self.Discips[0]['outs']))
        self.Discips[0]['eliminated'] = createKey('pass?', \
            self.Discips[0]['eliminated'])
        self.Discips[0]['eliminated'] = createKey('space_remaining_ind', \
            self.Discips[0]['eliminated'])
        self.Discips[0]['eliminated'] = createNumpy('Fail_Amount', \
            self.Discips[0]['eliminated'])
        self.Discips[0]['eliminated'] = createNumpy('Pass_Amount', \
            self.Discips[0]['eliminated'])
        self.Discips[0]['eliminated'] = createDict('out_ineqs',
            self.Discips[0]['eliminated'])
        self.Discips[0]['eliminated'] = createNumpy2('space_remaining', \
            self.Discips[0]['eliminated'], len(self.Discips[0]['ins']))
    
    
    def test_check_points(self):
        """
        Unit tests for the checkPoints function
        """
        
        # Test rule that is a freestanding inequality (x1 > 0.5)
        rule = sp.Gt(sp.Symbol('x1'), 0.5)
        expected_indices = [0, 2, 3, 4]
        actual_indices = checkPoints\
            (self.Discips[0], rule, rule.free_symbols, 'tested_ins')
        self.assertListEqual(actual_indices, expected_indices)
        
        # Test rule that is a sympy Or relational (x2 <= 0.2 | x3 >= 0.8)
        rule = sp.Or(sp.Le(sp.Symbol('x2'), 0.2), sp.Ge(sp.Symbol('x3'), 0.8))
        expected_indices = [3, 4, 6, 7, 12, 13, 15, 16, 21, 22, 24, 25]
        actual_indices = checkPoints\
            (self.Discips[0], rule, rule.free_symbols, 'space_remaining')
        self.assertListEqual(actual_indices, expected_indices)
        
        
    def test_update_points(self):
        """
        Unit tests for the updatePoints function
        """
        
        # Establish tested input and space remaining points to be moved
        tp_elim = [2, 4]
        sr_elim = []
        
        # Execute the update points function for the provided indices
        self.Discips[0] = updatePoints(self.Discips[0], tp_elim, \
            ['tested_ins', 'tested_outs', 'Fail_Amount',
             'Pass_Amount', 'pass?', 'out_ineqs'])
        self.Discips[0] = updatePoints(self.Discips[0], sr_elim, \
            ['space_remaining', 'space_remaining_ind'])
            
        # Determine the expected lists/arrays in the eliminated dictionary
        array_ins = np.array([[0.3, 0.2, 0.4],
                              [0.5, 1.0, 0.0]])
        array_outs = np.array([[1.2],
                               [1.4]])
        array_FA = np.array([0.2, 0.4])
        array_PA = np.array([0.2, 0.4])
        dict_outineqs = {self.y[0] < 0.32: np.array([0.2, 0.4])}
        list_p = [True, True]
        space_rem_ind = []
        array_sr = np.empty((0,3))
        
        # Ensure proper values are moved
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['tested_ins'], array_ins)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['tested_outs'], array_outs)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['Fail_Amount'], array_FA)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['Pass_Amount'], array_PA)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['out_ineqs'][self.y[0] < 0.32],
             dict_outineqs[self.y[0] < 0.32])
        self.assertEqual(self.Discips[0]['eliminated']['pass?'], list_p)
        self.assertEqual(self.Discips[0]['eliminated']['space_remaining_ind'], 
                         space_rem_ind)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['space_remaining'], array_sr)
        
        # Determine the expected lists/arrays outside the eliminated dictionary
        array_ins = np.array([[0.1, 0.1, 0.1],
                              [1.0, 1.0, 1.0],
                              [0.0, 0.0, 1.0]])
        array_outs = np.array([[1.0],
                               [1.1],
                               [1.3]])
        array_FA = np.array([0.0, 0.1, 0.3])
        array_PA = np.array([0.0, 0.1, 0.3])
        dict_outineqs = {self.y[0] < 0.32: np.array([0.0, 0.1, 0.3])}
        list_p = [True, False, False]
        space_rem_ind = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                         16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        array_sr = uniformGrid(27, self.Discips[0]['ins'], self.Input_Rules)[0]
        
        # Ensure proper values remain
        np.testing.assert_array_equal(self.Discips[0]['tested_ins'], array_ins)
        np.testing.assert_array_equal\
            (self.Discips[0]['tested_outs'], array_outs)
        np.testing.assert_array_equal(self.Discips[0]['Fail_Amount'], array_FA)
        np.testing.assert_array_equal(self.Discips[0]['Pass_Amount'], array_PA)
        np.testing.assert_array_equal\
            (self.Discips[0]['out_ineqs'][self.y[0] < 0.32],
             dict_outineqs[self.y[0] < 0.32])
        self.assertEqual(self.Discips[0]['pass?'], list_p)
        self.assertEqual(self.Discips[0]['space_remaining_ind'], space_rem_ind)
        np.testing.assert_array_equal\
            (self.Discips[0]['space_remaining'], array_sr)
        
    
    def test_elim_dicts(self):
        """
        Unit tests for the elimDicts function
        """
        
        # Test that discipline does not already contain "eliminated" dictionary
        self.assertNotIn("eliminated", self.Discips[1])
        
        # Execute elimDicts function on second discipline
        self.Discips[1] = elimDicts(self.Discips[1])
        
        # Test that discipline without nested "eliminated" dictionary creates
        # one with all of the relevant keys
        self.assertIn("eliminated", self.Discips[1])
        self.assertIn("Fail_Amount", self.Discips[1]['eliminated'])
        self.assertIn("Pass_Amount", self.Discips[1]['eliminated'])
        self.assertIn("pass?", self.Discips[1]['eliminated'])
        self.assertIn("tested_ins", self.Discips[1]['eliminated'])
        self.assertIn("tested_outs", self.Discips[1]['eliminated'])
        self.assertIn("out_ineqs", self.Discips[1]['eliminated'])
        self.assertIn("space_remaining", self.Discips[1]['eliminated'])
        self.assertIn("space_remaining_ind", self.Discips[1]['eliminated'])
        
        
    def test_test_points(self):
        """
        Unit tests for the testPoints function
        """
        
        # Execute the test points function for the provided rule (x1 >= 0.1)
        rule = sp.Ge(sp.Symbol('x1'), 0.1)
        self.Discips[0] = testPoints(self.Discips[0], rule.free_symbols, rule)
        
        # Determine the expected lists/arrays in the eliminated dictionary
        array_ins = np.array([[0.0, 0.0, 1.0]])
        array_outs = np.array([[1.3]])
        array_FA = np.array([0.3])
        array_PA = np.array([0.3])
        dict_outineqs = {self.y[0] < 0.32: np.array([0.3])}
        list_p = [False]
        list_sri = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        array_sr = np.array([[0.0, 0.0, 0.0],
                             [0.0, 0.0, 0.5],
                             [0.0, 0.0, 1.0],
                             [0.0, 0.5, 0.0],
                             [0.0, 0.5, 0.5],
                             [0.0, 0.5, 1.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 1.0, 0.5],
                             [0.0, 1.0, 1.0]])
        
        # Check that "eliminated" arrays and lists are correct
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['tested_ins'], array_ins)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['tested_outs'], array_outs)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['Fail_Amount'], array_FA)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['Pass_Amount'], array_PA)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['out_ineqs'][self.y[0] < 0.32],
             dict_outineqs[self.y[0] < 0.32])
        self.assertEqual(self.Discips[0]['eliminated']['pass?'], list_p)
        self.assertEqual(self.Discips[0]['eliminated']['space_remaining_ind'],
                         list_sri)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['space_remaining'], array_sr)
        
        # Determine the expected lists/arrays outside the eliminated dictionary
        array_ins = np.array([[0.1, 0.1, 0.1],
                              [1.0, 1.0, 1.0],
                              [0.3, 0.2, 0.4],
                              [0.5, 1.0, 0.0]])
        array_outs = np.array([[1.0],
                               [1.1],
                               [1.2],
                               [1.4]])
        array_FA = np.array([0.0, 0.1, 0.2, 0.4])
        array_PA = np.array([0.0, 0.1, 0.2, 0.4])
        dict_outineqs = {self.y[0] < 0.32: np.array([0.0, 0.1, 0.2, 0.4])}
        list_p = [True, False, True, True]
        list_sri = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                    24, 25, 26]
        array_sr = np.array([[0.5, 0.0, 0.0],
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
        
        # Check that remaining arrays and lists are correct
        np.testing.assert_array_equal(self.Discips[0]['tested_ins'], array_ins)
        np.testing.assert_array_equal\
            (self.Discips[0]['tested_outs'], array_outs)
        np.testing.assert_array_equal(self.Discips[0]['Fail_Amount'], array_FA)
        np.testing.assert_array_equal(self.Discips[0]['Pass_Amount'], array_PA)
        np.testing.assert_array_equal\
            (self.Discips[0]['out_ineqs'][self.y[0] < 0.32],
             dict_outineqs[self.y[0] < 0.32])
        self.assertEqual(self.Discips[0]['pass?'], list_p)
        self.assertEqual(self.Discips[0]['space_remaining_ind'], list_sri)
        np.testing.assert_array_equal\
            (self.Discips[0]['space_remaining'], array_sr)
        
    
    def test_sort_points(self):
        """
        Unit tests for the sortPoints function
        """
        
        # Populate lists/arrays for Discipline 2
        self.Discips[1]['tested_ins'] = np.array([[0.0, 0.0, 0.0],
                                                  [0.5, 0.5, 0.5],
                                                  [1.0, 1.0, 1.0]])
        self.Discips[1]['tested_outs'] = np.array([[0.0, 0.0],
                                                   [0.5, 0.5],
                                                   [1.0, 1.0]])
        self.Discips[1]['Fail_Amount'] = np.array([0.0, 0.5, 1.0])
        self.Discips[1]['Pass_Amount'] = np.array([0.0, 0.5, 1.0])
        self.Discips[1]['out_ineqs'] = {
            self.y[1] > 0.1: np.array([0.0, 0.5, 1.0])
        }
        self.Discips[1]['pass?'] = [True, False, True]
        self.Discips[1]['space_remaining'], tp_actual, \
            self.Discips[1]['space_remaining_ind'] = \
            uniformGrid(27, self.Discips[1]['ins'], self.Input_Rules)
        
        # Initialize a list of input rules
        ir1 = sp.Ge(sp.Symbol('x1'), 0.1)
        ir2 = sp.Or(sp.Le(sp.Symbol('x2'), 0.2), sp.Lt(sp.Symbol('x3'), 0.8))
        ir3 = sp.Lt(sp.Symbol('x4'), 0.9)
        irules_new = [ir1, ir2, ir3]
        
        # Run the sortPoints function for established disciplines and rules
        [self.Discips[0], self.Discips[1]] = \
            sortPoints([self.Discips[0], self.Discips[1]], irules_new)
        
        # Determine expected eliminated lists/arrays of Discipline 1
        array_ins = np.array([[0.0, 0.0, 1.0],
                              [1.0, 1.0, 1.0]])
        array_outs = np.array([[1.3],
                               [1.1]])
        array_FA = np.array([0.3, 0.1])
        array_PA = np.array([0.3, 0.1])
        dict_outineqs = {self.y[0] < 0.32: np.array([0.3, 0.1])}
        list_p = [False, False]
        list_sri = [0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 17, 23, 26]
        array_sr = np.array([[0.0, 0.0, 0.0],
                             [0.0, 0.0, 0.5],
                             [0.0, 0.0, 1.0],
                             [0.0, 0.5, 0.0],
                             [0.0, 0.5, 0.5],
                             [0.0, 0.5, 1.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 1.0, 0.5],
                             [0.0, 1.0, 1.0],
                             [0.5, 0.5, 1.0],
                             [0.5, 1.0, 1.0],
                             [1.0, 0.5, 1.0],
                             [1.0, 1.0, 1.0]])
        
        # Ensure proper values are moved for Discipline 1
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['tested_ins'], array_ins)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['tested_outs'], array_outs)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['Fail_Amount'], array_FA)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['Pass_Amount'], array_PA)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['out_ineqs'][self.y[0] < 0.32],
             dict_outineqs[self.y[0] < 0.32])
        self.assertEqual(self.Discips[0]['eliminated']['pass?'], list_p)
        self.assertEqual(self.Discips[0]['eliminated']['space_remaining_ind'],
                         list_sri)
        np.testing.assert_array_equal\
            (self.Discips[0]['eliminated']['space_remaining'], array_sr)
        
        # Determine expected remaining lists/arrays of Discipline 1
        array_ins = np.array([[0.1, 0.1, 0.1],
                              [0.3, 0.2, 0.4],
                              [0.5, 1.0, 0.0]])
        array_outs = np.array([[1.0],
                               [1.2],
                               [1.4]])
        array_FA = np.array([0.0, 0.2, 0.4])
        array_PA = np.array([0.0, 0.2, 0.4])
        dict_outineqs = {self.y[0] < 0.32: np.array([0.0, 0.2, 0.4])}
        list_p = [True, True, True]
        list_sri = [9, 10, 11, 12, 13, 15, 16, 18, 19, 20, 21, 22, 24, 25]
        array_sr = np.array([[0.5, 0.0, 0.0],
                             [0.5, 0.0, 0.5],
                             [0.5, 0.0, 1.0],
                             [0.5, 0.5, 0.0],
                             [0.5, 0.5, 0.5],
                             [0.5, 1.0, 0.0],
                             [0.5, 1.0, 0.5],
                             [1.0, 0.0, 0.0],
                             [1.0, 0.0, 0.5],
                             [1.0, 0.0, 1.0],
                             [1.0, 0.5, 0.0],
                             [1.0, 0.5, 0.5],
                             [1.0, 1.0, 0.0],
                             [1.0, 1.0, 0.5]])
        
        # Ensure proper values remain for Discipline 1
        np.testing.assert_array_equal(self.Discips[0]['tested_ins'], array_ins)
        np.testing.assert_array_equal\
            (self.Discips[0]['tested_outs'], array_outs)
        np.testing.assert_array_equal(self.Discips[0]['Fail_Amount'], array_FA)
        np.testing.assert_array_equal(self.Discips[0]['Pass_Amount'], array_PA)
        np.testing.assert_array_equal\
            (self.Discips[0]['out_ineqs'][self.y[0] < 0.32],
             dict_outineqs[self.y[0] < 0.32])
        self.assertEqual(self.Discips[0]['pass?'], list_p)
        self.assertEqual(self.Discips[0]['space_remaining_ind'], list_sri)
        np.testing.assert_array_equal\
            (self.Discips[0]['space_remaining'], array_sr)
        
        # Determine expected eliminated lists/arrays of Discipline 2
        array_ins = np.array([[1.0, 1.0, 1.0]])
        array_outs = np.array([[1.0, 1.0]])
        array_FA = np.array([1.0])
        array_PA = np.array([1.0])
        dict_outineqs = {self.y[1] > 0.1: np.array([1.0])}
        list_p = [True]
        list_sri = [6, 7, 8, 15, 16, 17, 24, 25, 26]
        array_sr = np.array([[0.0, 1.0, 0.0],
                             [0.0, 1.0, 0.5],
                             [0.0, 1.0, 1.0],
                             [0.5, 1.0, 0.0],
                             [0.5, 1.0, 0.5],
                             [0.5, 1.0, 1.0],
                             [1.0, 1.0, 0.0],
                             [1.0, 1.0, 0.5],
                             [1.0, 1.0, 1.0]])
        
        # Ensure proper values are moved for Discipline 2
        np.testing.assert_array_equal\
            (self.Discips[1]['eliminated']['tested_ins'], array_ins)
        np.testing.assert_array_equal\
            (self.Discips[1]['eliminated']['tested_outs'], array_outs)
        np.testing.assert_array_equal\
            (self.Discips[1]['eliminated']['Fail_Amount'], array_FA)
        np.testing.assert_array_equal\
            (self.Discips[1]['eliminated']['Pass_Amount'], array_PA)
        np.testing.assert_array_equal\
            (self.Discips[1]['eliminated']['out_ineqs'][self.y[1] > 0.1],
             dict_outineqs[self.y[1] > 0.1])
        self.assertEqual(self.Discips[1]['eliminated']['pass?'], list_p)
        self.assertEqual(self.Discips[1]['eliminated']['space_remaining_ind'],
                         list_sri)
        np.testing.assert_array_equal\
            (self.Discips[1]['eliminated']['space_remaining'], array_sr)
        
        # Determine expected remaining lists/arrays of Discipline 2
        array_ins = np.array([[0.0, 0.0, 0.0],
                              [0.5, 0.5, 0.5]])
        array_outs = np.array([[0.0, 0.0],
                               [0.5, 0.5]])
        array_FA = np.array([0.0, 0.5])
        array_PA = np.array([0.0, 0.5])
        dict_outineqs = {self.y[1] > 0.1: np.array([0.0, 0.5])}
        list_p = [True, False]
        list_sri = [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 18, 19, 20, 21, 
                    22, 23]
        array_sr = np.array([[0.0, 0.0, 0.0],
                             [0.0, 0.0, 0.5],
                             [0.0, 0.0, 1.0],
                             [0.0, 0.5, 0.0],
                             [0.0, 0.5, 0.5],
                             [0.0, 0.5, 1.0],
                             [0.5, 0.0, 0.0],
                             [0.5, 0.0, 0.5],
                             [0.5, 0.0, 1.0],
                             [0.5, 0.5, 0.0],
                             [0.5, 0.5, 0.5],
                             [0.5, 0.5, 1.0],
                             [1.0, 0.0, 0.0],
                             [1.0, 0.0, 0.5],
                             [1.0, 0.0, 1.0],
                             [1.0, 0.5, 0.0],
                             [1.0, 0.5, 0.5],
                             [1.0, 0.5, 1.0]])
        
        # Ensure proper values remain for Discipline 2
        np.testing.assert_array_equal(self.Discips[1]['tested_ins'], array_ins)
        np.testing.assert_array_equal\
            (self.Discips[1]['tested_outs'], array_outs)
        np.testing.assert_array_equal(self.Discips[1]['Fail_Amount'], array_FA)
        np.testing.assert_array_equal(self.Discips[1]['Pass_Amount'], array_PA)
        np.testing.assert_array_equal\
            (self.Discips[1]['out_ineqs'][self.y[1] > 0.1],
             dict_outineqs[self.y[1] > 0.1])
        self.assertEqual(self.Discips[1]['pass?'], list_p)
        self.assertEqual(self.Discips[1]['space_remaining_ind'], list_sri)
        np.testing.assert_array_equal\
            (self.Discips[1]['space_remaining'], array_sr)
    
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_point_sorter)
unittest.TextTestRunner(verbosity=2).run(suite)