"""
SUMMARY:
Unit tests for the getConstraints function from get_constraints.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from get_constraints import getConstraints
from vars_def import setProblem
import unittest

"""
CLASSES
"""
class test_get_constraints(unittest.TestCase):

    def setUp(self):
        """
        Establish a list of dictionaries for each discipline and a list of
        rules that are object definitions
        """
        
        prob = setProblem()
        self.Discips, self.Input_Rules, self.Output_Rules = prob.SBD1()
    
    def test_get_constaints(self):
        """
        Unit tests for the getConstraints function
        """
        
        self.assertEqual(getConstraints(self.Discips[0]['ins'],\
                                        self.Input_Rules),\
                         [self.Input_Rules[0],\
                          self.Input_Rules[1],\
                          self.Input_Rules[2]])
        
        self.assertEqual(getConstraints(self.Discips[1]['ins'],\
                                        self.Input_Rules),\
                         [self.Input_Rules[2],\
                          self.Input_Rules[3],\
                          self.Input_Rules[4]])
        
        self.assertEqual(getConstraints(self.Discips[2]['ins'],\
                                        self.Input_Rules),\
                         [self.Input_Rules[0],\
                          self.Input_Rules[4],\
                          self.Input_Rules[5]])
        
        self.assertEqual(getConstraints(self.Discips[0]['outs'],\
                                        self.Output_Rules),\
                         [self.Output_Rules[0]])
        
        self.assertEqual(getConstraints(self.Discips[1]['outs'],\
                                        self.Output_Rules),\
                         [self.Output_Rules[1],\
                          self.Output_Rules[2]])
        
        self.assertEqual(getConstraints(self.Discips[2]['outs'],\
                                        self.Output_Rules),\
                         [self.Output_Rules[3],\
                          self.Output_Rules[4]])
    
    def test_get_Inequalities(self):
        """
        Unit tests for the getInequalities function
        """
        
        return
    
    def test_extract_inequality(self):
        """
        Unit tests for the extract_inequality nested function
        """
        
        return

"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_get_constraints)
unittest.TextTestRunner(verbosity=2).run(suite)