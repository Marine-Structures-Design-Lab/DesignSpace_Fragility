"""
SUMMARY:
Unit tests for the entropyTracker class from entropy_tracker.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from entropy_tracker import initializePF, timeHistory, reassignPF, evalEntropy
import unittest


"""
CLASSES
"""
class test_entropy_tracker(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables for functions and methods
        """
    
    
    def test_initialize_pf(self):
        """
        Unit tests for the initializePF function
        """
        
    
    def test_time_history(self):
        """
        Unit tests for the timeHistory function
        """
    
    
    def test_reassign_pf(self):
        """
        Unit tests for the reassignPF function
        """
    
    
    def test_eval_entropy(self):
        """
        Unit tests for the evalEntropy function
        """
        
        
        
        
        
        
    

"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_entropy_tracker)
unittest.TextTestRunner(verbosity=2).run(suite)