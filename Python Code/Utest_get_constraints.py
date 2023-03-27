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
import sympy as sp
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
        self.Discips, self.Rules = getattr(prob,'SBD1')()
    
    def test_get_constaints(self):
        """
        Unit tests for the getConstraints function (and, by effect, breakup()
        method of the varRule class)
        """
        # Each discipline's rules at the starting point
        self.assertEqual(getConstraints(self.Discips[0]['ins'],self.Rules),\
                         [self.Rules[0].breakup(),\
                          self.Rules[1].breakup(),\
                          self.Rules[2].breakup()])
        self.assertEqual(getConstraints(self.Discips[1]['ins'],self.Rules),\
                         [self.Rules[2].breakup(),\
                          self.Rules[3].breakup(),\
                          self.Rules[4].breakup()])
        self.assertEqual(getConstraints(self.Discips[2]['ins'],self.Rules),\
                         [self.Rules[0].breakup(),\
                          self.Rules[4].breakup(),\
                          self.Rules[5].breakup()])
        self.assertEqual(getConstraints(self.Discips[0]['outs'],self.Rules),\
                         [self.Rules[6].breakup()])
        self.assertEqual(getConstraints(self.Discips[1]['outs'],self.Rules),\
                         [self.Rules[7].breakup(),\
                          self.Rules[8].breakup()])
        self.assertEqual(getConstraints(self.Discips[2]['outs'],self.Rules),\
                         [self.Rules[9].breakup(),\
                          self.Rules[10].breakup()])
        
        # A couple random tests of various variables with the original rules
        self.assertEqual(getConstraints(sp.symbols('x1,x6,y3'),self.Rules),\
                         [self.Rules[0].breakup(),\
                          self.Rules[5].breakup(),\
                          self.Rules[8].breakup()])
        self.assertEqual(getConstraints(sp.symbols\
                        ('x1,x2,x3,x4,x5,x6,y1,y2,y3,y4,y5'),self.Rules),\
                         [self.Rules[0].breakup(),\
                          self.Rules[1].breakup(),\
                          self.Rules[2].breakup(),\
                          self.Rules[3].breakup(),\
                          self.Rules[4].breakup(),\
                          self.Rules[5].breakup(),\
                          self.Rules[6].breakup(),\
                          self.Rules[7].breakup(),\
                          self.Rules[8].breakup(),\
                          self.Rules[9].breakup(),\
                          self.Rules[10].breakup()])
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_get_constraints)
unittest.TextTestRunner(verbosity=2).run(suite)