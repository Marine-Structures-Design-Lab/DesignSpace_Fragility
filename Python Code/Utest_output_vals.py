"""
SUMMARY:
Unit tests for the getOutput class from output_vals.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_vals import getOutput
from vars_def import setProblem
from create_key import createKey
import unittest
import copy
import numpy as np

"""
CLASSES
"""
class test_output_vals(unittest.TestCase):

    def setUp(self):
        """
        Establish dictionaries for each discipline and rules as object
        definitions
        """
        # Set up the initial list of dictionaries for each discipline and rules
        prob = setProblem()
        self.Discips, self.Rules = prob.SBD1()
        
        # Loop through each discipline creating new keys and adding time
        for i in range(0,len(self.Discips)):
            self.Discips[i] = createKey('tested_ins',self.Discips[i])
            self.Discips[i] = createKey('tested_outs',self.Discips[i])
        
        # Create a copy of the list of dictionaries
        self.Discips1 = copy.deepcopy(self.Discips)
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Add input values to all disciplines in dictionary
            ### As well as partially filled output values
            self.Discips1[i]['tested_ins'] = \
                np.random.rand(20,len(self.Discips1[i]['ins']))
            self.Discips1[i]['tested_outs'] = \
                np.zeros((10,len(self.Discips1[i]['outs'])))
            self.Discips1[i]['tested_ins'] = \
                np.append(self.Discips1[i]['tested_ins'],[[5,4,2]],axis=0)
        
        # Create two more copies of the dictionaries
        self.Discips_filled = copy.deepcopy(self.Discips1)
        
        # Create an empty list of zero numpy arrays
        self.answers = [np.zeros((1,1)),np.zeros((1,2)),np.zeros((1,2))]
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Initialize different objects for each discipline
            outpts = getOutput(self.Discips_filled[i])
            
            # Produce new disciplines
            self.Discips_filled[i] = outpts.getValues()
            
            # Establish "should-be" answers for last row of each discipline
            if i == 0:
                self.answers[i] = np.array([50.0])
            elif i == 1:
                self.answers[i] = np.array([-1403.75,4356.0])
            elif i == 2:
                self.answers[i] = np.array([6.567795368,0.8661219879])
        
    def test_get_output(self):
        """
        Unit tests for the getOutput method
        """
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Check that there is NOT rewriting of previous output values
            self.assertEqual\
                (self.Discips_filled[i]['tested_outs'][0:10,:].tolist(),\
                 self.Discips1[i]['tested_outs'].tolist())
            
            # Check that there is calculation of new output values
            self.assertTrue\
                (np.all(self.Discips_filled[i]['tested_outs'][10:20,:]))
            
            # Check that there is NOT calculation of old output values
            self.assertTrue\
                (not np.all(self.Discips_filled[i]['tested_outs'][0:10,:]))
            
            # Check that correct values are being calculated
            np.testing.assert_array_almost_equal\
                (self.Discips_filled[i]['tested_outs'][20,:],
                 self.answers[i])
    
    # Other methods
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_output_vals)
unittest.TextTestRunner(verbosity=2).run(suite)