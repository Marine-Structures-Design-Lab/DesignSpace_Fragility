"""
Created on Thu Mar 23 13:28:22 2023

@author: joeyv
"""

"""
LIBRARIES
"""
import unittest
from exploration_amount import exploreSpace as expoS

"""
CLASSES
"""
class test_exploration_amount(unittest.TestCase):
    
    def setUp(self):
        
        ind = expoS.exploreSpace(0,100,[2,3,4])
    
    def test_fixed_explore(self):
        
        self.assertEqual(ind.fixedExplore(),20)
        

"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_exploration_amount)
unittest.TextTestRunner(verbosity=2).run(suite)