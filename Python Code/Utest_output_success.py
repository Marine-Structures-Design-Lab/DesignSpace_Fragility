"""
SUMMARY:
Unit tests for the checkOutput class from output_success.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_success import checkOutput
from vars_def import setProblem
from create_key import createKey
from get_constraints import getConstraints
import unittest
import numpy as np
import copy

"""
CLASSES
"""
class test_output_success(unittest.TestCase):

    def setUp(self):
        """
        Establish dictionaries for each discipline and rules as object
        definitions
        """
        # Set up the initial list of dictionaries for each discipline and rules
        prob = setProblem()
        self.Discips, self.Input_Rules, self.Output_Rules = prob.SBD1()
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Create new keys
            self.Discips[i] = createKey('tested_outs',self.Discips[i])
            self.Discips[i] = createKey('pass?',self.Discips[i])
            
            # Add output values to all disciplines in dictionary
            ### As well as partially filled "pass?" values
            self.Discips[i]['tested_outs'] = \
                np.random.rand(20,len(self.Discips[i]['outs']))
            self.Discips[i]['pass?'] = [None]*10
        
        # Create copy of the dictionary
        self.Discips1 = copy.deepcopy(self.Discips)
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Get output rules
            output_rules = getConstraints(self.Discips1[i]['outs'],\
                                          self.Output_Rules)
            
            # Initialize object for each discipline
            outchk = checkOutput(self.Discips1[i],output_rules)
            
            # Produce new discipline
            self.Discips1[i] = outchk.basicCheck()
            
    def test_basic_check(self):
        """
        Unit tests for the basicCheck method
        """
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
        
            # Check that there is NOT rewriting of previous "pass?" values
            self.assertEqual(self.Discips1[i]['pass?'][0:10],\
                             self.Discips[i]['pass?'])
            
            # Check that there is determination of new "pass?" values
            self.assertTrue(len(self.Discips1[i]['pass?']) == 20)
            
            # Check that there is NOT determination of old "pass?" values
            self.assertTrue\
                (all(j is None for j in self.Discips1[i]['pass?'][0:10]))
            
    # Other methods
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_output_success)
unittest.TextTestRunner(verbosity=2).run(suite)