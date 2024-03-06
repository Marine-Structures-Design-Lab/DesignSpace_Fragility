"""
SUMMARY:
Unit tests for the functions from organize_data.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from organize_data import countBooleans
import unittest
import numpy as np


"""
CLASSES
"""
class test_organize_data(unittest.TestCase):

    def setUp(self):
        """
        
        """
    
    
    def test_shared_indices(self):
        """
        Unit tests for the sharedIndices function
        """
        
        # Create a larger numpy array
        larger_array = np.array([[0.1, 0.0, 0.3],
                                 [0.0, 0.0, 1.0],
                                 [0.5, 0.5, 0.5],
                                 [5.3, 6.6, -0.7],
                                 [0.3, 0.1, 0.2],
                                 [0.7, 0.7, 0.6],
                                 [0.1, 0.2, 0.9],
                                 [0.8, 0.1, 0.2]])
        
        # Create a smaller numpy array
        smaller_array  = np.array([[]])
        
        
        # Create an empty numpy array
        
        
        # Determine the expected index lists
        
        
        # Check that expected index lists match actual index lists
    
    
    def test_count_booleans(self):
        """
        Unit tests for the countBooleans function
        """
        
        # Create a list of integers corresponding to specific boolean values
        index_list = [0, 3, 4, 6, 2]
        
        # Create a list of boolean values
        bool_list = [True, False, True, False, False, False, True, False, True]
        
        # Determine the expected true count
        exp_ans = 3
        
        # Run the function
        true_count = countBooleans(index_list, bool_list)
        
        # Check that expected true count matches actual true count
        self.assertEqual(true_count, exp_ans)
        
    
    def test_fill_space_remaining(self):
        """
        Unit tests for the fillSpaceRemaning method
        """
    
    
    def test_find_averages(self):
        """
        Unit tests for the findAverages method
        """
    
    
    def test_find_percentages(self):
        """
        Unit tests for the findPercentages method
        """
    
    
    
    
    
    
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_organize_data)
unittest.TextTestRunner(verbosity=2).run(suite)