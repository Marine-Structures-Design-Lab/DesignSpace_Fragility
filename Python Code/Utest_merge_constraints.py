"""
SUMMARY:
Unit tests for the mergeConstraints class from merge_constraints.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from merge_constraints import mergeConstraints
import unittest
import sympy as sp

"""
CLASSES
"""
class test_merge_constraints(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables to be used by multiple test methods
        """
        
        # Initialize sympy variables
        self.x = sp.symbols('x1:4')
        x = self.x
        
        # Initialize objects for noncontradictory rule lists
        self.noncon_list1 = [x[0] < 0.5, x[0] < 0.7]
        self.noncon_list2 = [x[0] < 0.5, sp.Or(x[0] > 0.5, x[1] < 0.5)]
        self.noncon_list3 = [sp.Or(x[1] > 0.5, x[2] > 0.5), 
                             sp.Or(x[1] < 0.5, x[2] < 0.5)]
        self.noncon_list4 = [x[2] >= 0.5, x[2] <= 0.5]
        
        # Initialize objects for contradictory rule lists
        self.con_list1 = [x[0] < 0.5, x[0] > 0.5]
        self.con_list2 = [x[0] < 0.5, x[0] > 0.5, 
                          x[1] > 0.3, x[1] <= 0.3, 
                          x[2] > 0.5]
        self.con_list3 = [x[0] < 0.5, x[0] > 0.5, 
                          sp.Or(x[0] > 0.5, x[2] < 0.5)]
        self.con_list4 = [sp.And(x[0] < 0.5, x[1] < 0.5),
                          sp.And(x[0] > 0.5, x[1] < 0.5)]
        
        
        
    def test_remove_contradiction(self):
        """
        Unit tests for the removeContradiction method
        """
        
        # Initialize sympy variables
        x = self.x
        
        # Test noncontradictory rule lists
        mc = mergeConstraints(self.noncon_list1)
        list1 = mc.removeContradiction()
        self.assertEqual(self.noncon_list1, list1)
        
        mc = mergeConstraints(self.noncon_list2)
        list2 = mc.removeContradiction()
        self.assertEqual(self.noncon_list2, list2)
        
        mc = mergeConstraints(self.noncon_list3)
        list3 = mc.removeContradiction()
        self.assertEqual(self.noncon_list3, list3)
        
        mc = mergeConstraints(self.noncon_list4)
        list4 = mc.removeContradiction()
        self.assertEqual(self.noncon_list4, list4)
        
        
        # Test contradictory rule lists
        mc = mergeConstraints(self.con_list1)
        list1 = mc.removeContradiction()
        exp_list1 = []
        self.assertEqual(list1, exp_list1)
        
        mc = mergeConstraints(self.con_list2)
        list2 = mc.removeContradiction()
        exp_list2 = [x[2] > 0.5]
        self.assertEqual(list2, exp_list2)
        
        mc = mergeConstraints(self.con_list3)
        list3 = mc.removeContradiction()
        exp_list3 = [sp.Or(x[0] > 0.5, x[2] < 0.5)]
        self.assertEqual(list3, exp_list3)
        
        mc = mergeConstraints(self.con_list4)
        list4 = mc.removeContradiction()
        exp_list4 = []
        self.assertEqual(list4, exp_list4)
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_merge_constraints)
unittest.TextTestRunner(verbosity=2).run(suite)