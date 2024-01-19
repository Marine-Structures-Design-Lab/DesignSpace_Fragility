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
    predictData, analyzeInfeasibility, analyzeFeasibility, bezierPoint
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
        x = sp.symbols('x1:5')
        y = sp.symbols('y1:4')
        
        # Create a discipline without eliminated data
        self.Discip1 = {
            "tested_ins": np.array([[0.1, 0.1, 0.1],
                                    [0.2, 0.3, 0.4],
                                    [0.5, 0.5, 0.9]]),
            "tested_outs": np.zeros((3,1)),
            "Fail_Amount": np.array([0.0, 0.5, 0.3]),
            "Pass_Amount": np.array([0.7, 0.0, 0.4]),
            "pass?": [True, True, True],
            "ins": [x[0], x[1], x[2]],
            "outs": [y[0]],
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
            "tested_outs": np.zeros((4,2)),
            "Fail_Amount": np.array([0.1, 0.0, 0.8, 0.0]),
            "Pass_Amount": np.array([0.0, 0.2, 0.9, 0.0]),
            "pass?": [True, True, True, True],
            "ins": [x[1], x[2], x[3]],
            "outs": [y[1], y[2]],
            "space_remaining": np.array([[0.4, 0.4, 0.4],
                                         [0.5, 0.4, 0.5],
                                         [0.3, 0.3, 0.4],
                                         [0.1, 0.7, 0.2],
                                         [0.5, 0.6, 0.1]]),
            "eliminated": {
                "tested_ins": np.array([[0.1, 0.1, 0.1],
                                        [0.2, 0.3, 0.4],
                                        [0.5, 0.5, 0.9]]),
                "tested_outs": np.zeros((3,2)),
                "Fail_Amount": np.array([0.0, 0.5, 0.3]),
                "Pass_Amount": np.array([0.7, 0.0, 0.4]),
                "pass?": [True, True, True],
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
    
    
    def test_analyze_feasibility(self):
        """
        Unit tests for analyzeFeasibility function
        """
        
        # Create two sets of mean and standard deviation data
        means1_1 = np.array([0.3, -0.7, 0.1, 0.0, -0.2])
        std1_1 = np.array([0.1, 0.3, 0.05, 0.2, 0.2])
        means1_2 = np.array([])
        std1_2 = np.array([])
        means2_1 = np.array([0.3, -0.7, 0.1, 0.0, -0.2])
        std2_1 = np.array([0.1, 0.3, 0.05, 0.2, 0.2])
        means2_2 = np.array([0.4, 0.0, 0.5, -0.3])
        std2_2 = np.array([0.1, 0.05, 0.2, 0.1])
        
        # Run function with both sets of mean and standard deviation data
        feas1 = analyzeFeasibility(means1_1, std1_1, means1_2, std1_2)
        feas2 = analyzeFeasibility(means2_1, std2_1, means2_2, std2_2)
        
        # Determine the expected values of both sets of data
        exp_feas1 = 0.0
        exp_feas2 = (0.99865010+0.00981533+0.97724987+0.50000000+0.15865525) /\
            (0.99996833+0.50000000+0.99379033+0.00134990)
        
        # Test that calculated values match expected data
        np.testing.assert_almost_equal(feas1, exp_feas1)
        np.testing.assert_almost_equal(feas2, exp_feas2)
        
    
    def test_bezier_point(self):
        """
        Unit tests for bezierPoint function
        """
        
        # Create various values of the m1 metric
        m1 = np.array([0.0, 0.2, 0.5, 0.8, 1.0])
        
        # Initialize a numpy array of zeros the same size as m1
        y = np.zeros_like(m1)
        
        # Run function for each value of the m1 metric
        for i, value in enumerate(m1):
            y[i] = bezierPoint(m1[i])
            
        # Determine expected values of y
        exp_y = np.array([1.0, 0.896, 0.65, 0.296, 0.0])
        
        # Check that expected and actual array for y match up
        np.testing.assert_array_almost_equal(y, exp_y)
        
        # Check that nonetype is returned when t value is not between 0 and 1
        m1 = 20
        y = bezierPoint(m1)
        self.assertIsNone(y)
    
    
    def test_form_opinion(self):
        """
        Unit tests for formOpinion method
        """
        
        # Initialize symbols
        x = sp.symbols('x1:5')
        
        # Create a list of rules
        rules_new = [x[0]>0.5, 
                     sp.Or(x[1]<0.2, x[2]>=0.8), 
                     sp.And(x[3]>0.2,x[3]<0.6), 
                     sp.Or(x[0]>0.8, x[2]<0.9), 
                     x[2]>0.5]
        
        # Create a mergeConstraints object
        cmerger = mergeConstraints(rules_new, [self.Discip1, self.Discip2],
                                   {}, {})
        
        # Form opinions for the set of new rules
        opinions = cmerger.formOpinion()
        
        # Ensure opinion has nan only if not impacted by rule
        self.assertFalse(np.isnan(opinions[0][0]))
        self.assertTrue(np.isnan(opinions[0][1]))
        self.assertFalse(np.isnan(opinions[1][0]))
        self.assertFalse(np.isnan(opinions[1][1]))
        self.assertTrue(np.isnan(opinions[2][0]))
        self.assertFalse(np.isnan(opinions[2][1]))
        self.assertFalse(np.isnan(opinions[3][0]))
        self.assertTrue(np.isnan(opinions[3][1]))
        self.assertFalse(np.isnan(opinions[4][0]))
        self.assertFalse(np.isnan(opinions[4][1]))
        
        # Ensure 5 sets of opinions are formed
        self.assertEqual(len(opinions), 5)
        
        # Ensure each set has opinions from two disciplines
        for op in opinions:
            self.assertEqual(op.shape, (2,))
    
    
    def test_dom_decisions(self):
        """
        Unit tests for domDecision method
        """
        
        # Initialize symbols
        x = sp.symbols('x1:5')
        
        # Create a list of rules
        rules_new = [x[0]>0.5, 
                     sp.Or(x[1]<0.2, x[2]>=0.8),
                     sp.And(x[3]>0.2,x[3]<0.6),
                     sp.Or(x[0]>0.8, x[2]<0.9),
                     x[2]>0.5]
        
        # Create a mergeConstraints object
        cmerger = mergeConstraints(rules_new, [self.Discip1, self.Discip2],
                                   {}, {})
        
        # Create list of integers for discipline proposing each rule
        irules_discip = [0, 1, 1, 0, 1]
        
        # Create opinions for the new set of rules
        opinions = [np.array([0.8, np.nan]),
                    np.array([0.5, 0.9]),
                    np.array([np.nan, 0.2]),
                    np.array([1.0, np.nan]),
                    np.array([1.0, 0.05])]
        
        # Establish initial failure criteria parameter for each discipline
        self.Discip1['part_params'] = {'fail_crit': 0.0}
        self.Discip2['part_params'] = {'fail_crit': 0.1}
        
        # Run domDecision method
        rules_new = cmerger.domDecision(opinions, irules_discip)
        
        # Establish expected rule list
        exp_rules_new = [x[0]>0.5,
                         sp.And(x[3]>0.2,x[3]<0.6),
                         sp.Or(x[0]>0.8, x[2]<0.9),
                         x[2]>0.5]
        
        # Ensure proper rule(s) are being thrown out
        self.assertListEqual(rules_new, exp_rules_new)
        
        # Re-establish list of rules
        rules_new = [x[0]>0.5, 
                     sp.Or(x[1]<0.2, x[2]>=0.8),
                     sp.And(x[3]>0.2,x[3]<0.6),
                     sp.Or(x[0]>0.8, x[2]<0.9),
                     x[2]>0.5]
        
        # Create a mergeConstraints object
        cmerger = mergeConstraints(rules_new, [self.Discip1, self.Discip2],
                                   {}, {})
        
        # Establish new failure criteria parameter for each discipline
        self.Discip1['part_params'] = {'fail_crit': 0.9}
        self.Discip2['part_params'] = {'fail_crit': 0.35}
        
        # Run domDecision method
        rules_new = cmerger.domDecision(opinions, irules_discip)
        
        # Establish expected rule list
        exp_rules_new = [x[0]>0.5, 
                         sp.Or(x[1]<0.2, x[2]>=0.8),
                         sp.And(x[3]>0.2,x[3]<0.6),
                         sp.Or(x[0]>0.8, x[2]<0.9),
                         x[2]>0.5]
        
        # Ensure proper rule(s) are being thrown out
        self.assertListEqual(rules_new, exp_rules_new)
        
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_merge_constraints)
unittest.TextTestRunner(verbosity=2).run(suite)