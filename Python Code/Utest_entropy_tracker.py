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
from entropy_tracker import entropyTracker, initializePF, timeHistory, \
    reassignPF, minmaxNormalize, initializeWR, assignWR
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
        
        
        
        
        
        
    

"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_entropy_tracker)
unittest.TextTestRunner(verbosity=2).run(suite)