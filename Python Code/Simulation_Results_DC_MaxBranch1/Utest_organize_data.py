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
from organize_data import sharedIndices, countBooleans, fillSpaceRemaining, \
    findAverages, findPercentages
import unittest
import numpy as np


"""
CLASSES
"""
class test_organize_data(unittest.TestCase):
    
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
        
        # Run the function
        space_rem, feas_rem = fillSpaceRemaining(test_case, set_of_times, Discips)
        
        # Check that the function produces the expected output
        self.assertDictEqual(space_rem, expected_space_rem)
        self.assertDictEqual(feas_rem, expected_feas_rem)
    
    
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
        
        # Run the function
        average_rem, average_feas = findAverages(space_rem, feas_rem)
        
        # Check that the function produces the expected output
        self.assertDictEqual(average_rem, expected_average_rem)
        self.assertDictEqual(average_feas, expected_average_feas)
    
    
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
        
        # Run the function
        percent_rem, percent_feas1, percent_feas2=findPercentages(average_rem,
                                                                  average_feas)
        
        # Check that the function produces the expected output
        self.assertDictEqual(percent_rem, expected_percent_rem)
        self.assertDictEqual(percent_feas1, expected_percent_feas1)
        self.assertDictEqual(percent_feas2, expected_percent_feas2)


"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_organize_data)
unittest.TextTestRunner(verbosity=2).run(suite)