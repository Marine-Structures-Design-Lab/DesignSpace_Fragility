"""
SUMMARY:
Unit tests for the ruleCheck function from rule_check.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from rule_check import ruleCheck
import unittest

"""
CLASSES
"""
class test_rule_check(unittest.TestCase):
    
    def setUp(self):
        """
        Established nested boolean lists for testing
        """
        self.list1 = [[[True,True],[True]],[[True,True]]]
        self.list2 = [[[False,False],[True]],[[True,True]]]
        self.list3 = [[[True,True],[False]],[[True,True]]]
        self.list4 = [[[False,True],[False]],[[True,True]]]
        self.list5 = [[[True,True],[True]],[[True,False]]]
        self.list6 = [[[False,False],[False]],[[False,False]]]
        
    def test_rule_check(self):
        """
        Unit test for the ruleCheck function
        """
        self.assertTrue(ruleCheck(self.list1))
        self.assertTrue(ruleCheck(self.list2))
        self.assertTrue(ruleCheck(self.list3))
        self.assertFalse(ruleCheck(self.list4))
        self.assertFalse(ruleCheck(self.list5))
        self.assertFalse(ruleCheck(self.list6))
           
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_rule_check)
unittest.TextTestRunner(verbosity=2).run(suite)