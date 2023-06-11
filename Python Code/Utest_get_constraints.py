"""
SUMMARY:
Unit tests for the functions from get_constraints.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from get_constraints import getConstraints, getInequalities, extractInequality
from vars_def import setProblem
from create_key import createDict
import unittest
import sympy as sp
import numpy as np

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
        self.y = sp.symbols('y1:6')
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Create a key for the output rule inequalities
            self.Discips[i] = createDict('out_ineqs',self.Discips[i])
    
    
    def test_get_constaints(self):
        """
        Unit tests for the getConstraints function
        """
        
        # Check input rules for discipline 1
        self.assertEqual(getConstraints(self.Discips[0]['ins'],\
                                        self.Input_Rules),\
                         [self.Input_Rules[0],\
                          self.Input_Rules[1],\
                          self.Input_Rules[2]])
        
        # Check input rules for discipline 2
        self.assertEqual(getConstraints(self.Discips[1]['ins'],\
                                        self.Input_Rules),\
                         [self.Input_Rules[2],\
                          self.Input_Rules[3],\
                          self.Input_Rules[4]])
        
        # Check input rules for discipline 3
        self.assertEqual(getConstraints(self.Discips[2]['ins'],\
                                        self.Input_Rules),\
                         [self.Input_Rules[0],\
                          self.Input_Rules[4],\
                          self.Input_Rules[5]])
        
        # Check output rules for discipline 1
        self.assertEqual(getConstraints(self.Discips[0]['outs'],\
                                        self.Output_Rules),\
                         [self.Output_Rules[0]])
        
        # Check output rules for discipline 2
        self.assertEqual(getConstraints(self.Discips[1]['outs'],\
                                        self.Output_Rules),\
                         [self.Output_Rules[1],\
                          self.Output_Rules[2]])
        
        # Check output rules for discipline 3
        self.assertEqual(getConstraints(self.Discips[2]['outs'],\
                                        self.Output_Rules),\
                         [self.Output_Rules[3],\
                          self.Output_Rules[4]])
    
    
    def test_get_Inequalities(self):
        """
        Unit tests for the getInequalities function
        """
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Determine the output rules for each discipline
            output_rules =\
                getConstraints(self.Discips[i]['outs'],self.Output_Rules)
                
            # Gather any new inequalities of relevance to the discipline
            self.Discips[i] =\
                getInequalities(self.Discips[i],output_rules,'out_ineqs')
            
        # Check inequalities and length for discipline 1
        required_keys =\
            [self.y[0]>=0.0,self.y[0]<=0.4,self.y[0]>=1.2,self.y[0]<=1.6]
        for key in required_keys:
            self.assertIn(key,self.Discips[0]['out_ineqs'])
        self.assertEqual(len(self.Discips[0]['out_ineqs']),len(required_keys))
        
        # Check inequalities and length for discipline 2
        required_keys =\
            [self.y[1]>=0.5,self.y[1]<=0.7,self.y[2]>=0.2,self.y[2]<=0.5]
        for key in required_keys:
            self.assertIn(key,self.Discips[1]['out_ineqs'])
        self.assertEqual(len(self.Discips[1]['out_ineqs']),len(required_keys))
        
        # Check inequalities and length for discipline 3
        required_keys =\
            [self.y[3]>=0.0,self.y[3]<=0.5,self.y[4]>=0.8,self.y[4]<=1.6]
        for key in required_keys:
            self.assertIn(key,self.Discips[2]['out_ineqs'])
        self.assertEqual(len(self.Discips[2]['out_ineqs']),len(required_keys))
        
        # Add an array of zeros to discipline 1's dictionary for first key
        self.Discips[0]['out_ineqs'][self.y[0]>=0.0] = np.zeros((2,2))
        
        # Call the getInequalities function again for discipline 1
        output_rules =\
            getConstraints(self.Discips[0]['outs'],self.Output_Rules)
        self.Discips[0] =\
            getInequalities(self.Discips[0],output_rules,'out_ineqs')
        
        # Check values from y[0]>=0.0 key of discipline 1 were not overwritten
        np.testing.assert_array_equal\
            (self.Discips[0]['out_ineqs'][self.y[0]>=0.0],np.zeros((2,2)))
        
        
    def test_extract_inequality(self):
        
        # Initialize sympy symbols
        x = sp.symbols('x1:4')
        
        # Create rules for which inequalities are extracted
        rule1 = x[0] < 0.5
        rule2 = sp.Or(x[1] < 0.5, x[2] > 0.5, x[0] < 0.5, x[1] > 0.8)
        rule3 = sp.And(sp.Or(x[1] < 0.5, x[2] > 0.5), x[0] < 0.5)
        
        # Call extractInequality on each rule
        act_list1 = extractInequality(rule1)
        act_list2 = extractInequality(rule2)
        act_list3 = extractInequality(rule3)
        
        # Establish the expected rules/lists
        exp_list1 = x[0] < 0.5
        exp_list2 = [x[1] < 0.5, x[2] > 0.5, x[0] < 0.5, x[1] > 0.8]
        exp_list3 = [[x[2] > 0.5, x[1] < 0.5], x[0] < 0.5]
        
        # Check that the actual lists match the expected lists
        self.assertEqual(act_list1, exp_list1)
        self.assertCountEqual(act_list2, exp_list2)
        self.assertCountEqual(act_list3, exp_list3)
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_get_constraints)
unittest.TextTestRunner(verbosity=2).run(suite)