"""
SUMMARY:
Unit tests for the functions from windfall_regret.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from windfall_regret import createBins, initializeWR, complementProb, \
    minmaxNormalize, assignWR, evalCompProb, calcWindRegret, quantRisk
import unittest
import sympy as sp
import numpy as np


"""
CLASSES
"""
class test_windfall_regret(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables for functions
        """
        
        # Initialize sympy input variables
        x = sp.symbols('x1:7')
        y = sp.symbols('y1:6')
        
        # Create set of input rules already adopted
        rule1 = x[0] < 0.5
        rule2 = sp.And(x[3] > 0.05, x[3] < 0.55)
        rule3 = sp.Or(x[4] > 0.7, x[5] < 0.8)
        self.irf = [rule1, rule2, rule3]
        
        # Create new set of input rules being proposed
        self.rule4 = x[2] < 0.7
        self.rule5 = sp.Or(x[0] > 0.3, x[5] < 0.4)
        
        # Initialize Discipline information at the beginning of the time stamp
        self.Discips_fragility = [
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
             'space_remaining_ind': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
             'tp_actual': 100,
             'tested_ins': np.zeros((10,3)),
             'tested_outs': np.zeros((10,1)),
             'Fail_Amount': np.zeros(10),
             'Pass_Amount': np.zeros(10),
             'pass?': [False, False, False, False, False, False, False, False,
                       False, False],
             'ins': [x[0], x[1], x[2]],
             'outs': [y[0]]},
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
             'space_remaining_ind': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
             'tp_actual': 100,
             'tested_ins': np.zeros((10,3)),
             'tested_outs': np.zeros((10,2)),
             'Fail_Amount': np.zeros(10),
             'Pass_Amount': np.zeros(10),
             'pass?': [False, False, False, False, False, False, False, False,
                       False, False],
             'ins': [x[2], x[3], x[4]],
             'outs': [y[1], y[2]]},
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
             'space_remaining_ind': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
             'tp_actual': 100,
             'tested_ins': np.zeros((10,3)),
             'tested_outs': np.zeros((10,2)),
             'Fail_Amount': np.zeros(10),
             'Pass_Amount': np.zeros(10),
             'pass?': [False, False, False, False, False, False, False, False,
                       False, False],
             'ins': [x[0], x[4], x[5]],
             'outs': [y[3], y[4]]}
        ]
    
    
    def test_create_bins(self):
        """
        Unit tests for the createBins function
        """
        
        # Execute the function for each discipline
        unique_bins1, inverse_indices1 = createBins(self.Discips_fragility[0],
                                                    [0, 1, 2], 1350)
        unique_bins2, inverse_indices2 = createBins(self.Discips_fragility[1],
                                                    [1, 2], 1400)
        unique_bins3, inverse_indices3 = createBins(self.Discips_fragility[2],
                                                    [2], 1300)
        
        # Determine the expected results
        exp_unique_bins1 = np.array([[0, 0, 0],
                                     [0, 0, 1],
                                     [0, 0, 2],
                                     [0, 0, 3],
                                     [0, 0, 4],
                                     [6, 0, 5],
                                     [6, 0, 6],
                                     [6, 0, 7],
                                     [6, 0, 8],
                                     [6, 0, 9]])
        exp_inverse_indices1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        exp_unique_bins2 = np.array([[0, 0],
                                     [1, 0],
                                     [2, 0],
                                     [3, 0],
                                     [4, 0],
                                     [5, 0],
                                     [6, 0],
                                     [7, 0],
                                     [8, 0],
                                     [9, 0]])
        exp_inverse_indices2 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        exp_unique_bins3 = np.array([[0],
                                     [7],
                                     [8],
                                     [9],
                                     [10]])
        exp_inverse_indices3 = np.array([3, 4, 0, 0, 1, 2, 3, 0, 0, 0])
        
        # Check that arrays are equal for each discipline
        np.testing.assert_array_almost_equal(unique_bins1, 
                                             exp_unique_bins1)
        np.testing.assert_array_almost_equal(inverse_indices1, 
                                             exp_inverse_indices1)
        np.testing.assert_array_almost_equal(unique_bins2, 
                                             exp_unique_bins2)
        np.testing.assert_array_almost_equal(inverse_indices2, 
                                             exp_inverse_indices2)
        np.testing.assert_array_almost_equal(unique_bins3, 
                                             exp_unique_bins3)
        np.testing.assert_array_almost_equal(inverse_indices3, 
                                             exp_inverse_indices3)
        
    
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
    
    
    def test_minmax_normalize(self):
        """
        Unit tests for the minmaxNormalize function
        """
        
        # Initialize an empty data array
        data = np.array([])
        
        # Determine expected returned data array
        exp_data = np.array([])
        
        # Run the function
        act_data = minmaxNormalize(data)
        
        # Check that actual data array matches expected
        np.testing.assert_array_almost_equal(act_data, exp_data)
        
        # Initialize an array with same min and max values
        data = np.array([3.0, 3.0])
        
        # Determine expected returned data array
        exp_data = np.zeros_like(data)
        
        # Run the function
        act_data = minmaxNormalize(data)
        
        # Check that actual data array matches expected
        np.testing.assert_array_almost_equal(act_data, exp_data)
        
        # Initialize an array with various data
        data = np.array([0.1, 0.5, 2.0])
        
        # Determine expected returned data array
        exp_data = np.array([0.0, 0.2105263158, 1.0])
        
        # Run the function
        act_data = minmaxNormalize(data)
        
        # Check that actual data array matches expected
        np.testing.assert_array_almost_equal(act_data, exp_data)
    
    
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
    
    
    def test_average_wr(self):
        """
        Unit tests for the averageWR function
        """
    
    
    def test_eval_comp_prob(self):
        """
        Unit tests for the evalCompProb function
        """
        
        # Create passfail data
        pf_fragility = [
            np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
            np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
            np.array([-0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, 
                      -1.0])
        ]
        
        # Create passfail standard deviation data
        pf_std_fragility = [np.ones(10), np.ones(10), np.ones(10)]
        
        # Determine expected complementary probabilities of feasibility
        exp_prob_feas = [np.array([1.0, 0.8692216889, 0.7410308257, 
                                   0.6166254663, 0.4970941278, 0.3833876659, 
                                   0.2762976001, 0.1764416626, 0.0842568714, 
                                   0.0]),
                         np.array([1.0, 0.8692216889, 0.7410308257, 
                                   0.6166254663, 0.4970941278, 0.3833876659, 
                                   0.2762976001, 0.1764416626, 0.0842568714, 
                                   0.0]),
                         np.array([1.0, 0.8692216889, 0.7410308257, 
                                   0.6166254663, 0.4970941278, 0.3833876659, 
                                   0.2762976001, 0.1764416626, 0.0842568714, 
                                   0.0]),
        ]
        
        # Run the function
        act_prob_feas = evalCompProb(pf_fragility, pf_std_fragility)
        
        # Check that expected results match actual results
        for res_exp, res_act in zip(exp_prob_feas, act_prob_feas):
            np.testing.assert_array_almost_equal(res_exp, res_act)
        
    
    def test_calc_wind_regret(self):
        """
        Unit tests for the calcWindRegret function
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
        
        # Create passfail data at the beginning of the time stamp
        pf_fragility = [
            np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
            np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
            np.array([-0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, 
                      -1.0])
        ]
        
        # Create probability of feasibility / TVE data
        prob_tve = [np.array([1.0, 0.8692216889, 0.7410308257, 
                                   0.6166254663, 0.4970941278, 0.3833876659, 
                                   0.2762976001, 0.1764416626, 0.0842568714, 
                                   0.0]),
                         np.array([1.0, 0.8692216889, 0.7410308257, 
                                   0.6166254663, 0.4970941278, 0.3833876659, 
                                   0.2762976001, 0.1764416626, 0.0842568714, 
                                   0.0]),
                         np.array([1.0, 0.8692216889, 0.7410308257, 
                                   0.6166254663, 0.4970941278, 0.3833876659, 
                                   0.2762976001, 0.1764416626, 0.0842568714, 
                                   0.0]),
        ]
        
        # Determine expected windfall and regret dictionaries
        exp_windreg = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': np.array([-1.0, -0.8692216889, 
                                       -0.7410308257, -0.6166254663, 
                                       -0.4970941278, -0.3833876659, 
                                       -0.2762976001, -0.1764416626, 
                                       -0.0842568714, -0.0]),
              'reduced': np.array([-1.0, -0.8692216889, -0.7410308257, 
                                   -0.6166254663, -0.4970941278]),
              'leftover': np.array([0.3833876659, 0.2762976001, 
                                    0.1764416626, 0.0842568714, 0.0])},
             {'non_reduced': np.array([-1.0, -0.8692216889, 
                                       -0.7410308257, -0.6166254663, 
                                       -0.4970941278, -0.3833876659, 
                                       -0.2762976001, -0.1764416626, 
                                       -0.0842568714, -0.0]),
              'reduced': np.array([]),
              'leftover': np.array([1.0, 0.8692216889, 0.7410308257, 
                                    0.6166254663, 0.4970941278, 0.3833876659, 
                                    0.2762976001, 0.1764416626, 0.0842568714, 
                                    0.0])},
             {'non_reduced': np.array([1.0, 0.8692216889, 
                                       0.7410308257, 0.6166254663, 
                                       0.4970941278, 0.3833876659, 
                                       0.2762976001, 0.1764416626, 
                                       0.0842568714, 0.0]),
              'reduced': np.array([0.7410308257, 0.6166254663, 0.3833876659]),
              'leftover': np.array([-1.0, -0.8692216889, -0.4970941278, 
                                    -0.2762976001, -0.1764416626, 
                                    -0.0842568714, -0.0])}]}
        
        # Determine expected running windfall dictionaries
        exp_run_wind = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': 0.0000000000,
              'reduced': 0.09203838,
              'leftover': 0.0000000000},
             {'non_reduced': 0.0000000000,
              'reduced': 0.4644355909,
              'leftover': 0.0000000000},
             {'non_reduced': 0.4644355909,
              'reduced': 0.1741043958,
              'leftover': 0.0000000000}]}
        
        # Determine expected running regret dictionaries
        exp_run_reg = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': 0.4644355909,
              'reduced': 0.3723972109,
              'leftover': 0.0000000000},
             {'non_reduced': 0.4644355909,
              'reduced': 0.0000000000,
              'leftover': 0.0000000000},
             {'non_reduced': 0.0000000000,
              'reduced': 0.2903311951,
              'leftover': 0.0000000000}]}
        
        # Run the function
        windreg, run_wind, run_reg = \
            calcWindRegret(self.irf, self.Discips_fragility, passfail, 
                           prob_tve, pf_fragility)
        
        # Ensure actual windreg arrays match up with expected arrays
        for rule, list_dics in exp_windreg.items():
            for ind, dic in enumerate(list_dics):
                for ds, array in dic.items():
                    np.testing.assert_almost_equal(windreg[rule][ind][ds], 
                                                   array)
        
        # Ensure actual running windfall values match up with expected values
        for rule, list_dics in exp_run_wind.items():
            for ind, dic in enumerate(list_dics):
                for ds, val in dic.items():
                    self.assertAlmostEqual(run_wind[rule][ind][ds], val)
        
        # Ensure actual running regret values match up with expected values
        for rule, list_dics in exp_run_reg.items():
            for ind, dic in enumerate(list_dics):
                for ds, val in dic.items():
                    self.assertAlmostEqual(run_reg[rule][ind][ds], val)
    
    
    def test_quant_risk(self):
        """
        Unit tests for the quantRisk function
        """
        
        # Initialize windfall and regret dictionaries
        windreg = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': np.array([-1.0, -0.8692216889, 
                                       -0.7410308257, -0.6166254663, 
                                       -0.4970941278, -0.3833876659, 
                                       -0.2762976001, -0.1764416626, 
                                       -0.0842568714, -0.0]),
              'reduced': np.array([-1.0, -0.8692216889, -0.7410308257, 
                                   -0.6166254663, -0.4970941278]),
              'leftover': np.array([0.3833876659, 0.2762976001, 
                                    0.1764416626, 0.0842568714, 0.0])},
             {'non_reduced': np.array([-1.0, -0.8692216889, 
                                       -0.7410308257, -0.6166254663, 
                                       -0.4970941278, -0.3833876659, 
                                       -0.2762976001, -0.1764416626, 
                                       -0.0842568714, -0.0]),
              'reduced': np.array([]),
              'leftover': np.array([1.0, 0.8692216889, 0.7410308257, 
                                    0.6166254663, 0.4970941278, 0.3833876659, 
                                    0.2762976001, 0.1764416626, 0.0842568714, 
                                    0.0])},
             {'non_reduced': np.array([1.0, 0.8692216889, 
                                       0.7410308257, 0.6166254663, 
                                       0.4970941278, 0.3833876659, 
                                       0.2762976001, 0.1764416626, 
                                       0.0842568714, 0.0]),
              'reduced': np.array([0.7410308257, 0.6166254663, 0.3833876659]),
              'leftover': np.array([-1.0, -0.8692216889, -0.4970941278, 
                                    -0.2762976001, -0.1764416626, 
                                    -0.0842568714, -0.0])}]}
        
        # Initialize running windfall dictionaries
        run_wind = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': 0.0000000000,
              'reduced': 0.09203838,
              'leftover': 0.0000000000},
             {'non_reduced': 0.0000000000,
              'reduced': 0.4644355909,
              'leftover': 0.0000000000},
             {'non_reduced': 0.4644355909,
              'reduced': 0.1741043958,
              'leftover': 0.0000000000}]}
        
        # Initialize running regret dictionaries
        run_reg = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'non_reduced': 0.4644355909,
              'reduced': 0.3723972109,
              'leftover': 0.0000000000},
             {'non_reduced': 0.4644355909,
              'reduced': 0.0000000000,
              'leftover': 0.0000000000},
             {'non_reduced': 0.0000000000,
              'reduced': 0.2903311951,
              'leftover': 0.0000000000}]}
        
        # Determine expected risk dictionaries
        exp_risk = {(self.rule4, self.rule5) + tuple(self.irf): \
            [{'regret': -0.1981725385,
              'windfall': 0.0},
             {'regret': -1.0,
              'windfall': 0.0},
             {'regret': 0.0,
              'windfall': -0.62512693}]}
        
        # Run the method
        risk = quantRisk(self.Discips_fragility, run_wind, run_reg, windreg)
        
        # Ensure actual risk values match up with expected values
        for rule, list_dics in exp_risk.items():
            for ind, dic in enumerate(list_dics):
                for pot, val in dic.items():
                    self.assertAlmostEqual(risk[rule][ind][pot], val)


"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_windfall_regret)
unittest.TextTestRunner(verbosity=2).run(suite)