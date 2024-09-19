"""
SUMMARY:
Unit tests for the functions in connect_perceptions.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from connect_perceptions import connectPerceptions, padData, prepareTrain
import unittest
import sympy as sp
import numpy as np


"""
CLASSES
"""
class test_connect_perceptions(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables and object call for functions
        """
        
        # Set seed for random values
        np.random.seed(0)
        
        # Initialize sympy design variables
        self.x = sp.symbols('x1:8')
        
        # Initialize tested and space remaining data for multiple disciplines
        self.Discips = [
            {'tested_ins': np.ones((10, 3)),
             'ins': [self.x[0], self.x[1], self.x[2]],
             'space_remaining': np.full((20, 3), 0.95),
             'Fail_Amount': np.full((10,), 0.45),
             'Pass_Amount': np.zeros(10)},
            {'tested_ins': np.full((8, 3), 0.5),
             'ins': [self.x[2], self.x[3], self.x[4]],
             'space_remaining': np.full((30, 3), 0.85),
             'Fail_Amount': np.full((8,), 0.35),
             'Pass_Amount': np.zeros(8)},
            {'tested_ins': np.zeros((5, 4)),
             'ins': [self.x[0], self.x[4], self.x[5], self.x[6]],
             'space_remaining': np.full((15, 4), 0.75),
             'Fail_Amount': np.full((5,), 0.25),
             'Pass_Amount': np.zeros(5)}
        ]
        
        # Initialize tested and space remaining data for more disciplines
        self.Discips2 = [
            {'tested_ins': np.random.rand(100, 3),
             'ins': [self.x[0], self.x[1], self.x[2]],
             'space_remaining': np.random.uniform(0, 1, (20000, 3)),
             'Fail_Amount': np.random.uniform(-2, 2, size=100),
             'Pass_Amount': np.random.uniform(-2, 2, size=100)},
            {'tested_ins': np.random.rand(80, 3),
             'ins': [self.x[2], self.x[3], self.x[4]],
             'space_remaining': np.random.uniform(0, 1, (30000, 3)),
             'Fail_Amount': np.random.uniform(-2, 2, size=80),
             'Pass_Amount': np.random.uniform(-2, 2, size=80)},
            {'tested_ins': np.random.rand(50, 4),
             'ins': [self.x[0], self.x[4], self.x[5], self.x[6]],
             'space_remaining': np.random.uniform(0, 1, (25000, 4)),
             'Fail_Amount': np.random.uniform(-2, 2, size=50),
             'Pass_Amount': np.random.uniform(-2, 2, size=50)}
        ]
        
        
    def test_pad_data(self):
        """
        Unit tests for the padData function
        """
        
        # Execute function for two different disciplines
        x_padded1 = padData(self.Discips[0]['tested_ins'], 4)
        x_padded2 = padData(self.Discips[2]['tested_ins'], 4)
        
        # Determine expected arrays
        exp_x_padded1 = np.hstack([np.ones((10, 3)), np.zeros((10, 1))])
        exp_x_padded2 = np.zeros((5, 4))
        
        # Check if actual arrays match up with expected arrays
        np.testing.assert_array_almost_equal(x_padded1, exp_x_padded1)
        np.testing.assert_array_almost_equal(x_padded2, exp_x_padded2)
    
    
    def test_prepare_train(self):
        """
        Unit tests for the prepareTrain function
        """
        
        # Determine number of design variables in discipline with the most
        target_dim = max([len(discip['ins'])+1 for discip in self.Discips])
        
        # Execute function for list of disciplines
        X, Y, scalers_x = prepareTrain(self.Discips, target_dim)
        
        # Determine expected x- and y-training arrays
        exp_X = [
            np.hstack([np.zeros((10,1)),np.ones((10,3)),np.zeros((10,1))]), 
            np.hstack([np.ones((8,1)),np.full((8,3), 0.5),np.zeros((8,1))]), 
            np.hstack([np.full((5,1), 2.),np.zeros((5,4))])
        ]
        exp_Y = [
            np.zeros((10,1)) - np.full((10,1), 0.45),
            np.zeros((8,1)) - np.full((8,1), 0.35),
            np.zeros((5,1)) - np.full((5,1), 0.25)
        ]
        
        # Ensure lists are proper lengths
        self.assertEqual(len(X), 3)
        self.assertEqual(len(Y), 3)
        self.assertEqual(len(scalers_x), 3)
        
        # Ensure x-training and y-training arrays are correct
        for i in range(0, len(exp_X)):
            X[i][:,1:len(self.Discips[i]['ins'])+1] = scalers_x[i].\
                inverse_transform(X[i][:,1:len(self.Discips[i]['ins'])+1])
            np.testing.assert_array_almost_equal(X[i], exp_X[i])
            np.testing.assert_array_almost_equal(Y[i], exp_Y[i])
    
    
    def test_connect_perceptions(self):
        """
        Unit tests for the connectPerceptions function
        """
        
        # Execute the function
        pf_fragility, pf_std_fragility = connectPerceptions(self.Discips2)
        
        # Ensure that pass-fail lists are the proper length
        self.assertEqual(len(pf_fragility), 3)
        self.assertEqual(len(pf_std_fragility), 3)
        
        # Check that all of the predictions are between -1 and +1 and all the
        ### standard deviations of the predictions are positive
        for pf, pf_std in zip(pf_fragility, pf_std_fragility):
            self.assertTrue(np.all(pf >= -1.0) and np.all(pf <= 1.0))
            self.assertTrue(np.all(pf_std > 0.0))
        
        
        
        # Ensure pass-fail predictions all fall between -1 and +1



"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_connect_perceptions)
unittest.TextTestRunner(verbosity=2).run(suite)