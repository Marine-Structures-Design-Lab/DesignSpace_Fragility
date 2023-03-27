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
        ind = exploreSpace(0,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),20)
        ind = exploreSpace(20,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),14)
        ind = exploreSpace(35,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),9)
        ind = exploreSpace(50,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),6)
        ind = exploreSpace(60,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),4)
        ind = exploreSpace(70,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),4)
        ind = exploreSpace(80,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),4)
        ind = exploreSpace(90,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),4)
        ind = exploreSpace(96,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),4)
        ind = exploreSpace(97,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),3)
        ind = exploreSpace(98,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),2)
        ind = exploreSpace(99,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),1)
        ind = exploreSpace(100,100,[2,3,4])
        self.assertEqual(ind.fixedExplore(),0)
    
    # Other methods
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_exploration_amount)
unittest.TextTestRunner(verbosity=2).run(suite)