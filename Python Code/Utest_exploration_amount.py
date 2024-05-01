"""
SUMMARY:
Unit tests for the exploreSpace class from exploration_amount.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from exploration_amount import exploreSpace
import unittest

"""
CLASSES
"""
class test_exploration_amount(unittest.TestCase):      
    
    def test_fixed_explore(self):
        """
        Unit tests for the fixedExplore method
        """
        
        ind = exploreSpace(0,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),200)
        ind = exploreSpace(200,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),144)
        ind = exploreSpace(344,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),118)
        ind = exploreSpace(462,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),80)
        ind = exploreSpace(542,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),54)
        ind = exploreSpace(596,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),48)
        ind = exploreSpace(644,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),35)
        ind = exploreSpace(679,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),32)
        ind = exploreSpace(711,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),20)
        ind = exploreSpace(731,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),18)
        ind = exploreSpace(811,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),8)
        ind = exploreSpace(995,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),5)
        ind = exploreSpace(1000,1000,[2,3,4])
        self.assertEqual(ind.fixedExplore(),1)
    
    # Other methods
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_exploration_amount)
unittest.TextTestRunner(verbosity=2).run(suite)