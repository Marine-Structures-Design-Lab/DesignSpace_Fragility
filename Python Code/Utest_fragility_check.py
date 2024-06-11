"""
SUMMARY:
Unit tests for the checkFragility class from fragility_check.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from fragility_check import checkFragility
import unittest
import sympy as sp
import numpy as np


"""
CLASSES
"""
class test_fragility_check(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables and object call for methods
        """
        
        # Initialize sympy input variables
        x = sp.symbols('x1:7')
        
        # Create new input rules being proposed
        self.rule1 = x[0] > 0.5
        self.rule2 = sp.And(x[3] > 0.1, x[3] < 0.5)
        self.rule3 = sp.Or(x[4] > 0.7, x[5] < 0.8)
        
        # Create added potentials for regret and windfall for rule combos
        risk = {
            (self.rule1, self.rule2): [
                {'regret': -0.1, 'windfall': 0.1},
                {'regret': 0.0, 'windfall': 0.0},
                {'regret': 0.29, 'windfall': -0.1}
                ],
            (self.rule1, self.rule3): [
                {'regret': 0.0, 'windfall': 0.0},
                {'regret': 0.9, 'windfall': -0.3},
                {'regret': 0.0, 'windfall': 0.0}
                ],
            (self.rule2, self.rule3): [
                {'regret': 0.0, 'windfall': 0.0},
                {'regret': 0.0, 'windfall': 0.0},
                {'regret': -0.45, 'windfall': 0.50}
                ]
            }
        
        # Initialize dictionaries for each discipline
        Discips_fragility = [
            {'space_remaining': np.array([[0.0, 0.0, 0.0],
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
                                         [1.0, 1.0, 1.0]]),
            'tp_actual': 27},
            {'space_remaining': np.array([[0.0, 0.0, 0.0],
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
                                         [0.5, 1.0, 1.0]]),
            'tp_actual': 27},
            {'space_remaining': np.array([[0.0, 0.0, 0.0],
                                         [0.0, 0.0, 0.5],
                                         [0.0, 0.0, 1.0],
                                         [0.0, 0.5, 0.0],
                                         [0.0, 0.5, 0.5],
                                         [0.0, 0.5, 1.0],
                                         [0.0, 1.0, 0.0],
                                         [0.0, 1.0, 0.5],
                                         [0.0, 1.0, 1.0]]),
            'tp_actual': 27},
        
        ]
        
        # Create an object call
        self.fragile = checkFragility(risk, Discips_fragility)
    
    
    def test_basic_check(self):
        """
        Unit tests for the basicCheck method
        """
        
        # Initialize current time iterations and total project iterations
        iters = 500
        iters_max = 1000
        
        # Initialize exponential function parameters
        p = np.array([0.2, 2.2, 1.0, 0.95])
        
        # Initialize exponential function shift
        shift = 0.2
        
        # Determine expected results of the returned dictionary
        exp_max_risk = {
            (self.rule1, self.rule2): {
                'value': 0.39,
                'fragile': True,
                },
            (self.rule1, self.rule3): {
                'value': 1.2,
                'fragile': True
                },
            (self.rule2, self.rule3): {
                'value': 0.0,
                'fragile': False
                }
            }
        
        # Run the method
        max_risk = self.fragile.basicCheck(iters, iters_max, p, shift)
        
        # Check that expected results are being returned
        self.assertDictEqual(max_risk, exp_max_risk)
    
    
    def test_basic_check2(self):
        """
        Unit tests for the basicCheck2 method
        """
        
        # Initialize current time iterations and total project iterations
        iters = 500
        iters_max = 1000
        
        # Initialize exponential function parameters
        p = np.array([0.2, 2.2, 1.0, 0.95])
        
        # Initialize exponential weight parameter
        shift = 0.4
        
        # Determine expected results of the returned dictionary
        exp_max_risk = {
            (self.rule1, self.rule2): {
                'fragile': True,
                0: {'value': -0.2, 'threshold': 0.9810327561},
                1: {'value': 0.0, 'threshold': 0.6540218374},
                2: {'value': 0.39, 'threshold': 0.3270109187}
                },
            (self.rule1, self.rule3): {
                'fragile': True,
                0: {'value': 0.0, 'threshold': 0.9810327561},
                1: {'value': 1.2, 'threshold': 0.6540218374},
                2: {'value': 0.0, 'threshold': 0.3270109187}
                },
            (self.rule2, self.rule3): {
                'fragile': False,
                0: {'value': 0.0, 'threshold': 0.9810327561},
                1: {'value': 0.0, 'threshold': 0.6540218374},
                2: {'value': -0.95, 'threshold': 0.3270109187}
                }
            }
        
        # Run the method
        max_risk = self.fragile.basicCheck2(iters, iters_max, p, shift)
        
        # Check that each rule returns expected boolean fragility result
        for rule in exp_max_risk.keys():
            self.assertEqual(exp_max_risk[rule]['fragile'], 
                             max_risk[rule]['fragile'])
        
        # Check that proper value and threshold are being calculated
        for rule in exp_max_risk.keys():
            for ind_dic in range(0, 3):
                self.assertAlmostEqual(exp_max_risk[rule][ind_dic]['value'],
                                       max_risk[rule][ind_dic]['value'])
                self.assertAlmostEqual(exp_max_risk[rule][ind_dic]['threshold'],
                                       max_risk[rule][ind_dic]['threshold'])
        
        
    def test_new_combo(self):
        """
        Unit tests for the newCombo method
        """
        
        # Initialize endured risk calculations
        net_wr = {
            (self.rule1, self.rule2): {
                'value': 0.39,
                'fragile': True,
                },
            (self.rule1, self.rule3): {
                'value': 1.2,
                'fragile': True
                },
            (self.rule2, self.rule3): {
                'value': 0.0,
                'fragile': False
                }
            }
        
        # Initialize a set of banned rules
        x = sp.symbols('x1:7')
        original_banned_rules = {x[1] > 0.4, sp.Or(x[3] > 0.7, x[4] < 0.9)}
        
        # Determine expected results of final combo and banned rules
        exp_final_combo = (self.rule2, self.rule3)
        exp_banned_rules = {x[1] > 0.4, sp.Or(x[3] > 0.7, x[4] < 0.9),
                            self.rule1}
        
        # Run the method
        final_combo, original_banned_rules = \
            self.fragile.newCombo(net_wr, original_banned_rules)
        
        # Check that expected results are being returned
        self.assertTupleEqual(final_combo, exp_final_combo)
        self.assertSetEqual(original_banned_rules, exp_banned_rules)


"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_fragility_check)
unittest.TextTestRunner(verbosity=2).run(suite)