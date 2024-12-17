"""
SUMMARY:
Unit tests for the gfDecider class from gf_decision.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from gf_decision import gfDecider
import unittest


"""
CLASSES
"""
class test_gf_decision(unittest.TestCase):
    
    def test_fixed(self):
        """
        Unit tests for the Fixed method
        """
        
        # Create gradient factor decision coefficients
        gf_decide = {
            "strategy": "Fixed",
            "coefficients": [0.3]
        }
        
        # Set different gradient factor values
        gradient_factor1 = 0.31
        gradient_factor2 = 0.29
        
        # Set current and maximum time iterations
        iters = 100
        iters_max = 200
        
        # Create object calls
        gradfact1 = gfDecider(gf_decide['coefficients'], 
                              gradient_factor1, iters, iters_max)
        gradfact2 = gfDecider(gf_decide['coefficients'],
                              gradient_factor2, iters, iters_max)
        
        # Call gradient factor decision strategy
        break_loop1 = getattr(gradfact1, gf_decide['strategy'])()
        break_loop2 = getattr(gradfact2, gf_decide['strategy'])()
        
        # Check whether gf decision strategy results meet expected results
        self.assertTrue(break_loop1)
        self.assertFalse(break_loop2)
        
    
    def test_linear(self):
        """
        Unit tests for the Linear method
        """
        
        # Create gradient factor decision coefficients
        gf_decide = {
            "strategy": "Linear",
            "coefficients": [-0.006, 0.6]
        }
        
        # Set different gradient factor values
        gradient_factor1 = 0.31
        gradient_factor2 = 0.29
        
        # Set current and maximum time iterations
        iters = 100
        iters_max = 200
        
        # Create object calls
        gradfact1 = gfDecider(gf_decide['coefficients'], 
                              gradient_factor1, iters, iters_max)
        gradfact2 = gfDecider(gf_decide['coefficients'],
                              gradient_factor2, iters, iters_max)
        
        # Call gradient factor decision strategy
        break_loop1 = getattr(gradfact1, gf_decide['strategy'])()
        break_loop2 = getattr(gradfact2, gf_decide['strategy'])()
        
        # Check whether gf decision strategy results meet expected results
        self.assertTrue(break_loop1)
        self.assertFalse(break_loop2)
    
    
    def test_quadratic(self):
        """
        Unit tests for the Quadratic method
        """
        
        # Create gradient factor decision coefficients
        gf_decide = {
            "strategy": "Quadratic",
            "coefficients": [0.00009, 100, 0]
        }
        
        # Set different gradient factor values
        gradient_factor1 = 0.00226
        gradient_factor2 = 0.00224
        
        # Set current and maximum time iterations
        iters = 190
        iters_max = 200
        
        # Create object calls
        gradfact1 = gfDecider(gf_decide['coefficients'], 
                              gradient_factor1, iters, iters_max)
        gradfact2 = gfDecider(gf_decide['coefficients'],
                              gradient_factor2, iters, iters_max)
        
        # Call gradient factor decision strategy
        break_loop1 = getattr(gradfact1, gf_decide['strategy'])()
        break_loop2 = getattr(gradfact2, gf_decide['strategy'])()
        
        # Check whether gf decision strategy results meet expected results
        self.assertTrue(break_loop1)
        self.assertFalse(break_loop2)
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_gf_decision)
unittest.TextTestRunner(verbosity=2).run(suite)