"""
SUMMARY:
Unit tests for the checkOutput class from output_success.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_success import checkOutput, outputDiff
from vars_def import setProblem
from create_key import createKey, createDict, createNumpy
from get_constraints import getConstraints, getInequalities
from calc_rules import calcRules
import unittest
import numpy as np
import copy

"""
CLASSES
"""
class test_output_success(unittest.TestCase):

    def setUp(self):
        """
        Establish dictionaries for each discipline and rules as object
        definitions
        """
        
        # Set up the initial list of dictionaries for each discipline and rules
        prob = setProblem()
        self.Discips, self.Input_Rules, self.Output_Rules = prob.SBD1()
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Create new keys
            self.Discips[i] = createKey('tested_outs',self.Discips[i])
            self.Discips[i] = createKey('pass?',self.Discips[i])
        
        # Add output values to each dictionary
        self.Discips[0]['tested_outs'] = np.array([[0.1],
                                                   [0.5]])
        self.Discips[1]['tested_outs'] = np.array([[0.6, 0.3],
                                                   [0.6, 1.1]])
        self.Discips[2]['tested_outs'] = np.array([[0.2, 1.1],
                                                   [-0.4, 2.2]])
        
        # Create copy of the dictionary
        self.Discips1 = copy.deepcopy(self.Discips)
        self.Discips2 = copy.deepcopy(self.Discips)
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Add partially filled "pass?" values to dictionary
            self.Discips1[i]['pass?'] = [None]
            
            # Create a key for the output rule inequalities relevant to discipline
            self.Discips2[i] = createDict('out_ineqs',self.Discips2[i])
            
            # Get output rules
            output_rules = getConstraints(self.Discips1[i]['outs'],\
                                          self.Output_Rules)
            
            # Gather any new inequalities of relevance to the discipline
            self.Discips2[i] =\
                getInequalities(self.Discips2[i],output_rules,'out_ineqs')
            
            # Calculate left-hand side of output rule inequality for each point
            self.Discips2[i]['out_ineqs'] =\
                calcRules(self.Discips2[i],'out_ineqs','tested_outs','outs')
            
            # Initialize object for each discipline
            outchk = checkOutput(self.Discips1[i],output_rules)
            outchk2 = checkOutput(self.Discips2[i],output_rules)
            
            # Create a key for extent of passing/failing if it does not exist
            self.Discips2[i] = createNumpy('Fail_Amount',self.Discips2[i])
            
            # Produce new discipline
            self.Discips1[i] = outchk.basicCheck()
            self.Discips2[i] = outchk2.basicCheck()
            
            # Determine the extent to which failing points fail
            self.Discips2[i] = outchk2.rmsFail()
            
            
    def test_basic_check(self):
        """
        Unit tests for the basicCheck method
        """
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
        
            # Check that there is NOT rewriting of previous "pass?" values
            self.assertEqual(self.Discips1[i]['pass?'][0],None)
            
            # Check that there is determination of new "pass?" values
            self.assertTrue(len(self.Discips1[i]['pass?']) == 2)
            
            # Check that the pass? values produced are correct
            self.assertListEqual(self.Discips2[i]['pass?'],[True,False])
    
    
    def test_rms_fail(self):
        """
        Unit tests for the rmsFail method
        """
        
        # Determine expected normalized root mean square answers
        exp_ans = [np.array([0.0,0.25]),
                   np.array([0.0,0.53033008588991]),
                   np.array([0.0,0.60908337097702])]
        
        # Loop through each discipline
        for i in range(0, len(self.Discips2)):
            
            # Check if calculated NRMSD is almost equal to expected values
            np.testing.assert_array_almost_equal\
                (self.Discips2[i]['Fail_Amount'], exp_ans[i])
    
    
    def test_get_output_diff(self):
        """
        Unit tests for the outputDiff function
        """
        
        # Determine expected (normalized) outputDiff values
        exp_ans = [np.array([float(0.1/0.4)]),
                   np.array([np.nan, float(0.6/0.8)]),
                   np.array([float(0.4/0.6), float(0.6/1.1)])]
        
        # Loop through each discipline
        for i in range(0, len(self.Discips2)):
            
            # Get output rules of discipline
            output_rules = getConstraints(self.Discips2[i]['outs'],\
                                          self.Output_Rules)
            
            # Initialize a numpy vector the same length as the output rules
            tv_diff = np.zeros(len(output_rules))
            
            # Loop through each output rule of the discipline
            for rule in output_rules:
                
                # Call outputDiff function for output points first index only
                tv_diff[output_rules.index(rule)] = \
                    outputDiff(rule, 1, self.Discips2[i])
            
            # Check if tv_diff values almost equal to expected values
            np.testing.assert_array_almost_equal(tv_diff, exp_ans[i])
            
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_output_success)
unittest.TextTestRunner(verbosity=2).run(suite)