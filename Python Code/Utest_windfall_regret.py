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
from windfall_regret import windfallRegret, initializeWR, getIndices, \
    complementProb, assignWR
import unittest
import sympy as sp


"""
CLASSES
"""
class test_windfall_regret(unittest.TestCase):

    def setUp(self):
        """
        
        """
        
        
        
        
        
    def test_initialize_wr(self):
        """
        Unit tests for the initalizeWR function
        """

    
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
            wr, run_wind, run_reg = assignWR(prob_feas, ind, indices_in_both, val)
            self.assertDictEqual(wr, exp_wr[ind])
            self.assertDictEqual(run_wind, exp_run_wind[ind])
            self.assertDictEqual(run_reg, exp_run_reg[ind])
    
    
    def test_calc_wind_regret(self):
        """
        Unit tests for the calcWindRegret method
        """
    
    
    def test_quant_risk(self):
        """
        Unit tests for the quantRisk method
        """
    
    
    
    
    
    
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_windfall_regret)
unittest.TextTestRunner(verbosity=2).run(suite)