"""
SUMMARY:
Unit tests for the outputStart function from output_start.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_start import outputStart
import unittest
import numpy as np

"""
CLASSES
"""
class test_output_start(unittest.TestCase):
    
    def test_output_start(self):
        """
        Unit tests for the outputStart function
        """
        
        # Create disciplines with an empty key and two filled keys
        discip_empty = {'key': []}
        discip_filled1 = {'key': np.ones(5)}
        discip_filled2 = {'key': np.ones((8, 4))}
        
        # Execute the outputStart function on each discipline
        start_empty = outputStart(discip_empty, 'key')
        start_filled1 = outputStart(discip_filled1, 'key')
        start_filled2 = outputStart(discip_filled2, 'key')
        
        # Check that correct starting indices are returned
        self.assertEqual(start_empty, 0)
        self.assertEqual(start_filled1, 5)
        self.assertEqual(start_filled2, 8)
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_output_start)
unittest.TextTestRunner(verbosity=2).run(suite)