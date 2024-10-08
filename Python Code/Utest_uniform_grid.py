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
from vars_def import setProblem
import unittest
import numpy as np


"""
CLASSES
"""
class test_uniform_grid(unittest.TestCase):
    
    def setUp(self):
        """
        Establishes input rules for testing
        """
        
        # Create an object and call each method
        prob = setProblem()
        self.Discips, self.ir, Output_rules = prob.SBD1()
        self.Discips2, self.ir2, Output_rules = prob.SenYang()
        
        
    def test_uniform_grid(self):
        """
        Unit tests for the uniformGrid function
        """
        
        # Unit test for a 3-D design space
        point_array, point_amt, index_list = \
            uniformGrid(30, self.Discips[1]['ins'], self.ir)
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
        exp_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                    17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        np.testing.assert_array_equal(array, point_array)
        self.assertEqual(point_amt, 27)
        self.assertListEqual(index_list, exp_list)
        
        # Unit test for a 6-D design space
        point_array, point_amt, index_list = \
            uniformGrid(60, self.Discips2[0]['ins'], self.ir2)
        array = np.array([[0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0, 0.0, 1.0],
                          [0.0, 0.0, 1.0, 1.0, 0.0, 0.0]])
        exp_list = [0, 1, 2]
        np.testing.assert_array_equal(array, point_array)
        self.assertEqual(point_amt, 3)
        self.assertListEqual(index_list, exp_list)
    
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_uniform_grid)
unittest.TextTestRunner(verbosity=2).run(suite)