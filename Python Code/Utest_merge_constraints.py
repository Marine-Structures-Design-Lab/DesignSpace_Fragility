"""
SUMMARY:
Unit tests for the mergeConstraints class from merge_constraints.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from merge_constraints import mergeConstraints, trainData, initializeFit, \
    predictData, analyzeInfeasibility, analyzeFeasibility, bezierPoint, \
    getOpinion
import unittest
import numpy as np
import sympy as sp

"""
CLASSES
"""
class test_merge_constraints(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables to be used by multiple test methods
        """
        
        # Initialize symbols
        x = sp.symbols('x1:4')
        
        # Create a discipline without eliminated data
        self.Discip1 = {
            "tested_ins": np.array([[0.1, 0.1, 0.1],
                                    [0.2, 0.3, 0.4],
                                    [0.5, 0.5, 0.9]]),
            "Fail_Amount": np.array([0.0, 0.5, 0.3]),
            "Pass_Amount": np.array([0.7, 0.0, 0.4]),
            "ins": [x[0], x[1], x[2]],
            "space_remaining": np.array([[0.2, 0.2, 0.2],
                                         [0.5, 0.2, 0.5],
                                         [0.9, 0.9, 0.2],
                                         [0.2, 0.3, 0.8],
                                         [0.8, 0.1, 0.9],
                                         [0.5, 0.2, 0.9]])
            }
        
        # Create another discipline with eliminated data
        self.Discip2 = {
            "tested_ins": np.array([[0.3, 0.2, 0.3],
                                    [0.5, 0.5, 0.5],
                                    [0.9, 0.1, 0.9],
                                    [0.7, 0.6, 0.5]]),
            "Fail_Amount": np.array([0.1, 0.0, 0.8, 0.0]),
            "Pass_Amount": np.array([0.0, 0.2, 0.9, 0.0]),
            "ins": [x[0], x[1], x[2]],
            "space_remaining": np.array([[0.4, 0.4, 0.4],
                                         [0.5, 0.4, 0.5],
                                         [0.3, 0.3, 0.4],
                                         [0.1, 0.7, 0.2],
                                         [0.5, 0.6, 0.1]]),
            "eliminated": {
                "tested_ins": np.array([[0.1, 0.1, 0.1],
                                        [0.2, 0.3, 0.4],
                                        [0.5, 0.5, 0.9]]),
                "Fail_Amount": np.array([0.0, 0.5, 0.3]),
                "Pass_Amount": np.array([0.7, 0.0, 0.4]),
                "space_remaining": np.array([[0.1, 0.4, 0.4],
                                             [0.7, 0.7, 0.2]])
                }
            }
    
    
    def test_train_data(self):
        """
        Unit tests for trainData function
        """
        
        # Execute trainData on both disciplines
        xtrain1, ytrain1 = trainData(self.Discip1)
        xtrain2, ytrain2 = trainData(self.Discip2)
        
        # Determine expected output for both disciplines
        exp_xtrain1 = np.array([[0.1, 0.1, 0.1],
                                [0.2, 0.3, 0.4],
                                [0.5, 0.5, 0.9]])
        exp_ytrain1 = np.array([0.7, -0.5, 0.1])
        exp_xtrain2 = np.array([[0.3, 0.2, 0.3],
                                [0.5, 0.5, 0.5],
                                [0.9, 0.1, 0.9],
                                [0.7, 0.6, 0.5],
                                [0.1, 0.1, 0.1],
                                [0.2, 0.3, 0.4],
                                [0.5, 0.5, 0.9]])
        exp_ytrain2 = np.array([-0.1, 0.2, 0.1, 0.0, 0.7, -0.5, 0.1])
        
        # Test that function is gathering all of the x and y data
        np.testing.assert_array_almost_equal(xtrain1, exp_xtrain1)
        np.testing.assert_array_almost_equal(ytrain1, exp_ytrain1)
        
        # Test that function is also gathering eliminated data if it exists
        np.testing.assert_array_almost_equal(xtrain2, exp_xtrain2)
        np.testing.assert_array_almost_equal(ytrain2, exp_ytrain2)
    
    
    def test_predict_data(self):
        """
        Unit tests for predictData function
        """
        
        # Organize x and y training data for both disciplines
        xtrain1, ytrain1 = trainData(self.Discip1)
        xtrain2, ytrain2 = trainData(self.Discip2)
        
        # Fit a GPR for both sets of training data
        gpr1 = initializeFit(self.Discip1, xtrain1, ytrain1)
        gpr2 = initializeFit(self.Discip2, xtrain2, ytrain2)
        
        # Establish indices for non-reduced, reduced, and leftover space
        diction1 = {
            "non_reduced": [0, 1, 2, 3, 4, 5],
            "reduced": [0, 1, 2, 5],
            "leftover": [3, 4]
            }
        diction2 = {
            "non_reduced": [0, 1, 2, 3, 4],
            "reduced": [0, 1, 3],
            "leftover": [1, 3]
            }
        
        # Predict pass or fail amounts in space remaining of both disciplines
        passfail1, passfail_std1 = predictData(self.Discip1, gpr1, diction1)
        passfail2, passfail_std2 = predictData(self.Discip2, gpr2, diction2)
        
        # Determine expected size of passfail arrays for each discipline
        exp_passfail1_non = (6,)
        exp_passfail1_red = (4,)
        exp_passfail1_left = (2,)
        exp_passfailstd1_non = (6,)
        exp_passfailstd1_red = (4,)
        exp_passfailstd1_left = (2,)
        exp_passfail2_non = (5,)
        exp_passfail2_red = (3,)
        exp_passfail2_left = (2,)
        exp_passfailstd2_non = (5,)
        exp_passfailstd2_red = (3,)
        exp_passfailstd2_left = (2,)
        
        # Test that expected and actual array sizes match up
        self.assertEqual(passfail1['non_reduced'].shape, exp_passfail1_non)
        self.assertEqual(passfail1['reduced'].shape, exp_passfail1_red)
        self.assertEqual(passfail1['leftover'].shape, exp_passfail1_left)
        self.assertEqual(passfail_std1['non_reduced'].shape, \
                         exp_passfailstd1_non)
        self.assertEqual(passfail_std1['reduced'].shape, exp_passfailstd1_red)
        self.assertEqual(passfail_std1['leftover'].shape, \
                         exp_passfailstd1_left)
        self.assertEqual(passfail2['non_reduced'].shape, exp_passfail2_non)
        self.assertEqual(passfail2['reduced'].shape, exp_passfail2_red)
        self.assertEqual(passfail2['leftover'].shape, exp_passfail2_left)
        self.assertEqual(passfail_std2['non_reduced'].shape, \
                         exp_passfailstd2_non)
        self.assertEqual(passfail_std2['reduced'].shape, exp_passfailstd2_red)
        self.assertEqual(passfail_std2['leftover'].shape, \
                         exp_passfailstd2_left)
    
    
    def test_analyze_infeasibility(self):
        """
        Unit tests for analyzeInfeasibility function
        """
        
        # Create passfail and passfail_std data
        passfail1 = np.array([])
        passfail_std1 = np.array([])
        passfail2 = np.array([0.3, -0.7, 0.1, 0.0, -0.2])
        passfail_std2 = np.array([0.1, 0.3, 0.05, 0.2, 0.2])
        
        # Run function with both sets of passfail data
        infeas1 = analyzeInfeasibility(passfail1, passfail_std1)
        infeas2 = analyzeInfeasibility(passfail2, passfail_std2)
        
        # Determine expected values of both sets of passfail data
        exp_infeas1 = 0
        exp_infeas2 = 1 - ((1+0.2/1.8+0.25/0.3+0.6/1.2+0.4/1.2)/5)
        
        # Test that calculated values match expected data
        np.testing.assert_almost_equal(infeas1, exp_infeas1)
        np.testing.assert_almost_equal(infeas2, exp_infeas2)
    
    
        

        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_merge_constraints)
unittest.TextTestRunner(verbosity=2).run(suite)