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
from windfall_regret import minmaxNormalize
from dit import ScalarDistribution
from dit.other import generalized_cumulative_residual_entropy as gcre
import unittest
import numpy as np


"""
CLASSES
"""
class test_entropy_tracker(unittest.TestCase):

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
        
        # Create a list of disciplines with space remaining data
        Discips_fragility = [
            {'space_remaining': np.zeros((10,3))},
            {'space_remaining': np.zeros((6,3))},
            {'space_remaining': np.zeros((4,3))}
        ]
        
        # Run the function
        passfail_frag = timeHistory(Discips_fragility)
        
        # Determine the expected results
        exp_passfail_frag = [
            [np.array([]) for _ in range(10)],
            [np.array([]) for _ in range(6)],
            [np.array([]) for _ in range(4)]
        ]
        
        # Check that actual results meet expected results
        for list1, list2 in zip(passfail_frag, exp_passfail_frag):
            self.assertEqual(len(list1), len(list2))
            for array1 in list1:
                self.assertEqual(array1.size, 0)
    
    
    def test_reassign_pf(self):
        """
        Unit tests for the reassignPF function
        """
        
        # Initialize old pass-fail dictionary
        pf_old = {
            40: [np.array([0.0, -0.1]),
                 np.array([0.2, -0.2, 0.3]),
                 np.array([-0.3])],
            60: [np.array([0.5, -0.5]),
                 np.array([0.6, -0.6, 0.7]),
                 np.array([-0.7])],
            0:  [np.array([0.0, 0.0]),
                 np.array([0.0, 0.0, 0.0]),
                 np.array([0.0])]
        }
        
        # Initialize new pass-fail list of lists
        pf_new = [
            [np.array([]) for _ in range(2)],
            [np.array([]) for _ in range(3)],
            [np.array([]) for _ in range(1)]
        ]
        
        # Run the function
        pf_new = reassignPF(pf_old, pf_new)
        
        # Determine the expected results
        exp_pf_new = [
            [np.array([0.0, 0.0, 0.5]), np.array([0.0, -0.1, -0.5])],
            [np.array([0.0, 0.2, 0.6]), np.array([0.0, -0.2, -0.6]), 
             np.array([0.0, 0.3, 0.7])],
            [np.array([0.0, -0.3, -0.7])]
        ]
        
        # Check that actual results meet expected results
        for list1, list2 in zip(pf_new, exp_pf_new):
            self.assertEqual(len(list1), len(list2))
            for array1, array2 in zip(list1, list2):
                np.testing.assert_array_almost_equal(array1, array2)
        
    
    def test_eval_entropy(self):
        """
        Unit tests for the evalEntropy function
        """
        
        # Initialize pass-fail and pass-fail standard deviation data
        passfail_frag = [
            [np.array([0.0, 0.0, 0.5]), np.array([0.0, -0.1, -0.5])],
            [np.array([0.0, 0.2, 0.6]), np.array([0.0, -0.2, -0.6]), 
             np.array([0.0, 0.3, 0.7])],
            [np.array([0.0, -0.3, -0.7])]
        ]
        passfail_std_frag = [
            [np.array([1.0/np.sqrt(3.0), 0.1, 0.2]), 
             np.array([1.0/np.sqrt(3.0), 0.3, 0.4])],
            [np.array([1.0/np.sqrt(3.0), 0.5, 0.6]), 
             np.array([1.0/np.sqrt(3.0), 0.7, 0.8]), 
             np.array([1.0/np.sqrt(3.0), 0.9, 1.0])],
            [np.array([1.0/np.sqrt(3.0), 0.1, 0.2])]
        ]
        
        # Run the function
        TVE = evalEntropy(passfail_frag, passfail_std_frag)
        
        # Determine the non-normalized expected results
        exp_TVE = [np.array([gcre(ScalarDistribution([0.0, 0.0, 0.5], [0.1035169465, 0.5976553689, 0.2988276845])),
                             gcre(ScalarDistribution([0.0, -0.1, -0.5], [0.2289441984, 0.4406033152, 0.3304524864]))]),
                   np.array([gcre(ScalarDistribution([0.0, 0.2, 0.6], [0.3208263473, 0.370458356, 0.3087152967])),
                             gcre(ScalarDistribution([0.0, -0.2, -0.6], [0.3926998765, 0.3238933992, 0.2834067243])),
                             gcre(ScalarDistribution([0.0, 0.3, 0.7], [0.4506837974, 0.2891137908, 0.2602024117]))]),
                   np.array([gcre(ScalarDistribution([0.0, -0.3, -0.7], [0.1035169465, 0.5976553689, 0.2988276845]))])
        ]
        
        # Determine the normalized expected results
        for i, results in enumerate(exp_TVE):
            exp_TVE[i] = minmaxNormalize(results)
        
        # Check that expected results match the actual results
        for array1, array2 in zip(TVE, exp_TVE):
            np.testing.assert_array_almost_equal(array1, array2)
        
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_entropy_tracker)
unittest.TextTestRunner(verbosity=2).run(suite)