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
from organize_data import universalContribution, sharedIndices, countBooleans,\
    fillSpaceRemaining, findAverages, findPercentages
import unittest
import sympy as sp
import numpy as np
from scipy.stats import qmc


"""
CLASSES
"""
class test_organize_data(unittest.TestCase):
    
    def test_universal_contribution(self):
        """
        Unit tests for the universalContribution function
        """
        
        # Create sympy input variables
        x = sp.symbols('x1:7')
        
        # Create discipline data
        Discips = [
            {'tested_ins': np.array([[0.1, 0.2, 0.3],
                                     [0.4, 0.5, 0.6],
                                     [0.7, 0.8, 0.9],
                                     [1.0, 0.0, 0.1],
                                     [0.2, 0.3, 0.4]]),
             'pass?': [True, False, True, False, True],
             'ins': [x[0], x[1], x[2]]},
            {'tested_ins': np.array([[0.1, 0.2, 0.3],
                                     [0.1, 0.5, 0.3],
                                     [0.7, 0.8, 0.5],
                                     [1.0, 0.2, 0.1],
                                     [0.2, 0.3, 0.3]]),
             'pass?': [False, True, False, True, False],
             'ins': [x[2], x[3], x[4]]},
            {'tested_ins': np.array([[0.1, 0.2, 0.3],
                                     [0.1, 0.5, 0.3],
                                     [0.1, 0.8, 0.2],
                                     [1.0, 0.0, 0.1],
                                     [0.2, 0.2, 0.3]]),
             'pass?': [True, True, False, False, True],
             'ins': [x[0], x[4], x[5]]}
        ]
        
        # Choose design point index in first discipline
        index = 0
        ind_discip = 0
        
        # Determine the expected fraction for first discipline
        exp_frac = 2.0/3.0
        
        # Run the function
        frac = universalContribution(Discips, index, ind_discip)
        
        # Check that expected fraction almost equals actual fraction
        self.assertAlmostEqual(frac, exp_frac)
        
        # Choose design point index in second discipline
        index = 0
        ind_discip = 1
        
        # Determine the expected fraction for second discipline
        exp_frac = 0
        
        # Run the function
        frac = universalContribution(Discips, index, ind_discip)
        
        # Check that expected fraction almost equals actual fraction
        self.assertAlmostEqual(frac, exp_frac)
        
        # Choose design point index in third discipline
        index = 1
        ind_discip = 2
        
        # Determine the expected fraction for third discipline
        exp_frac = 1.0/2.0
        
        # Run the function
        frac = universalContribution(Discips, index, ind_discip)
        
        # Check that expected fraction almost equals actual fraction
        self.assertAlmostEqual(frac, exp_frac)
        
    
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
                                 [0.8, 0.1, 0.2],
                                 [0.4, 0.3, 0.4]])
        
        # Create a smaller numpy array
        smaller_array = np.array([[0.0, 0.0, 1.0],
                                  [5.3, 6.6, -0.7],
                                  [0.1, 0.2, 0.9]])
        
        # Create an empty numpy array
        smallest_array = np.empty((0,3))
        
        # Determine the expected index lists
        exp_ans1 = [1, 3, 6]
        exp_ans2 = []
        
        # Run the function
        indices1 = sharedIndices(larger_array, smaller_array)
        indices2 = sharedIndices(smaller_array, smallest_array)
        
        # Check that expected index lists match actual index lists
        self.assertListEqual(indices1, exp_ans1)
        self.assertListEqual(indices2, exp_ans2)
    
    
    def test_count_booleans(self):
        """
        Unit tests for the countBooleans function
        """
        
        # Create sympy input variables
        x = sp.symbols('x1:7')
        
        # Create discipline data
        Discips = [
            {'tested_ins': np.array([[0.1, 0.2, 0.3],
                                     [0.4, 0.5, 0.6],
                                     [0.7, 0.8, 0.9],
                                     [1.0, 0.0, 0.1],
                                     [0.2, 0.3, 0.4]]),
             'pass?': [True, False, True, False, True],
             'ins': [x[0], x[1], x[2]]},
            {'tested_ins': np.array([[0.1, 0.2, 0.3],
                                     [0.1, 0.5, 0.3],
                                     [0.3, 0.8, 0.5],
                                     [1.0, 0.2, 0.1],
                                     [0.2, 0.3, 0.3]]),
             'pass?': [False, True, False, True, False],
             'ins': [x[2], x[3], x[4]]},
            {'tested_ins': np.array([[0.1, 0.2, 0.3],
                                     [0.1, 0.5, 0.3],
                                     [0.1, 0.8, 0.2],
                                     [1.0, 0.0, 0.1],
                                     [0.2, 0.2, 0.3]]),
             'pass?': [True, True, False, False, True],
             'ins': [x[0], x[4], x[5]]}
        ]
        
        # Create a list of integers corresponding to specific boolean values
        index_list = [0, 4, 2]

        # Run the function for the first discipline
        true_count, true_count_all = countBooleans(index_list, Discips, 0)
        exp_tc = 3
        exp_tca = 2.0/4.0 + 1.0/1.0 + 0.0
        
        # Check that expected true counts match actual true counts
        self.assertAlmostEqual(true_count, exp_tc)
        self.assertAlmostEqual(true_count_all, exp_tca)

        # Run the function for the second discipline
        true_count, true_count_all = countBooleans(index_list, Discips, 1)
        exp_tc = 0
        exp_tca = 0.0
        
        # Check that expected true counts match actual true counts
        self.assertAlmostEqual(true_count, exp_tc)
        self.assertAlmostEqual(true_count_all, exp_tca)
        
        # Run the function for the third discipline
        true_count, true_count_all = countBooleans(index_list, Discips, 2)
        exp_tc = 2
        exp_tca = 1.0/1.0 + 1.0/1.0
        
        # Check that expected true counts match actual true counts
        self.assertAlmostEqual(true_count, exp_tc)
        self.assertAlmostEqual(true_count_all, exp_tca)
        
    
    def test_fill_space_remaining(self):
        """
        Unit tests for the fillSpaceRemaining function
        """
        
        # Create test case data
        test_case = {
            'Run_1': [[
                {'space_remaining': np.array([[0.1, 0.2, 0.3],
                                              [0.4, 0.5, 0.6],
                                              [0.7, 0.8, 0.9]]),
                 'iter': 0},
                
                {'space_remaining': np.array([[0.1, 0.2, 0.3],
                                              [0.4, 0.5, 0.6]]),
                 'iter': 100},
                
                {'space_remaining': np.array([[0.1, 0.2, 0.3]]),
                 'iter': 200}
            ]],
            'Run_2': [[
                {'space_remaining': np.array([[0.1, 0.2, 0.3],
                                              [0.4, 0.5, 0.6],
                                              [0.7, 0.8, 0.9]]),
                 'iter': 0},
                
                {'space_remaining': np.array([[0.1, 0.2, 0.3],
                                              [0.4, 0.5, 0.6]]),
                 'iter': 100},
                
                {'space_remaining': np.array([[0.1, 0.2, 0.3],
                                              [0.4, 0.5, 0.6]]),
                 'iter': 100},
                
                {'space_remaining': np.array([[0.1, 0.2, 0.3]]),
                 'iter': 200}
            ]]
        }
        
        # Create discipline data
        Discips = [
            {'tested_ins': np.array([[0.1, 0.2, 0.3],
                                     [0.4, 0.5, 0.6],
                                     [0.7, 0.8, 0.9]]),
             'pass?': [True, False, True]}
        ]
        
        # Create test times
        set_of_times = {0, 100, 150, 200}
    
        # Determine expected total space and feasible space output
        expected_space_rem = {
            'Run_1': {
                'Discipline_1': {
                    0: [3],
                    100: [2],
                    150: [2],
                    200: [1]
                }
            },
            'Run_2': {
                'Discipline_1': {
                    0: [3],
                    100: [2, 2],
                    150: [2],
                    200: [1]
                }
            }
        }
        expected_feas_rem = {
            'Run_1': {
                'Discipline_1': {
                    0: [2],
                    100: [1],
                    150: [1],
                    200: [1]
                }
            },
            'Run_2': {
                'Discipline_1': {
                    0: [2],
                    100: [1, 1],
                    150: [1],
                    200: [1]
                }
            }
        }
        expected_ufeas_rem = {
            'Run_1': {
                'Discipline_1': {
                    0: [0],
                    100: [0],
                    150: [0],
                    200: [0]
                }
            },
            'Run_2': {
                'Discipline_1': {
                    0: [0],
                    100: [0, 0],
                    150: [0],
                    200: [0]
                }
            }
        }
        expected_diver_rem = {
            'Run_1': {
                'Discipline_1': {
                    0: [qmc.discrepancy(np.array([[0.1, 0.2, 0.3],
                                                  [0.4, 0.5, 0.6],
                                                  [0.7, 0.8, 0.9]]))],
                    100: [qmc.discrepancy(np.array([[0.1, 0.2, 0.3],
                                                    [0.4, 0.5, 0.6]]))],
                    150: [qmc.discrepancy(np.array([[0.1, 0.2, 0.3],
                                                    [0.4, 0.5, 0.6]]))],
                    200: [qmc.discrepancy(np.array([[0.1, 0.2, 0.3]]))]
                }
            },
            'Run_2': {
                'Discipline_1': {
                    0: [qmc.discrepancy(np.array([[0.1, 0.2, 0.3],
                                                  [0.4, 0.5, 0.6],
                                                  [0.7, 0.8, 0.9]]))],
                    100: [qmc.discrepancy(np.array([[0.1, 0.2, 0.3],
                                                    [0.4, 0.5, 0.6]])),
                          qmc.discrepancy(np.array([[0.1, 0.2, 0.3],
                                                    [0.4, 0.5, 0.6]]))],
                    150: [qmc.discrepancy(np.array([[0.1, 0.2, 0.3],
                                                    [0.4, 0.5, 0.6]]))],
                    200: [qmc.discrepancy(np.array([[0.1, 0.2, 0.3]]))]
                }
            }
        }
        
        # Run the function
        space_rem, feas_rem, ufeas_rem, diver_rem = \
            fillSpaceRemaining(test_case, set_of_times, Discips)
        
        # Check that the function produces the expected output
        self.assertDictEqual(space_rem, expected_space_rem)
        self.assertDictEqual(feas_rem, expected_feas_rem)
        self.assertDictEqual(ufeas_rem, expected_ufeas_rem)
        self.assertDictEqual(diver_rem, expected_diver_rem)
    
    
    def test_find_averages(self):
        """
        Unit tests for the findAverages function
        """
        
        # Create total space remaining data
        space_rem = {
            'Run_1': {
                'Discipline_1': {
                    0: [10],
                    100: [8],
                    150: [8],
                    200: [2]
                }
            },
            'Run_2': {
                'Discipline_1': {
                    0: [10],
                    100: [8, 6],
                    150: [6],
                    200: [4]
                }
            }
        }
        
        # Create feasible space remaining data
        feas_rem = {
            'Run_1': {
                'Discipline_1': {
                    0: [3],
                    100: [1],
                    150: [1],
                    200: [0]
                }
            },
            'Run_2': {
                'Discipline_1': {
                    0: [5],
                    100: [3, 3],
                    150: [3],
                    200: [1]
                }
            }
        }
        
        # Create universal feasible space remaining data
        ufeas_rem = {
            'Run_1': {
                'Discipline_1': {
                    0: [1.2],
                    100: [1],
                    150: [0.5],
                    200: [0]
                }
            },
            'Run_2': {
                'Discipline_1': {
                    0: [5],
                    100: [2.3, 2.3],
                    150: [2.0],
                    200: [0.0]
                }
            }
        }
        
        # Create diversity data
        diver_rem = {
            'Run_1': {
                'Discipline_1': {
                    0: [0.0],
                    100: [0.2],
                    150: [0.2],
                    200: [0.7]
                }
            },
            'Run_2': {
                'Discipline_1': {
                    0: [0.0],
                    100: [0.2, 0.4],
                    150: [0.4],
                    200: [0.9]
                }
            }
        }
        
        # Determine expected total space and feasible space averages
        expected_average_rem = {
            'Discipline_1': {
                0: 10.0,
                100: 7.5,
                150: 7.0,
                200: 3.0
            }
        }
        expected_average_feas = {
            'Discipline_1': {
                0: 4.0,
                100: 2.0,
                150: 2.0,
                200: 0.5
            }
        }
        expected_average_ufeas = {
            'Discipline_1': {
                0: 3.1,
                100: 1.65,
                150: 1.25,
                200: 0.0
            }
        }
        expected_average_diver = {
            'Discipline_1': {
                0: 0.0,
                100: 0.25,
                150: 0.30000000000000004,
                200: 0.8
            }
        }
        
        # Run the function
        average_rem, average_feas, average_ufeas, average_diver = \
            findAverages(space_rem, feas_rem, ufeas_rem, diver_rem)
        
        # Check that the function produces the expected output
        self.assertDictEqual(average_rem, expected_average_rem)
        self.assertDictEqual(average_feas, expected_average_feas)
        self.assertDictEqual(average_ufeas, expected_average_ufeas)
        self.assertDictEqual(average_diver, expected_average_diver)
    
    
    def test_find_percentages(self):
        """
        Unit tests for the findPercentages function
        """
        
        # Create average total space remaining data
        average_rem = {
            'Discipline_1': {
                0: 10.0,
                100: 7.5,
                150: 7.0,
                200: 3.0
            }
        }
        
        # Create average feasible space remaining data
        average_feas = {
            'Discipline_1': {
                0: 4.0,
                100: 2.0,
                150: 2.0,
                200: 0.5
            }
        }
        
        # Create average universal feasible space remaining data
        average_ufeas = {
            'Discipline_1': {
                0: 3.1,
                100: 1.65,
                150: 1.25,
                200: 0.0
            }
        }
        
        # Create average diversity data
        average_diver = {
            'Discipline_1': {
                0: 0.0,
                100: 0.25,
                150: 0.3,
                200: 0.8
            }
        }
        
        # Determine total and feasible space percentages
        expected_percent_rem = {
            'Discipline_1': {
                0: 100.0,
                100: 75.0,
                150: 70.0,
                200: 30.0
            }
        }
        expected_percent_feas1 = {
            'Discipline_1': {
                0: 40.0,
                100: 2/7.5*100,
                150: 2/7*100,
                200: 0.5/3*100
            }
        }
        expected_percent_feas2 = {
            'Discipline_1': {
                0: 40.0,
                100: 20.0,
                150: 20.0,
                200: 5.0
            }
        }
        expected_percent_ufeas1 = {
            'Discipline_1': {
                0: 31.0,
                100: 1.65/7.5*100,
                150: 1.25/7*100,
                200: 0.0/3*100
            }
        }
        expected_percent_ufeas2 = {
            'Discipline_1': {
                0: 31.0,
                100: 16.499999999999996,
                150: 12.5,
                200: 0.0
            }
        }
        expected_percent_diver = {
            'Discipline_1': {
                0: 0.0,
                100: 25.0,
                150: 30.0,
                200: 80.0
            }
        }
        
        # Run the function
        percent_rem, percent_feas1, percent_feas2, percent_ufeas1, \
            percent_ufeas2, percent_diver = findPercentages(average_rem, 
                average_feas, average_ufeas, average_diver)
        
        # Check that the function produces the expected output
        self.assertDictEqual(percent_rem, expected_percent_rem)
        self.assertDictEqual(percent_feas1, expected_percent_feas1)
        self.assertDictEqual(percent_feas2, expected_percent_feas2)
        self.assertDictEqual(percent_ufeas1, expected_percent_ufeas1)
        self.assertDictEqual(percent_ufeas2, expected_percent_ufeas2)
        self.assertDictEqual(percent_diver, expected_percent_diver)


"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_organize_data)
unittest.TextTestRunner(verbosity=2).run(suite)