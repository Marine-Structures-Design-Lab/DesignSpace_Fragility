"""
SUMMARY:
Unit tests for the uniformGrid function from uniform_grid.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from uniform_grid import uniformGrid
import unittest
import numpy as np

"""
CLASSES
"""
class test_uniform_grid(unittest.TestCase):
    
    def test_uniform_grid(self):
        """
        Unit tests for the uniformGrid function
        """
        
        # Unit test for a 2-D design space
        point_array, point_amt = uniformGrid(9, 2)
        array = np.array([[0.0, 0.0],
                          [0.0, 0.5],
                          [0.0, 1.0],
                          [0.5, 0.0],
                          [0.5, 0.5],
                          [0.5, 1.0],
                          [1.0, 0.0],
                          [1.0, 0.5],
                          [1.0, 1.0]])
        np.testing.assert_array_equal(array, point_array)
        self.assertEqual(point_amt, 9)
        
        # Unit test for a 3-D design space
        point_array, point_amt = uniformGrid(30, 3)
        array = np.array([[0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.5],
                          [0.0, 0.0, 1.0],
                          [0.0, 0.5, 0.0],
                          [0.0, 0.5, 0.5],
                          [0.0, 0.5, 1.0],
                          [0.0, 1.0, 0.0],
                          [0.0, 1.0, 0.5],
                          [0.0, 1.0, 1.0],
                          [0.5, 0.0, 0.0],
                          [0.5, 0.0, 0.5],
                          [0.5, 0.0, 1.0],
                          [0.5, 0.5, 0.0],
                          [0.5, 0.5, 0.5],
                          [0.5, 0.5, 1.0],
                          [0.5, 1.0, 0.0],
                          [0.5, 1.0, 0.5],
                          [0.5, 1.0, 1.0],
                          [1.0, 0.0, 0.0],
                          [1.0, 0.0, 0.5],
                          [1.0, 0.0, 1.0],
                          [1.0, 0.5, 0.0],
                          [1.0, 0.5, 0.5],
                          [1.0, 0.5, 1.0],
                          [1.0, 1.0, 0.0],
                          [1.0, 1.0, 0.5],
                          [1.0, 1.0, 1.0]])
        np.testing.assert_array_equal(array, point_array)
        self.assertEqual(point_amt, 27)
    
   
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_uniform_grid)
unittest.TextTestRunner(verbosity=2).run(suite)