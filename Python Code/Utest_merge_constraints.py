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
from merge_constraints import mergeConstraints, sharedIndices, trainData, \
    analyzeInfeasibility, analyzeFeasibility, bezierPoint, getPredictions
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
    
    
    def test_shared_indices(self):
        """
        Unit tests for sharedIndices function
        """
        
        # Test for proper results when no common elements between A and B
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5, 6], [7, 8]])
        expected = ([0, 1], [], [0, 1])
        self.assertEqual(sharedIndices(A, B), expected)
        
        # Test for proper results when A and B are identical
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[1, 2], [3, 4]])
        expected = ([0, 1], [0, 1], [])
        self.assertEqual(sharedIndices(A, B), expected)
        
        # Test for proper results when some common elements between A and B
        A = np.array([[1, 2], [3, 4], [5, 6]])
        B = np.array([[3, 4], [7, 8]])
        expected = ([0, 1, 2], [1], [0, 2])
        self.assertEqual(sharedIndices(A, B), expected)
        
        # Test for proper results when A is empty
        A = np.array([])
        B = np.array([[1, 2], [3, 4]])
        expected = ([], [], [])
        self.assertEqual(sharedIndices(A, B), expected)
        
        # Test for proper results when B is empty
        A = np.array([[1, 2], [3, 4]])
        B = np.array([])
        expected = ([0, 1], [], [0, 1])
        self.assertEqual(sharedIndices(A, B), expected)
        
        # Test for proper results when both are empty
        A = np.array([])
        B = np.array([])
        expected = ([], [], [])
        self.assertEqual(sharedIndices(A, B), expected)
        
    
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
    
    
    def test_get_predictions(self):
        """
        Unit tests for getPredictions function
        """
        
        # Initialize symbols
        x = sp.symbols('x1:5')
        
        # Create new rules
        rule1 = (x[0] > 0.5,)
        rule2 = (sp.Or(x[1]<0.2, x[3]>0.5),)
        
        # Initialize passfail data for non-reduced space of both disciplines
        pf1 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
        pf_std1 = np.array([0.15, 0.25, 0.35, 0.45, 0.55, 0.65])
        pf2 = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        pf_std2 = np.array([0.15, 0.25, 0.35, 0.45, 0.55])
        
        # Execute function with established data
        passfail1, passfail_std1 = getPredictions(self.Discip1, rule1, pf1,
                                                  pf_std1)
        passfail2, passfail_std2 = getPredictions(self.Discip2, rule2, pf2,
                                                  pf_std2)
        
        # Determine expected passfail and standard deviation dictionaries
        exp_passfail1 = {
            'non_reduced': np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]),
            'reduced': np.array([0.3, 0.5]),
            'leftover': np.array([0.1, 0.2, 0.4, 0.6])
            }
        exp_passfail_std1 = {
            'non_reduced': np.array([0.15, 0.25, 0.35, 0.45, 0.55, 0.65]),
            'reduced': np.array([0.35, 0.55]),
            'leftover': np.array([0.15, 0.25, 0.45, 0.65])
            }
        exp_passfail2 = {
            'non_reduced': np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
            'reduced': np.array([0.4]),
            'leftover': np.array([0.1, 0.2, 0.3, 0.5])
            }
        exp_passfail_std2 = {
            'non_reduced': np.array([0.15, 0.25, 0.35, 0.45, 0.55]),
            'reduced': np.array([0.45]),
            'leftover': np.array([0.15, 0.25, 0.35, 0.55])
            }
        
        # Check that expected passfail dictionaries align with actual ones
        self.assertEqual(passfail1.keys(), exp_passfail1.keys())
        self.assertEqual(passfail_std1.keys(), exp_passfail_std1.keys())
        self.assertEqual(passfail2.keys(), exp_passfail2.keys())
        self.assertEqual(passfail_std2.keys(), exp_passfail_std2.keys())
        for key in passfail1:
            np.testing.assert_array_almost_equal(passfail1[key],
                                                 exp_passfail1[key])
            np.testing.assert_array_almost_equal(passfail_std1[key],
                                                 exp_passfail_std1[key])
            np.testing.assert_array_almost_equal(passfail2[key],
                                                 exp_passfail2[key])
            np.testing.assert_array_almost_equal(passfail_std2[key],
                                                 exp_passfail_std2[key])
        
        # Execute function again with established data
        passfail1, passfail_std1 = getPredictions(self.Discip1, rule2, pf1,
                                                  pf_std1)
        passfail2, passfail_std2 = getPredictions(self.Discip2, rule1, pf2,
                                                  pf_std2)
        
        # Determine expected passfail and standard deviation dictionaries
        exp_passfail1 = {
            'non_reduced': np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]),
            'reduced': np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]),
            'leftover': np.array([])
            }
        exp_passfail_std1 = {
            'non_reduced': np.array([0.15, 0.25, 0.35, 0.45, 0.55, 0.65]),
            'reduced': np.array([0.15, 0.25, 0.35, 0.45, 0.55, 0.65]),
            'leftover': np.array([])
            }
        exp_passfail2 = {
            'non_reduced': np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
            'reduced': np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
            'leftover': np.array([])
            }
        exp_passfail_std2 = {
            'non_reduced': np.array([0.15, 0.25, 0.35, 0.45, 0.55]),
            'reduced': np.array([0.15, 0.25, 0.35, 0.45, 0.55]),
            'leftover': np.array([])
            }
        
        # Check that expected passfail dictionaries align with actual ones
        self.assertEqual(passfail1.keys(), exp_passfail1.keys())
        self.assertEqual(passfail_std1.keys(), exp_passfail_std1.keys())
        self.assertEqual(passfail2.keys(), exp_passfail2.keys())
        self.assertEqual(passfail_std2.keys(), exp_passfail_std2.keys())
        for key in passfail1:
            np.testing.assert_array_almost_equal(passfail1[key],
                                                 exp_passfail1[key])
            np.testing.assert_array_almost_equal(passfail_std1[key],
                                                 exp_passfail_std1[key])
            np.testing.assert_array_almost_equal(passfail2[key],
                                                 exp_passfail2[key])
            np.testing.assert_array_almost_equal(passfail_std2[key],
                                                 exp_passfail_std2[key])
        
        
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
        opinions, passfail, passfail_std = cmerger.formOpinion()
        
        # Ensure opinion has nan only if not impacted by rule
        self.assertFalse(np.isnan(opinions[rules_new[0]][0]))
        self.assertTrue(np.isnan(opinions[rules_new[0]][1]))
        self.assertFalse(np.isnan(opinions[rules_new[1]][0]))
        self.assertFalse(np.isnan(opinions[rules_new[1]][1]))
        self.assertTrue(np.isnan(opinions[rules_new[2]][0]))
        self.assertFalse(np.isnan(opinions[rules_new[2]][1]))
        self.assertFalse(np.isnan(opinions[rules_new[3]][0]))
        self.assertTrue(np.isnan(opinions[rules_new[3]][1]))
        self.assertFalse(np.isnan(opinions[rules_new[4]][0]))
        self.assertFalse(np.isnan(opinions[rules_new[4]][1]))
        
        # Ensure 5 sets of opinions are formed
        self.assertEqual(len(opinions), 5)
        
        # Ensure each set has opinions from two disciplines
        for op in opinions:
            self.assertEqual(opinions[op].shape, (2,))
        
        # Ensure passfail data gathered for every rule combination
        self.assertEqual(len(passfail), 31)
        self.assertEqual(len(passfail_std), 31)
        
        # Loop through passfail data
        for (key_pf, val_pf), (key_pfstd, val_pfstd) in zip(passfail.items(), passfail_std.items()):
            
            # Ensure values have data for two disciplines
            self.assertEqual(len(val_pf), 2)
            self.assertEqual(len(val_pfstd), 2)
            
            # Loop through each discipline
            for (ind_pf, discip_pf), (ind_pfstd, discip_pfstd) in zip(enumerate(val_pf), enumerate(val_pfstd)):
                
                # Check that non-reduced array is proper length
                if ind_pf == 0:
                    self.assertEqual(len(discip_pf['non_reduced']), 6)
                    self.assertEqual(len(discip_pfstd['non_reduced']), 6)
                elif ind_pf == 1:
                    self.assertEqual(len(discip_pf['non_reduced']), 5)
                    self.assertEqual(len(discip_pfstd['non_reduced']), 5)
        
    
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
        opinions = {
            rules_new[0]: np.array([0.8, np.nan]),
            rules_new[1]: np.array([0.5, 0.9]),
            rules_new[2]: np.array([np.nan, 0.2]),
            rules_new[3]: np.array([1.0, np.nan]),
            rules_new[4]: np.array([1.0, 0.05])
            }
        
        # Establish initial failure criteria parameter for each discipline
        self.Discip1['part_params'] = {'fail_crit': [0.0, 0.05]}
        self.Discip2['part_params'] = {'fail_crit': [0.1, 0.05]}
        
        # Create passfail data for the rules
        passfail = {
            (rules_new[0],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[1],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[2],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[3],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[4],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ]
            }
        passfail_std = {
            (rules_new[0],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[1],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[2],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[3],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[4],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ]
            }
        
        # Run domDecision method
        rules_new, passfail, passfail_std = \
            cmerger.domDecision(opinions,irules_discip,passfail,passfail_std)
        
        # Establish expected rule list
        exp_rules_new = [x[0]>0.5,
                         sp.And(x[3]>0.2,x[3]<0.6),
                         sp.Or(x[0]>0.8, x[2]<0.9),
                         x[2]>0.5]
        
        # Ensure proper rule(s) are being thrown out
        self.assertListEqual(rules_new, exp_rules_new)
        
        # Ensure proper passfail data is being thrown out
        self.assertEqual(len(passfail), 4)
        self.assertEqual(len(passfail_std), 4)
        self.assertIn((x[0]>0.5,), passfail)
        self.assertIn((x[0]>0.5,), passfail_std)
        self.assertNotIn((sp.Or(x[1]<0.2, x[2]>=0.8),), passfail)
        self.assertNotIn((sp.Or(x[1]<0.2, x[2]>=0.8),), passfail_std)
        self.assertIn((sp.And(x[3]>0.2,x[3]<0.6),), passfail)
        self.assertIn((sp.And(x[3]>0.2,x[3]<0.6),), passfail_std)
        self.assertIn((sp.Or(x[0]>0.8, x[2]<0.9),), passfail)
        self.assertIn((sp.Or(x[0]>0.8, x[2]<0.9),), passfail_std)
        self.assertIn((x[2]>0.5,), passfail)
        self.assertIn((x[2]>0.5,), passfail_std)
        
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
        self.Discip1['part_params'] = {'fail_crit': [0.9, 0.05]}
        self.Discip2['part_params'] = {'fail_crit': [0.35, 0.05]}
        
        # Recreate passfail data for the rules
        passfail = {
            (rules_new[0],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[1],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[2],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[3],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[4],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ]
            }
        passfail_std = {
            (rules_new[0],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[1],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[2],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[3],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ],
            (rules_new[4],): [
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    },
                {
                    'non_reduced': np.array([]),
                    'reduced': np.array([]),
                    'leftover': np.array([])
                    }
                ]
            }
        
        # Run domDecision method
        rules_new, passfail, passfail_std = \
            cmerger.domDecision(opinions,irules_discip,passfail,passfail_std)
        
        # Establish expected rule list
        exp_rules_new = [x[0]>0.5, 
                         sp.Or(x[1]<0.2, x[2]>=0.8),
                         sp.And(x[3]>0.2,x[3]<0.6),
                         sp.Or(x[0]>0.8, x[2]<0.9),
                         x[2]>0.5]
        
        # Ensure proper rule(s) are being thrown out
        self.assertListEqual(rules_new, exp_rules_new)
        
        # Ensure proper passfail data is being thrown out
        self.assertEqual(len(passfail), 5)
        self.assertEqual(len(passfail_std), 5)
        self.assertIn((x[0]>0.5,), passfail)
        self.assertIn((x[0]>0.5,), passfail_std)
        self.assertIn((sp.Or(x[1]<0.2, x[2]>=0.8),), passfail)
        self.assertIn((sp.Or(x[1]<0.2, x[2]>=0.8),), passfail_std)
        self.assertIn((sp.And(x[3]>0.2,x[3]<0.6),), passfail)
        self.assertIn((sp.And(x[3]>0.2,x[3]<0.6),), passfail_std)
        self.assertIn((sp.Or(x[0]>0.8, x[2]<0.9),), passfail)
        self.assertIn((sp.Or(x[0]>0.8, x[2]<0.9),), passfail_std)
        self.assertIn((x[2]>0.5,), passfail)
        self.assertIn((x[2]>0.5,), passfail_std)
        
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_merge_constraints)
unittest.TextTestRunner(verbosity=2).run(suite)