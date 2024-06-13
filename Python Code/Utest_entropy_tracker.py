"""
SUMMARY:
Unit tests for the entropyTracker class from entropy_tracker.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from entropy_tracker import initializePF, timeHistory, reassignPF, evalEntropy
import unittest
import numpy as np


"""
CLASSES
"""
class test_entropy_tracker(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables for functions and methods
        """
    
    
    def test_initialize_pf(self):
        """
        Unit tests for the initializePF function
        """
        
        # Create history of pass-fail data
        passfail = [
            {None: [{'non_reduced': np.array([0.0, 0.1, -0.1]),
                     'indices': [0, 1, 2]},
                    {'non_reduced': np.array([0.0, 0.1, -0.1]),
                     'indices': [0, 1, 2]},
                    {'non_reduced': np.array([0.0, 0.1, -0.1]),
                     'indices': [0, 1, 2]},],
             'time': 40
            },
            {None: [{'non_reduced': np.array([0.0, 0.1, -0.1]),
                     'indices': [0, 1, 2]},
                    {'non_reduced': np.array([0.0, 0.1, -0.1]),
                     'indices': [0, 1, 2]},
                    {'non_reduced': np.array([0.0, 0.1, -0.1]),
                     'indices': [0, 1, 2]},],
             'time': 60
            },
            {(): [{'non_reduced': np.array([0.0, 0.1, -0.1]),
                   'indices': [0, 1, 2]},
                  {'non_reduced': np.array([0.0, 0.1, -0.1]),
                   'indices': [0, 1, 2]},
                  {'non_reduced': np.array([0.0, 0.1, -0.1]),
                   'indices': [0, 1, 2]},],
             'time': 90
            }
        ]
        
        # Create history of pass-fail standard deviation data
        passfail_std = [
            {None: [{'non_reduced': np.array([0.0, 0.1, 0.1]),
                     'indices': [0, 1, 2]},
                    {'non_reduced': np.array([0.0, 0.1, 0.1]),
                     'indices': [0, 1, 2]},
                    {'non_reduced': np.array([0.0, 0.1, 0.1]),
                     'indices': [0, 1, 2]},],
             'time': 40
            },
            {None: [{'non_reduced': np.array([0.0, 0.1]),
                     'indices': [0, 2]},
                    {'non_reduced': np.array([0.0, 0.1, 0.1]),
                     'indices': [0, 1, 2]},
                    {'non_reduced': np.array([0.1, 0.1]),
                     'indices': [1, 2]},],
             'time': 60
            },
            {(): [{'non_reduced': np.array([0.0, 0.1, 0.1]),
                   'indices': [0, 1, 2]},
                  {'non_reduced': np.array([0.0, 0.1, 0.1]),
                   'indices': [0, 1, 2]},
                  {'non_reduced': np.array([0.0, 0.1, 0.1]),
                    'indices': [0, 1, 2]},],
             'time': 90
            }
        ]
        
        # Run the function on both sets of passfail data
        passfail_frag = initializePF(passfail, 'mean')
        passfail_std_frag = initializePF(passfail_std, 'std')
        
        # Determine the expected dictionaries
        exp_passfail_frag = {
            40: [np.array([0.0, 0.1, -0.1]),
                 np.array([0.0, 0.1, -0.1]),
                 np.array([0.0, 0.1, -0.1])],
            60: [np.array([0.0, 0.1, -0.1]),
                 np.array([0.0, 0.1, -0.1]),
                 np.array([0.0, 0.1, -0.1])],
            0:  [np.array([0.0, 0.0, 0.0]),
                 np.array([0.0, 0.0, 0.0]),
                 np.array([0.0, 0.0, 0.0])]
        }
        exp_passfail_std_frag = {
            40: [np.array([0.0, 0.1]),
                 np.array([0.0, 0.1, 0.1]),
                 np.array([0.1, 0.1])],
            60: [np.array([0.0, 0.1]),
                 np.array([0.0, 0.1, 0.1]),
                 np.array([0.1, 0.1])],
            0:  [np.array([1.0/np.sqrt(3.0), 1.0/np.sqrt(3.0)]),
                 np.array([1.0/np.sqrt(3.0), 1.0/np.sqrt(3.0), 
                           1.0/np.sqrt(3.0)]),
                 np.array([1.0/np.sqrt(3.0), 1.0/np.sqrt(3.0)])]
        }
        
        # Check that actual dictionaries match up with expected dictionaries
        for (key1, val1), (key2, val2) in zip(passfail_frag.items(), 
                                              exp_passfail_frag.items()):
            self.assertEqual(key1, key2)
            for array1, array2 in zip(val1, val2):
                np.testing.assert_array_almost_equal(array1, array2)
        for (key1, val1), (key2, val2) in zip(passfail_std_frag.items(), 
                                              exp_passfail_std_frag.items()):
            self.assertEqual(key1, key2)
            for array1, array2 in zip(val1, val2):
                np.testing.assert_array_almost_equal(array1, array2)
        
    
    def test_time_history(self):
        """
        Unit tests for the timeHistory function
        """
        
        
    
    
    def test_reassign_pf(self):
        """
        Unit tests for the reassignPF function
        """
    
    
    def test_eval_entropy(self):
        """
        Unit tests for the evalEntropy function
        """
        
        
        
        
        
        
    

"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_entropy_tracker)
unittest.TextTestRunner(verbosity=2).run(suite)