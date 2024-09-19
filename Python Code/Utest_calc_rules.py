"""
SUMMARY:
Unit tests for the calcRules function from calc_rules.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from calc_rules import calcRules
from vars_def import setProblem
from create_key import createKey, createDict
from get_constraints import getConstraints, getInequalities
import unittest
import numpy as np
import sympy as sp

"""
CLASSES
"""
class test_get_constraints(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the test cases
        """
        
        # Set up the problem
        prob = setProblem()
        self.Discips, self.Input_Rules, self.Output_Rules = prob.SBD1()
        self.Discips2, self.Input_Rules2, self.Output_Rules2 = prob.SenYang()
        self.y = sp.symbols('y1:6')
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Create a key for tested inputs of discipline
            self.Discips[i] = createKey('tested_ins',self.Discips[i])
            self.Discips2[i] = createKey('tested_ins',self.Discips2[i])
            
            # Create a key for tested outputs of discipline
            self.Discips[i] = createKey('tested_outs',self.Discips[i])
            self.Discips2[i] = createKey('tested_outs',self.Discips2[i])
            
            # Create a key for output rule inequalities relevant to discipline
            self.Discips[i] = createDict('out_ineqs',self.Discips[i])
            self.Discips2[i] = createDict('out_ineqs',self.Discips2[i])
        
        # Create output values for disciplin
        self.Discips[2]['tested_outs'] = np.array([[1.0, 1.0],
                                                   [3.0, 5.0]])
        self.Discips2[1]['tested_outs'] = np.array([[0.4]])
        
        # Create input values for discipline 2
        self.Discips2[1]['tested_ins'] = \
            np.array([[0.4, 0.1, 0.3, 0.8, 0.0, 0.4]])
        
        return
    
    
    def test_calc_rules(self):
        """
        Unit tests for the calcRules function
        """
        
        # Create arrays with expected answers
        exp_ans = [np.array([1.0, 3.0]),
                   np.array([1.0, 3.0]),
                   np.array([1.0, 5.0]),
                   np.array([1.0, 5.0]),
                   np.array([3.5, 16.5])]
        exp_ans2 = [np.array([0.0500000000000000])]
        
        # Create an arbitrary list of extra rules
        extra_rules = [0.5*self.y[3]+3*self.y[4]<12]
        
        # Determine current output value rules for the discipline to meet
        output_rules =\
            getConstraints(self.Discips[2]['outs'],self.Output_Rules)
        output_rules2 = \
            getConstraints(self.Discips2[1]['outs']+self.Discips2[1]['ins'],
                           self.Output_Rules2)
            
        # Add arbitrary rule to the output rules
        output_rules += extra_rules
        
        # Gather any new inequalities of relevance to the discipline
        self.Discips[2] =\
            getInequalities(self.Discips[2],output_rules,'out_ineqs')
        self.Discips2[1] =\
            getInequalities(self.Discips2[1],output_rules2,'out_ineqs')
        
        # Calculate left-hand side of output rule inequality for each point
        self.Discips[2]['out_ineqs'] =\
            calcRules(self.Discips[2],'out_ineqs','tested_outs','outs',
                      'tested_ins','ins')
        self.Discips2[1]['out_ineqs'] =\
            calcRules(self.Discips2[1],'out_ineqs','tested_outs','outs',
                      'tested_ins','ins')
        
        # Loop through each key of the 'out_ineqs' key
        count = 0
        for key in self.Discips[2]['out_ineqs']:
            
            # Check that array is equal to the expected answers array
            np.testing.assert_array_equal(self.Discips[2]['out_ineqs'][key],\
                                          exp_ans[count])
            count += 1
        
        # Loop through each key of the 'out_ineqs' key
        for key in self.Discips2[1]['out_ineqs']:
            
            # Check that value in array is equal to expected answer
            self.assertAlmostEqual(self.Discips2[1]['out_ineqs'][key][0], 
                       exp_ans2[0][0], delta=1e-15)


        return
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_get_constraints)
unittest.TextTestRunner(verbosity=2).run(suite)
    
    