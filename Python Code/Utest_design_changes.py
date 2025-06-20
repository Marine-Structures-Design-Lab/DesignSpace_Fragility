"""
SUMMARY:
Unit tests for the changeDesign class from design_changes.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from design_changes import changeDesign
from vars_def import setProblem, X
import unittest
import numpy as np
import sympy as sp
import copy


"""
CLASSES
"""
class test_design_changes(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables and object call for methods
        """
        
        # Establish disciplines and initial rules for the design problem
        prob = setProblem()
        self.Discips, self.Input_Rules, self.Output_Rules = \
            getattr(prob, 'SenYang')()
        
    
    def test_reqs(self):
        """
        Unit tests for the Reqs method - for ~50% reduction!
        """
        
        # Create sympy design and output variables
        x = sp.symbols('x1:7') # L, T, D, C_B, B, V
        y = sp.symbols('y1:4') # F_n, GM, DW
        
        # Initiate requirements changes
        change = changeDesign(self.Discips, self.Input_Rules, 
                              self.Output_Rules)
        Discips, Input_Rules, Output_Rules = getattr(change, 'Reqs')()
        
        # Determine newly expected output rules
        exp_Output_Rules = [sp.And(y[0] > 0.292, y[0] <= 0.32),
                            sp.And(y[1] - 0.07*X(x[4],4) >= 0.0, 
                                   y[1] - 0.092*X(x[4],4) < 0.0),
                            sp.And(y[2] >= 3000, y[2] <= 160000),
                            y[2] - (X(x[1],1)/0.45)**(1.0/0.31) >= 0.0]
        
        # Check that lists match expected
        self.assertListEqual(Discips, self.Discips)
        self.assertListEqual(Output_Rules, exp_Output_Rules)
        self.assertListEqual(Input_Rules, self.Input_Rules)
        
    
    def test_reevaluate_points(self):
        """
        Unit tests for the reevaluatePoints method
        """
        
        # Create sympy design and output variables
        x = sp.symbols('x1:7') # L, T, D, C_B, B, V
        y = sp.symbols('y1:4') # F_n, GM, DW
        
        # Fill dictionaries with information
        self.Discips = [
            {'pass?': [True, False, True],
             'ins': [x[0], x[1], x[2], x[3], x[4], x[5]],
             'outs': [y[0]],
             'out_ineqs': {y[0]<=0.32: np.array([0.1, 0.1, 0.1])},
             'Fail_Amount': np.array([0.2, 0.2, 0.2]),
             'Pass_Amount': np.array([0.3, 0.3, 0.3]),
             'tested_ins': np.array([[0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                                     [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                     [0.6, 0.6, 0.6, 0.6, 0.6, 0.6]]),
             'tested_outs': np.array([[0.7],
                                      [0.8],
                                      [0.9]]),
             'eliminated': {
                 'pass?': [True, False, True],
                 'out_ineqs': {y[0]<=0.32: np.array([0.1, 0.1, 0.1])},
                 'Fail_Amount': np.array([0.2, 0.2, 0.2]),
                 'Pass_Amount': np.array([0.3, 0.3, 0.3]),
                 'tested_ins': np.array([[0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                                         [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                         [0.6, 0.6, 0.6, 0.6, 0.6, 0.6]]),
                 'tested_outs': np.array([[0.7],
                                          [0.8],
                                          [0.9]])
                 }
            },
            {'pass?': [True, False, True],
             'ins': [x[0], x[1], x[2], x[3], x[4], x[5]],
             'outs': [y[1]],
             'out_ineqs': {y[1] - 0.07*X(x[4],4) >= 0.0: \
                           np.array([0.1, 0.1, 0.1])},
             'Fail_Amount': np.array([0.2, 0.2, 0.2]),
             'Pass_Amount': np.array([0.3, 0.3, 0.3]),
             'tested_ins': np.array([[0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                                     [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                     [0.6, 0.6, 0.6, 0.6, 0.6, 0.6]]),
             'tested_outs': np.array([[0.7],
                                      [0.8],
                                      [0.9]]),
             'eliminated': {
                 'pass?': [True, False, True],
                 'out_ineqs': {y[1] - 0.07*X(x[4],4) >= 0.0: \
                               np.array([0.1, 0.1, 0.1])},
                 'Fail_Amount': np.array([0.2, 0.2, 0.2]),
                 'Pass_Amount': np.array([0.3, 0.3, 0.3]),
                 'tested_ins': np.array([[0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                                         [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                         [0.6, 0.6, 0.6, 0.6, 0.6, 0.6]]),
                 'tested_outs': np.array([[0.7],
                                          [0.8],
                                          [0.9]])
                 }
            },
            {'pass?': [True, False, True],
             'ins': [x[0], x[1], x[2], x[3], x[4], x[5]],
             'outs': [y[2]],
             'out_ineqs': {y[2] >= 3000: np.array([0.1, 0.1, 0.1]),
                           y[2] <= 500000: np.array([0.1, 0.1, 0.1]),
                           y[2] - (X(x[1],1)/0.45)**(1.0/0.31) >= 0.0: \
                               np.array([0.1, 0.1, 0.1])},
             'Fail_Amount': np.array([0.2, 0.2, 0.2]),
             'Pass_Amount': np.array([0.3, 0.3, 0.3]),
             'tested_ins': np.array([[0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                                     [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                     [0.6, 0.6, 0.6, 0.6, 0.6, 0.6]]),
             'tested_outs': np.array([[0.7],
                                      [0.8],
                                      [0.9]]),
             'eliminated': {
                 'pass?': [True, False, True],
                 'out_ineqs': {y[2] >= 3000: np.array([0.1, 0.1, 0.1]),
                               y[2] <= 500000: np.array([0.1, 0.1, 0.1]),
                               y[2] - (X(x[1],1)/0.45)**(1.0/0.31) >= 0.0: \
                                   np.array([0.1, 0.1, 0.1])},
                 'Fail_Amount': np.array([0.2, 0.2, 0.2]),
                 'Pass_Amount': np.array([0.3, 0.3, 0.3]),
                 'tested_ins': np.array([[0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                                         [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                         [0.6, 0.6, 0.6, 0.6, 0.6, 0.6]]),
                 'tested_outs': np.array([[0.7],
                                          [0.8],
                                          [0.9]])
                 }
            }
        ]
            
        # Create a copy of the disciplines' information
        Discips = copy.deepcopy(self.Discips)
        
        # Initiate requirements changes
        change = changeDesign(self.Discips, self.Input_Rules, 
                              self.Output_Rules)
        self.Discips, self.Input_Rules, self.Output_Rules = \
            getattr(change, 'Reqs')()
        
        # Reevaluate points
        self.Discips = change.reevaluatePoints()
        
        # Check that Disciplines' dictionaries are properly update
        for discip, s_discip in zip(Discips, self.Discips):
            np.testing.assert_array_equal(discip['tested_ins'], 
                                          s_discip['tested_ins'])
            np.testing.assert_array_equal(discip['tested_outs'],
                                          s_discip['tested_outs'])
            np.testing.assert_array_equal(discip['eliminated']['tested_ins'],
                                          s_discip['eliminated']['tested_ins'])
            np.testing.assert_array_equal\
                (discip['eliminated']['tested_outs'],
                 s_discip['eliminated']['tested_outs'])
            self.assertFalse(np.array_equal(discip['Fail_Amount'],
                                            s_discip['Fail_Amount']))
            self.assertFalse(np.array_equal(discip['Pass_Amount'],
                                            s_discip['Pass_Amount']))
            self.assertFalse(np.array_equal\
                (discip['eliminated']['Fail_Amount'],
                 s_discip['eliminated']['Fail_Amount']))
            self.assertFalse(np.array_equal\
                (discip['eliminated']['Pass_Amount'],
                 s_discip['eliminated']['Pass_Amount']))
                

"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_design_changes)
unittest.TextTestRunner(verbosity=2).run(suite)