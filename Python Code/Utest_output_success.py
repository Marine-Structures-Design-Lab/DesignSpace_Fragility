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
import sympy as sp
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
        
        ########## TESTS FOR SBD1 ##########
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
            
            # Create key for output rule inequalities relevant to discipline
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
            self.Discips2[i] = createNumpy('Pass_Amount',self.Discips2[i])
            
            # Produce new discipline
            self.Discips1[i] = outchk.basicCheck()
            self.Discips2[i] = outchk2.basicCheck()
            
            # Determine the extent to which points pass or fail
            self.Discips2[i] = outchk2.rmsFail()
        
        
        ########## TESTS FOR NEW OUTPUT SPACE ##########
        # Create sympy output variables
        y = sp.symbols('y1:3')
        
        # Create new discipline and output rules
        self.Discipline = [{"outs": [y[0], y[1]]}]
        self.ORules = [y[0] > 0.1,
                       sp.Or(y[0] > 0.25, y[1] > 0.3),
                       sp.And(y[1] > 0.2, y[1] < 0.6),
                       y[0] + y[1] < 1]
        
        # Add output values to new discipline's dictionary
        self.Discipline[0]['tested_outs'] = np.array([[0.35, 0.35],
                                                      [0.90, 0.90],
                                                      [0.06, 0.10],
                                                      [0.60, 0.05],
                                                      [0.17, 0.53],
                                                      [0.29, 0.24]])
        
        # Create needed keys
        self.Discipline[0] = createKey('pass?', self.Discipline[0])
        
        # Create a key for the output rule inequalities relevant to discipline
        self.Discipline[0] = createDict('out_ineqs', self.Discipline[0])
        
        # Get output rules
        output_rules = getConstraints(self.Discipline[0]['outs'], self.ORules)
        
        # Gather any new inequalities of relevance to the discipline
        self.Discipline[0] =\
            getInequalities(self.Discipline[0], output_rules, 'out_ineqs')
        
        # Calculate left-hand side of output rule inequality for each point
        self.Discipline[0]['out_ineqs'] =\
            calcRules(self.Discipline[0], 'out_ineqs', 'tested_outs', 'outs')
        
        # Initialize object for discipline
        outchk = checkOutput(self.Discipline[0], output_rules)
        
        # Create a key for extent of passing/failing if it does not exist
        self.Discipline[0] = createNumpy('Fail_Amount', self.Discipline[0])
        self.Discipline[0] = createNumpy('Pass_Amount', self.Discipline[0])
        
        # Produce new discipline
        self.Discipline[0] = outchk.basicCheck()
        
        # Determine the extent to which points pass or fail
        self.Discipline[0] = outchk.rmsFail()
        
        
    def test_basic_check(self):
        """
        Unit tests for the basicCheck method
        """
        
        ########## TESTS FOR SBD1 ##########
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
        
            # Check that there is NOT rewriting of previous "pass?" values
            self.assertEqual(self.Discips1[i]['pass?'][0],None)
            
            # Check that there is determination of new "pass?" values
            self.assertTrue(len(self.Discips1[i]['pass?']) == 2)
            
            # Check that the pass? values produced are correct
            self.assertListEqual(self.Discips2[i]['pass?'], [True,False])
    
    
        ########## TESTS FOR NEW OUTPUT SPACE ##########
        # Check that the pass? values produced are correct
        self.assertListEqual(self.Discipline[0]['pass?'], 
                             [True, False, False, False, True, True])
    
    
    def test_rms_fail(self):
        """
        Unit tests for the rmsFail method
        """
        
        ########## TESTS FOR SBD1 ##########
        # Determine expected normalized root mean square fail amounts
        fail_ans = [np.array([0.0, 0.25]),
                    np.array([0.0, 0.53033008588991]),
                    np.array([0.0, 0.60908337097702])]
        
        # Determine expected pass amounts
        pass_ans = [np.array([0.25, 0.0]),
                    np.array([0.1, 0.0]),
                    np.array([0.272727272727, 0.0])]
        
        # Loop through each discipline
        for i in range(0, len(self.Discips2)):
            
            # Check if calculated fail amounts match expected values
            np.testing.assert_array_almost_equal\
                (self.Discips2[i]['Fail_Amount'], fail_ans[i])
            
            # Check if calculated pass amounts match expected values
            np.testing.assert_array_almost_equal\
                (self.Discips2[i]['Pass_Amount'], pass_ans[i])
        
        
        ########## TESTS FOR NEW OUTPUT SPACE ##########
        # Determine expected normalized root mean square fail amounts
        fail_ans = np.array([0.0,
                             0.3010486145,
                             0.1296828204,
                             0.0882352941,
                             0.0,
                             0.0])
        
        # Determine expected pass amounts
        pass_ans = np.array([0.119047619,
                             0.0,
                             0.0,
                             0.0,
                             0.0823529412,
                             0.0470588235])
        
        # Check if calculated fail amounts are almost equal to expected values
        np.testing.assert_array_almost_equal\
            (self.Discipline[0]['Fail_Amount'], fail_ans)
        
        # Check if calculated pass amounts are almost equal to expected values
        np.testing.assert_array_almost_equal\
            (self.Discipline[0]['Pass_Amount'], pass_ans)
    
    
    def test_get_output_diff(self):
        """
        Unit tests for the outputDiff function
        """
        
        ########## TESTS FOR SBD1 ##########
        # Determine expected (normalized) outputDiff values
        exp_ans = [np.array([float(0.1/0.4)]),
                   np.array([0.0, float(0.6/0.8)]),
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
        
        
        ########## TESTS FOR NEW OUTPUT SPACE ##########
        # Determine expected (normalized) outputDiff values
        exp_ans = [np.array([float(0.25/0.84), float(0.1/0.84),
                             float(0.15/0.85), float(0.3/1.64)]),
                   np.array([0.0, 0.0,
                             float(0.3/0.85), float(0.8/1.64)]),
                   np.array([float(0.04/0.84), float(0.19/0.84),
                             float(0.1/0.85), 0.0]),
                   np.array([0.0, 0.0,
                             float(0.15/0.85), 0.0]),
                   np.array([float(0.07/0.84), float(0.23/0.85),
                             float(0.07/0.85), float(0.3/1.64)]),
                   np.array([float(0.19/0.84), float(0.04/0.84),
                             float(0.04/0.85), float(0.47/1.64)])]
        
        # Get output rules of discipline
        output_rules = getConstraints(self.Discipline[0]['outs'],\
                                      self.ORules)
        
        # Initialize a numpy vector the same length as the output rules
        tv_diff = np.zeros(len(output_rules))
        
        # Loop through each index of the discipline
        for ind in range(0, self.Discipline[0]['tested_outs'].shape[0]):
            
            # Loop through each output rule of the discipline
            for rule in output_rules:
            
                # Call outputDiff function for output points
                tv_diff[output_rules.index(rule)] = \
                    outputDiff(rule, ind, self.Discipline[0])
                
            # Check if tv_diff values almost equal to expected values
            np.testing.assert_array_almost_equal(tv_diff, exp_ans[ind])
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_output_success)
unittest.TextTestRunner(verbosity=2).run(suite)