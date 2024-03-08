"""
SUMMARY:
Unit tests for the windfallRegret class from windfall_regret.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from windfall_regret import windfallRegret, initializeWR, complementProb, \
    assignWR
import unittest
import sympy as sp
import numpy as np


"""
CLASSES
"""
class test_windfall_regret(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables for functions and methods
        """
        
        # Initialize sympy input variables
        x = sp.symbols('x1:7')
        
        # Create set of input rules already adopted
        rule1 = x[0] < 0.5
        rule2 = sp.And(x[3] > 0.05, x[3] < 0.55)
        rule3 = sp.Or(x[4] > 0.7, x[5] < 0.8)
        self.irf = [rule1, rule2, rule3]
        irules_fragility = [rule1, rule2, rule3]
        
        # Create new set of input rules being proposed
        self.rule4 = x[2] < 0.7
        self.rule5 = sp.Or(x[0] > 0.3, x[5] < 0.4)
        
        # Initialize Discipline information at the beginning of the time stamp
        Discips_fragility = [
            {'space_remaining': np.array([[0.0, 0.0, 0.0],
                                          [0.0, 0.0, 0.1],
                                          [0.0, 0.0, 0.2],
                                          [0.0, 0.0, 0.3],
                                          [0.0, 0.0, 0.4],
                                          [0.6, 0.0, 0.5],
                                          [0.6, 0.0, 0.6],
                                          [0.6, 0.0, 0.7],
                                          [0.6, 0.0, 0.8],
                                          [0.6, 0.0, 0.9]]),
             'tp_actual': 100,
             'tested_ins': np.zeros((10,3)),
             'tested_outs': np.zeros((10,3)),
             'Fail_Amount': np.zeros(10),
             'Pass_Amount': np.zeros(10),
             'pass?': [False, False, False, False, False, False, False, False,
                       False, False],
             'ins': [x[0], x[1], x[2]]},
            {'space_remaining': np.array([[0.0, 0.0, 0.0],
                                          [1.0, 0.1, 0.0],
                                          [1.0, 0.2, 0.0],
                                          [1.0, 0.3, 0.0],
                                          [1.0, 0.4, 0.0],
                                          [1.0, 0.5, 0.0],
                                          [0.0, 0.6, 0.0],
                                          [0.0, 0.7, 0.0],
                                          [0.0, 0.8, 0.0],
                                          [0.0, 0.9, 0.0]]),
             'tp_actual': 100,
             'tested_ins': np.zeros((10,3)),
             'tested_outs': np.zeros((10,3)),
             'Fail_Amount': np.zeros(10),
             'Pass_Amount': np.zeros(10),
             'pass?': [False, False, False, False, False, False, False, False,
                       False, False],
             'ins': [x[2], x[3], x[4]]},
            {'space_remaining': np.array([[0.0, 0.6, 0.9],
                                          [0.1, 0.5, 1.0],
                                          [0.2, 0.0, 0.0],
                                          [0.3, 0.0, 0.0],
                                          [0.2, 0.7, 0.7],
                                          [0.4, 0.8, 0.8],
                                          [0.2, 0.9, 0.9],
                                          [0.7, 0.0, 0.0],
                                          [0.8, 0.0, 0.0],
                                          [0.9, 0.0, 0.0]]),
             'tp_actual': 100,
             'tested_ins': np.zeros((10,3)),
             'tested_outs': np.zeros((10,3)),
             'Fail_Amount': np.zeros(10),
             'Pass_Amount': np.zeros(10),
             'pass?': [False, False, False, False, False, False, False, False,
                       False, False],
             'ins': [x[0], x[4], x[5]]}
        ]
        
        # Create an object call
        self.windregret = windfallRegret(Discips_fragility, irules_fragility)
        
        
    def test_initialize_wr(self):
        """
        Unit tests for the initalizeWR function
        """
        
        # Create passfail dictionaries with new input rule(s)
        passfail1 = {(self.rule4, self.rule5): \
            [{'non_reduced': np.empty(0),
              'reduced': np.empty(0),
              'leftover': np.empty(0)},
             {'non_reduced': np.empty(0),
              'reduced': np.empty(0),
              'leftover': np.empty(0)},
             {'non_reduced': np.empty(0),
              'reduced': np.empty(0),
              'leftover': np.empty(0)}]}
        passfail2 = {(self.rule4,): \
            [{'non_reduced': np.empty(0),
              'reduced': np.empty(0),
              'leftover': np.empty(0)},
             {'non_reduced': np.empty(0),
              'reduced': np.empty(0),
              'leftover': np.empty(0)},
             {'non_reduced': np.empty(0),
              'reduced': np.empty(0),
              'leftover': np.empty(0)}],
                     (self.rule5,): \
            [{'non_reduced': np.empty(0),
              'reduced': np.empty(0),
              'leftover': np.empty(0)},
             {'non_reduced': np.empty(0),
              'reduced': np.empty(0),
              'leftover': np.empty(0)},
             {'non_reduced': np.empty(0),
              'reduced': np.empty(0),
              'leftover': np.empty(0)}]}
        
        # Determine expected windfall and regret dictionaries
        exp_windreg1 = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': np.array([], dtype=float),
              'reduced': np.array([], dtype=float),
              'leftover': np.array([], dtype=float)},
             {'non_reduced': np.array([], dtype=float),
              'reduced': np.array([], dtype=float),
              'leftover': np.array([], dtype=float)},
             {'non_reduced': np.array([], dtype=float),
              'reduced': np.array([], dtype=float),
              'leftover': np.array([], dtype=float)}]}
        exp_windreg2 = {(self.rule4,) + tuple(self.irf): \
            [{'non_reduced': np.array([], dtype=float),
              'reduced': np.array([], dtype=float),
              'leftover': np.array([], dtype=float)},
             {'non_reduced': np.array([], dtype=float),
              'reduced': np.array([], dtype=float),
              'leftover': np.array([], dtype=float)},
             {'non_reduced': np.array([], dtype=float),
              'reduced': np.array([], dtype=float),
              'leftover': np.array([], dtype=float)}],
                        (self.rule5,) + tuple(self.irf): \
            [{'non_reduced': np.array([], dtype=float),
              'reduced': np.array([], dtype=float),
              'leftover': np.array([], dtype=float)},
             {'non_reduced': np.array([], dtype=float),
              'reduced': np.array([], dtype=float),
              'leftover': np.array([], dtype=float)},
             {'non_reduced': np.array([], dtype=float),
              'reduced': np.array([], dtype=float),
              'leftover': np.array([], dtype=float)}]}
        exp_run_wind1 = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0}]}
        exp_run_wind2 = {(self.rule4,) + tuple(self.irf): \
            [{'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0}],
                         (self.rule5,) + tuple(self.irf): \
            [{'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0}]}
        exp_run_reg1 = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0}]}
        exp_run_reg2 = {(self.rule4,) + tuple(self.irf): \
            [{'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0}],
                        (self.rule5,) + tuple(self.irf): \
            [{'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0},
             {'non_reduced': 0.0,
              'reduced': 0.0,
              'leftover': 0.0}]}
        
        # Run the function
        windreg1, run_wind1, run_reg1 = initializeWR(self.irf, passfail1)
        windreg2, run_wind2, run_reg2 = initializeWR(self.irf, passfail2)
        
        # Ensure that proper keys are produced in each dictionary
        self.assertSetEqual(set(windreg1.keys()), set(exp_windreg1.keys()))
        self.assertSetEqual(set(windreg2.keys()), set(exp_windreg2.keys()))
        self.assertSetEqual(set(run_reg1.keys()), set(exp_run_reg1.keys()))
        self.assertSetEqual(set(run_reg2.keys()), set(exp_run_reg2.keys()))
        self.assertSetEqual(set(run_wind1.keys()), set(exp_run_wind1.keys()))
        self.assertSetEqual(set(run_wind2.keys()), set(exp_run_wind2.keys()))
        
        # Ensure each key has a list of the proper size
        for key in exp_windreg1.keys():
            self.assertEqual(len(windreg1[key]), len(exp_windreg1[key]))
        for key in exp_windreg2.keys():
            self.assertEqual(len(windreg2[key]), len(exp_windreg2[key]))
        for key in exp_run_reg1.keys():
            self.assertEqual(len(run_reg1[key]), len(exp_run_reg1[key]))
        for key in exp_run_reg2.keys():
            self.assertEqual(len(run_reg2[key]), len(exp_run_reg2[key]))
        for key in exp_run_wind1.keys():
            self.assertEqual(len(run_wind1[key]), len(exp_run_wind1[key]))
        for key in exp_run_wind2.keys():
            self.assertEqual(len(run_wind2[key]), len(exp_run_wind2[key]))
        
        # Ensure that proper keys are produced in each inner dictionary
        for key1, list_dics in exp_windreg1.items():
            for ind, dic in enumerate(list_dics):
                self.assertSetEqual(set(windreg1[key1][ind].keys()),
                                    set(list_dics[ind].keys()))
        for key1, list_dics in exp_windreg2.items():
            for ind, dic in enumerate(list_dics):
                self.assertSetEqual(set(windreg2[key1][ind].keys()),
                                    set(list_dics[ind].keys()))
        for key1, list_dics in exp_run_reg1.items():
            for ind, dic in enumerate(list_dics):
                self.assertSetEqual(set(run_reg1[key1][ind].keys()),
                                    set(list_dics[ind].keys()))
        for key1, list_dics in exp_run_reg2.items():
            for ind, dic in enumerate(list_dics):
                self.assertSetEqual(set(run_reg2[key1][ind].keys()),
                                    set(list_dics[ind].keys()))
        for key1, list_dics in exp_run_wind1.items():
            for ind, dic in enumerate(list_dics):
                self.assertSetEqual(set(run_wind1[key1][ind].keys()),
                                    set(list_dics[ind].keys()))
        for key1, list_dics in exp_run_wind2.items():
            for ind, dic in enumerate(list_dics):
                self.assertSetEqual(set(run_wind2[key1][ind].keys()),
                                    set(list_dics[ind].keys()))
    
    
    def test_complement_prob(self):
        """
        Unit tests for the complementProb function
        """
        
        # Initialize various passfail and standard deviation values
        pf = [1.0, 0.0, -1.0]
        pf_std = [2.0, 1.0, 2.0]
        
        # Determine the expect output of the function
        exp_prob_feas = [0.3085375387, 0.5, 0.3085375387]
        
        # Run the function and check that output matches expected value
        for ind, (p, ps) in enumerate(zip(pf, pf_std)):
            prob_feas = complementProb(p, ps)
            self.assertAlmostEqual(prob_feas, exp_prob_feas[ind])
    
    
    def test_assign_wr(self):
        """
        Unit tests for the assignWR function
        """
        
        # Initialize a probability of feasibility value
        prob_feas = 0.5
        
        # Initialize list of indices for non-reduced and reduced design points
        indices_in_both = [0, 1]
        
        # Initialize a list of passfail values
        pf = [-0.1, 0.1, -0.1, 0.1]
        
        # Determine expected windfall and regret values
        exp_wr = [{'non_reduced': prob_feas, 'reduced': prob_feas},
                  {'non_reduced': -prob_feas, 'reduced': -prob_feas},
                  {'non_reduced': prob_feas, 'leftover': -prob_feas},
                  {'non_reduced': -prob_feas, 'leftover': prob_feas}]
        exp_run_wind = [{'non_reduced': prob_feas, 'reduced': prob_feas},
                        {},
                        {'non_reduced': prob_feas},
                        {'reduced': prob_feas}]
        exp_run_reg = [{},
                       {'non_reduced': prob_feas, 'reduced': prob_feas},
                       {'reduced': prob_feas},
                       {'non_reduced': prob_feas}]
        
        # Run the function and check that proper dictionaries are produced
        for ind, val in enumerate(pf):
            wr, run_wind, run_reg = assignWR(prob_feas,ind,indices_in_both,val)
            self.assertDictEqual(wr, exp_wr[ind])
            self.assertDictEqual(run_wind, exp_run_wind[ind])
            self.assertDictEqual(run_reg, exp_run_reg[ind])
    
    
    def test_calc_wind_regret(self):
        """
        Unit tests for the calcWindRegret method
        """
        
        # Create passfail dictionary with new input rules
        passfail = {(self.rule4, self.rule5): \
            [{'non_reduced': np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
              'reduced': np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
              'leftover': np.array([])},
             {'non_reduced': np.array([0.2, 0.3, 0.4, 0.5, 0.6]),
              'reduced': np.array([]),
              'leftover': np.array([0.2, 0.3, 0.4, 0.5, 0.6])},
             {'non_reduced': np.array([0.3, 0.4, 0.5, 0.6, 0.7]),
              'reduced': np.array([0.3, 0.4, 0.6]),
              'leftover': np.array([0.5, 0.7])}]}
        
        # Create passfail standard deviation dictionary with new input rules
        passfail_std = {(self.rule4, self.rule5): \
            [{'non_reduced': np.ones(5),
              'reduced': np.ones(5),
              'leftover': np.array([])},
             {'non_reduced': np.ones(5),
              'reduced': np.array([]),
              'leftover': np.ones(5)},
             {'non_reduced': np.ones(5),
              'reduced': np.ones(3),
              'leftover': np.ones(2)}]}
        
        # Create passfail data at the beginning of the time stamp
        pf_fragility = [
            np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
            np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
            np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ]
        
        # Create passfail standard deviation data at beginning of time stamp
        pf_std_fragility = [np.ones(10), np.ones(10), np.ones(10)]
        
        # Determine expected windfall and regret dictionaries
        exp_windreg = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': np.array([]),
              'reduced': np.array([]),
              'leftover': np.array([])},
             {'non_reduced': np.array([]),
              'reduced': np.array([]),
              'leftover': np.array([])},
             {'non_reduced': np.array([]),
              'reduced': np.array([]),
              'leftover': np.array([])}]}
        
        
            
        
        
        
        
        
        
        
        
        
    
    
    def test_quant_risk(self):
        """
        Unit tests for the quantRisk method
        """
    
    
    
    
    
    
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_windfall_regret)
unittest.TextTestRunner(verbosity=2).run(suite)