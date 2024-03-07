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
        
        # Create an object call
        self.fragile = checkFragility(risk)
    
    
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